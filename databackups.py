from aiogram import Dispatcher, Bot, executor
from aiogram import types
from datetime import datetime
from loguru import logger
import random
import asyncio
import json
import os 
import zipfile

# # # # # # # # # # # # # # # # # # # # #
#                                       #
#               CONFIG                  #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

BOT_TOKEN = ""
SETTINGS_FILE = "databackups_settings.json"
BACKUP_TIME = "15:00"

# folders for backup
backup_targets = [
    "Data",
    "DataBackups",
    "MaFiles"
]

# # # # # # # # # # # # # # # # # # # # #
#                                       #
#             STARTUP FUNCTION          #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

BACKUP_TIME = datetime.strptime(BACKUP_TIME, "%H:%M")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN is not set")
    input()
    quit()

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher(bot)

async def startup(dp):
    global ONE_TIME_CODE
    ONE_TIME_CODE = random.randint(100000, 999999)
    me = await bot.get_me()
    logger.success(f"Bot started as @{me.username}. Admin code: {ONE_TIME_CODE}")

@dp.message_handler(commands=["test", "backup", "b"])
async def test_backup(message: types.Message):
    admins = Settings.get("admins", [])
    if message.from_user.id not in admins:
        await message.answer("[DataBackups] Вас нет в белом списке") 
        return
    
    zip_file_name = create_zip_archive(backup_targets)

    await bot.send_document(
        chat_id = message.from_user.id, 
        document = types.InputFile(zip_file_name, filename = zip_file_name), 
        caption = f"[DataBackups] #backup {zip_file_name}"
    )
    os.remove(zip_file_name)

@dp.message_handler()
async def access_command(message: types.Message):
    admins = Settings.get("admins", [])
    if message.from_user.id in admins:
        await message.answer("[DataBackups] Вы уже добавлены в белый список") 
        return
    
    if message.text == str(ONE_TIME_CODE):
        await message.answer("[DataBackups] Код верный, аккаунт добавлен в белый список")
        Settings.set("admins", admins + [message.from_user.id])
    else:
        await message.answer("[DataBackups] Вы ввели неверный код")

# # # # # # # # # # # # # # # # # # # # #
#                                       #
#             SETTINGS FILE             #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

class Settings:
    @staticmethod
    def load():
        if not os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "w") as f:
                json.dump({}, f)
            logger.debug(f"Settings file {SETTINGS_FILE} created")

        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def get(key: str, default = None):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        return data.get(key, default)
    
    @staticmethod
    def set(key: str, value):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        data[key] = value
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)


# # # # # # # # # # # # # # # # # # # # #
#                                       #
#              MAIN PART                #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

async def wait_time():
    """wait until BACKUP_TIME"""
    await asyncio.sleep(5)
    while True:
        now = datetime.now()
        if now.hour == BACKUP_TIME.hour and now.minute == BACKUP_TIME.minute:
            logger.success(f"Start backup at {now}")
            await make_backups()
        await asyncio.sleep(60) # ждем 60 секунд перед проверкой снова

async def make_backups():
    zip_file_name = create_zip_archive(backup_targets)
    admins = Settings.get("admins", [])
    if not admins:
        logger.error("No admins found")
        return

    for admin in admins:
        try:
            await bot.send_document(
                chat_id = admin, 
                document = types.InputFile(zip_file_name, filename = zip_file_name), 
                caption = f"[DataBackups] #backup {zip_file_name}"
            )
            logger.success(f"Backup sent to {admin}")
        except Exception as e:
            logger.error(f"Error sending backup to {admin}: {e}")
            logger.exception(e)
    else:
        logger.info(f"Backup sent to {len(admins)} admins")
    os.remove(zip_file_name)
    

def create_zip_archive(files_list):
    zip_file_name = f"TradeOnBackup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_list:
            if os.path.isfile(file):
                zipf.write(file, arcname=os.path.basename(file))
            elif os.path.isdir(file):
                for root, dirs, files in os.walk(file):
                    for f in files:
                        file_path = os.path.join(root, f)
                        zipf.write(file_path, arcname=os.path.relpath(file_path, file))

    return zip_file_name

# # # # # # # # # # # # # # # # # # # # #
#                                       #
#            INIT AND START             #
#               EXECUTOR                #
#                                       #
# # # # # # # # # # # # # # # # # # # # #

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(wait_time())

executor.start_polling(dp, loop = loop, skip_updates = True, on_startup = startup)
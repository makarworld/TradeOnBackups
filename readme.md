## Бот для автоматического бекапа данных TradeOn
Каждый день в заданное время бот создаёт архив из папок Data, DataBackups, MaFiles и отправляет вам.
Если что-то случится с сервером вы не потеряете данные о покупках и сможете откатиться к ним в любой момент.

![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/8ffe8b32-970b-4f98-ade5-1e0ed104dbed)

## Установка
1. Установите python 3.10+
2. Установите зависимости, напишите в консоли `pip install aiogram==2.25.1 loguru`
3. Переместите файл `databackups.py` в папку с ботом TradeOn 
4. В файле `databackups.py` в 17 строке впишите `BOT_TOKEN` от @BotFather (!! Важно, это должен быть не токен из TradeOn бота, создайте новый)
5. В 19 строке можете вписать своё время для бекапа
6. Запустите файл `databackups.py`
7. Отправьте вашему боту Admin code который был показан в консоли при старте программы. (6 цифр)
![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/d4b55cfb-e5de-4a57-9f85-b8cfbb9b1d93)

![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/0601b041-f36b-4999-af72-cebb8ea96a0e)


## Ошибки

_aiogram.utils.exceptions.TerminatedByOtherGetUpdates: Terminated by other getupdates request; make sure that only one bot instance is running_

**Вы поставили на один токен 2 бота, замените BOT_TOKEN**

_No admins found_

**Вы не добавили себя в белый список, для этого введите Admin code который был показан при старте бота**

## Бот для автоматического бекапа данных TradeOn
Каждый день в заданное время бот создаёт архив из папок Data, DataBackups, MaFiles и отправляет вам.
Если что-то случится с сервером вы не потеряете данные о покупках и сможете откатиться к ним в любой момент.

![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/8ffe8b32-970b-4f98-ade5-1e0ed104dbed)

## Установка
1. Установите python 3.10+
2. Установите зависимости, напишите в консоли `pip install aiogram==2.25.1 loguru`
3. В файле `databackups.py` в 17 строке впишите `BOT_TOKEN` от @BotFather (!! Важно, это должен быть не токен из TradeOn бота, создайте новый)
4. В 19 строке можете вписать своё время для бекапа
5. Запустите файл `databackups.py`
6. Отправьте вашему боту Admin code который был показан в консоли при старте программы. (6 цифр)
![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/3b8c4f1f-f9c1-497a-8819-4486b8f054f1)
![image](https://github.com/makarworld/TradeOnBackups/assets/58076271/a3eca241-6d5a-4afa-80fe-1d252f8d9724)

## Ошибки

_aiogram.utils.exceptions.TerminatedByOtherGetUpdates: Terminated by other getupdates request; make sure that only one bot instance is running_

**Вы поставили на один токен 2 бота, замените BOT_TOKEN**

_No admins found_

**Вы не добавили себя в белый список, для этого введите Admin code который был показан при старте бота**

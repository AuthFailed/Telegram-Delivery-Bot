# CRM-система курьерской службы
[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/AuthFailed/Telegram-Delivery-Bot/issues/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![time tracker](https://wakatime.com/badge/github/AuthFailed/Telegram-Delivery-Bot.svg)](https://wakatime.com/badge/github/AuthFailed/Telegram-Delivery-Bot)

## Установка
1. Клонируйте этот репозиторий 
```sh https://github.com/AuthFailed/Telegram-Delivery-Bot```
2. Установите и запустите Redis сервер
3. Установите и запустите PostgreSQL сервер
4. Установите зависимости командой `pip install -r requirements.txt`
5. Создайте и настройке файл `bot.ini` по примеру из файла [bot.ini.example](./tgbot/bot.ini.example)
6. Запустите бота как сервис из папки `systemd` либо командой `python bot.py`

## Что бот умеет?
- [X] Регистрация
  - [X] Как частное лицо
  - [X] Как компания
  - [X] Как курьер
- [X] Система ролей
  - [X] Администратор
  - [X] Менеджер
  - [X] Курьер
  - [X] Заказчик  
- [X] Система заказов
  - [X] Оформление заказ
  - [X] Изменение и отслеживание статуса заказа
  - [X] Назначение курьера на заказ
- [X] Система профилей
  - [X] У заказчика: Информация о его заказах, возможность изменения личных данных, удаление профиля
  - [X] У курьера: Информация о взятых заказах, возможность изменения статуса на 'Занят', 'Свободен' и 'На заказе'
- [X] Логирование
  - [X] Все логи записываются не только на сервере, но и в отдельный чат в Telegram'e

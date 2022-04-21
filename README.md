#Телеграм бот для поиска отелей в любом городе мира

#Команды бота:

* /lowprice - поиск cамых дешевых отелей
* /highprice - поиск самых дорогих отелей
* /bestdeal - поиск отелей по цене и удалению от центра города
* /history - история поиска
* /help - список команд бота
   
#Для запуска бота нужно:

1) Получить токен бота:

    * Запустить Telegram
    * Перейти в бота: @BotFather
    * Нажать кнопку: START (Если вы ранее уже создавали ботов — перейдите к 4 пункту)
    * Написать боту: /newbot.
    * Введите название нового бота
    * Введите ник бота, чтобы он заканчивался на слово bot                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

      
2) Получить токен от hotels Api:

    * Зарегистрироваться на сайте rapidapi.com.
    * Перейти в API Marketplace → категория Travel → Hotels
    * Нажать кнопку Subscribe to Test.
    * Выбрать бесплатный пакет (Basic)


3) Вставить полученные токены в файл env.example в переменные BOT_TOKEN и API_TOKEN


4) Переименовать env.example файл в .env


5) Установить виртуальное окружение введя в консоль команду pip install -r requirements.txt


6) Запустить модуль app.py командой python3 app.py
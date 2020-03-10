# Rest_api
REST API on Flask

Для запуска сервиса необходимо под Windows

1. Установить docker toolbox
2. Скачать или клонировать проект
3. Запустить docker terminal и запомнитб ip адрес docker виртуальной машины например будет - is configured to use the default machine with IP 192.168.99.100
4. В фойле config.py проекта поменять 'host': '192.168.99.100' на свой 'host': 'ip адрес docker виртуальной машины'
5. Зайти в папку проекта через docker terminal
6. Выполнить в docker terminal команду  docker-compose build
7. Выполнить команду  docker-compose up -d
8. Перейти по адресу виртуальной машины и порт 5000 - http://http://192.168.99.100/:5000
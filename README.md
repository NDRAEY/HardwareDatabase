# HardwareDatabase

Установка для Debian Linux 11:
Mongo DB:
```
echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" > /etc/apt/sources.list.d/mongodb-org-4.4.list
apt-get update

apt-get install mongodb-org
```

Скачивание проекта:
```
git clone https://github.com/NDRAEY/HardwareDatabase
```

Запуск проекта:
```
cd HardwareDatabase/frontend
python manage.py runserver
```

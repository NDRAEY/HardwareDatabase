# HardwareDatabase

Установка для Debian Linux 11:

Mongo DB:
```
sudo su

echo "deb [trusted=yes] http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" > /etc/apt/sources.list.d/mongodb-org-4.4.list
apt-get update

apt-get install mongodb-org

exit
```

Возможно будет необходимо включить автозапуск MongoDB:
```
sudo systemctl enable mongod
sudo systemctl start mongod
```

Скачивание проекта:
```
git clone https://github.com/NDRAEY/HardwareDatabase
```

Установка проекта:
```
cd HardwareDatabase/frontend
sudo pip3 install -r requirements.txt
```

Запуск проекта:
```
python manage.py runserver
```

## Описание:
Тестовое задание для blockchain solutions.
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/seerez/bs_test.git
```
```
cd blockchain
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/bin/activate
```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
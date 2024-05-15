## 1. Встановлення залежностей
```
    pip install -r requirements.txt
```
## 2. Виконання міграцій
```
    python manage.py migrate
```
## 3. Створити superuser
```
   python manage.py createsuperuser  
```
## 4. Заповнення бази даних
```
   python manage.py populate_db
```
## 5. Запуск проєкту
```
    python manage.py runserver
```
## 5. Запуск проєкту в Docker
```
    Для запуску проєкту в Docker, потрібно зайти в 
    кореневу папку та запустити файл docker-compose.yaml
    або за допомогою команди "docker compose up"
```

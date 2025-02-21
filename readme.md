# sleep
 - Проставить правильно логин и пароль постгреса в компоуз файле
 - Поднять бд
    ```
    docker-compose pull postgres:latest
    docker-compose build
    docker-compose up
    ```
 - Запустить models.py с правильными данными из компоуз файла 
 - Открыть localhost:8000/docs
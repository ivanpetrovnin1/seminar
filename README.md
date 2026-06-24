# LinkShortest_I

LinkShortest_I – сервис сокращения ссылок, позволяющий пользователям создавать и удалять их по своим коротким URL. Проект реализован на FastAPI для backend, а также Streamlit для frontend. В качестве бд для сервиса используется PostgreSQL и Redis для кэширования. Сервис поддерживает регистрацию пользователей и создание кастомных alias-ссылок с возможностью ограничения времени жизни ссылок.

## Функциональные возможности сервиса

### Функции

- **Создание, удаление, изменение и получение информации по короткой ссылке:**
  - `POST /api/links/create` – создание новой ссылки с возможностью указания кастомного alias и времени жизни.
  - `GET /api/links/list` – вывод всех ссылок, созданных данным пользователем.
  - `DELETE /api/links/delete/{short_code}` – удаление ссылки.
- **Регистрация и управление аккаунтом:**
  - `POST /api/auth/register` – регистрация нового пользователя.
  - `POST /api/auth/login` – вход в систему (с установкой cookie-сессии).
  - `DELETE /api/auth/user` – удаление аккаунта (с каскадным удалением всех связанных ссылок).
- **Кэширование популярных ссылок:**  
  Redis используется для кэширования данных перенаправления, что ускоряет обработку запросов.

## Стэк сервиса

- **Backend:** FastAPI, Uvicorn, SQLAlchemy, psycopg2, python-dotenv, passlib, Redis, Pydantic.
- **Frontend:** Streamlit, Requests.
- **База данных:** PostgreSQL.
- **Кэширование:** Redis.
- **Контейнеризация:** Docker, Docker Compose.

## Структура проекта

```
LinkShortest_I/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env              
│   └── app/
│       ├── main.py
│       ├── api/
│       │   ├── auth.py
│       │   └── links.py
│       ├── core/
│       │   ├── cache.py
│       │   ├── config.py
│       │   ├── database.py
│       │   └── security.py
│       ├── models/
│       │   ├── user.py
│       │   └── link.py
│       ├── schemas/
│       │   ├── user.py
│       │   └── link.py
│       └── services/
│           └── shortener.py
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── frontend_utils.py
│   └── app.py
├── docker-compose.yml    
└── README.md
```

## Тестирование

1. **Настройка переменных окружения для запуска:**  
   В файле `backend/.env` укажите следующие значения по шаблону:

   ```env
   DATABASE_URL=postgresql://urlshort:urlshortpass@localhost:5432/urlshort_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=YOUR_SECRET_KEY
   SESSION_TTL=86400
   INACTIVITY_DAYS=90
   ```

Важно, чтобы PostgreSQL и Redis были запущены на локальной машине.

1. **Отдельный запуск backend:**
Перейдите в папку backend и выполните:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступно по ссылке <http://localhost:8000>.

1. **Отдельный запуск frontend:**
Перейдите в папку frontend и выполните:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

Frontend-приложение будет доступно по ссылке <http://localhost:8501>.

1. **Docker Compose**

Для сборки сервиса воедино был написан docker-compose.yml файл.

Запустить все сервисы можно командой:

```bash
docker compose up --build
```

## Основные шаги в интерфейсе

### Регистрация

![Регистрация](image/registration.jpg)

### Создание ссылок

![Создание ссылок](image/create_link.jpg)

### Получение ссылок

![Получение ссылок](image/links.jpg)

### Удаление аккаунта

![Удаление аккаунта](image/delete_user.jpg)

### Выход из аккаунта

![Выход из аккаунта](image/logout.jpg)

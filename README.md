# E_COMMERCE_BOT#

Платформа для интернет-магазина, состоящая из двух приложений:  
- **Telegram-бот** (Aiogram 3) для взаимодействия с пользователями и администраторами.  
- **API-сервис** (FastAPI) для управления каталогом, заказами и данными.

Оба сервиса используют **PostgreSQL** и общую директорию **shared** для схем и утилит.

## Функционал

### Для пользователя:
- Просмотр каталога товаров:
  - категории
  - список товаров
  - детальная страница товара
- Корзина:
  - удаление товаров
  - изменение количества
- Подтверждение заказа 

### Для администратора:
-  Добавление нового товара (через бота):
  - категория
  - название
  - описание
  - цена
  - количество на складе
  - фото
-  Редактирование товара

### API:
- Работа с пользователями, товарами, заказами и корзиной  
- JSON-эндпоинты для интеграции с внешними сервисами  
- Swagger-документация (`/docs`)

##  Технологии

- Python 3.11
- Aiogram 3
- PostgreSQL
- SQLAlchemy + asyncpg
- Docker + Docker Compose
- FastAPI (API)  

## Структура проекта
│── bot/
│ ├── app/shared/db/
│ ├── app/shared/schemas/
│ ├── app/keyboards/ 
│ ├── app/handlers/ 
│ ├── app/states/ 
│ ├── app/pages/
│ ├── app/notifications/
│ ├── app/utils/
│ ├── app/auth.py
│ ├── app/main.py # Точка входа
│ ├── Dockerfile
│ └── requirements.txt
│── api/
│ ├── app/shared/db/
│ ├── app/shared/schemas/
│ ├── app/routers/ 
│ ├── app/main.py # Точка входа
│ ├── Dockerfile
│ └── requirements.txt
│── shared/
│ ├── db/
│ ├── schemas/
│── .env # Создать
│── docker-compose.yml
└── README.md

## ⚙️ Установка и запуск
### Клонируем репозиторий
git clone https://github.com/LyHaTik/E_COMMERCE_BOT

### Создаём файл .env для бота:
BOT_TOKEN=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=

ADMINS = [...] # Список ID админов

### Запускаем проект через Docker
docker-compose up --build
docker-compose up

## Дополнительно
Общая бизнес-логика вынесена в shared/ и используется обоими сервисами.
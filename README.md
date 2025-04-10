
# 🇰🇿 Tax Codex AI Chat API

**Tax Codex AI** — это RESTful API, созданный на FastAPI, который предоставляет чат-интерфейс с использованием OpenAI для ответа на вопросы, связанные с Налоговым кодексом Республики Казахстан. Система поддерживает регистрацию и авторизацию пользователей, сохраняет историю чатов и использует SQLite (или другую БД) как хранилище.

---

## 🚀 Функционал

- 🔐 Регистрация и авторизация пользователей (JWT токены)
- 💬 Задать вопрос ИИ по налоговому кодексу РК
- 📜 Получить историю своих чатов
- 🌐 CORS поддержка
- 🧠 Использование OpenAI GPT-3.5-turbo
- ✅ Healthcheck и test-эндпоинты

---

## 📁 Структура проекта

```
Backend/
├── models/           # SQLAlchemy модели (User, ChatHistory)
├── routes/           # Маршруты FastAPI (user, chat)
├── services/         # Вызов OpenAI API
├── database.py       # Подключение к БД, создание таблиц
├── chat.db           # SQLite база данных (или другая через .env)
├── .env              # Конфиденциальные переменные
├── main.py           # Точка входа (FastAPI)
```

---

## ⚙️ Установка и запуск

### 1. Клонируй репозиторий
```bash
git clone https://github.com/your-username/tax-codex-ai.git
cd tax-codex-ai/Backend
```

### 2. Создай виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

### 3. Установи зависимости
```bash
pip install -r requirements.txt
```

### 4. Создай `.env` файл
```env
DATABASE_URL=sqlite:///./chat.db
OPENAI_API_KEY=sk-...
```

### 5. Запусти сервер
```bash
uvicorn main:app --reload
```

---

## 🛠️ API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/register` | Регистрация пользователя |
| `POST` | `/api/login` | Авторизация и получение JWT |
| `POST` | `/api/ask` | Отправка вопроса ИИ (требуется токен) |
| `GET` | `/api/history` | Получение истории чатов (требуется токен) |
| `GET` | `/api/healthcheck` | Проверка состояния сервера |
| `GET` | `/api/test` | Тестовый эндпоинт |

---

## 🔐 Авторизация

Для доступа к защищённым маршрутам (`/ask`, `/history`) используй JWT токен:

```
Authorization: Bearer <your_token>
```

---

## 🤖 OpenAI Интеграция

Сервис использует модель `gpt-3.5-turbo` и предоставляет системную инструкцию, чтобы ответы были в контексте **Налогового кодекса РК** (https://adilet.zan.kz/rus/docs/K1700000120).

---

## 🧠 Пример запроса/ответа

**POST /api/ask**

```json
{
  "question": "Какие налоги платит ИП на упрощенке?"
}
```

**Ответ:**
```json
{
  "answer": "ИП на упрощенной декларации платит индивидуальный подоходный налог в размере 3% от дохода..."
}
```

---

## 📚 Технологии

- **FastAPI**
- **SQLAlchemy**
- **OpenAI API**
- **JWT (OAuth2PasswordBearer)**
- **Pydantic**
- **SQLite** (или PostgreSQL и др.)
- **CORS Middleware**

---

## 📩 Контакты

Если у тебя есть вопросы или предложения — feel free to reach out! 😄

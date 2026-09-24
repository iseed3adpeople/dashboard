# dashboard

Личная стартовая страница: обратный отсчёт до дня рождения, текущая погода
и простой чек-лист целей, которые можно отмечать/добавлять/удалять прямо
на странице.

## Стек

- Flask
- Vanilla JS (fetch) на фронте

## Установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните значения:

```bash
cp .env.example .env
```

- `BIRTHDAY` — дата в формате `YYYY-MM-DD`, до которой считаются дни
- `OPENWEATHER_API_KEY` — ключ с [openweathermap.org](https://openweathermap.org/api)
- `CITY` — город для прогноза погоды

## Запуск

```bash
python app.py
```

Откройте http://localhost:5000.

## Структура

```
app.py        — маршруты Flask
config.py     — конфигурация из .env
goals.json    — хранилище целей (простой JSON-файл)
templates/    — HTML
static/       — CSS
```

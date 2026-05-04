# Docker deploy (AWS EC2)

## 1) Подготовка на сервере
- Установить Docker + Docker Compose plugin.
- Открыть порты в Security Group: `80` (и `22` для SSH).

## 2) Подготовка проекта
```bash
cp .env.example .env
```

Заполни `.env`:
- `POSTGRES_PASSWORD` (обязательно поменять)
- `DJANGO_ALLOWED_HOSTS` (например: `your-domain.com,www.your-domain.com,<EC2_PUBLIC_IP>`)
- при HTTPS добавь `DJANGO_CSRF_TRUSTED_ORIGINS` (например: `https://your-domain.com,https://www.your-domain.com`)

## 3) Запуск
```bash
docker compose up -d --build
```

## 4) Проверка
```bash
docker compose ps
docker compose logs -f web
docker compose logs -f nginx
```

Сайт будет доступен на `http://<EC2_PUBLIC_IP>`.

## 5) Полезные команды
```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py populate_cars
docker compose down
```

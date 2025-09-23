# 🩺 Appointment Project  

پروژه **مدیریت تایم ویزیت دکتر** ساخته شده با **Django** و **Docker**.  

---

## ✨ Features
- مدیریت بیماران و پزشکان  
- رزرو وقت آنلاین  
- پنل ادمین  

---

## 🔧 Requirements
- Python 3.12  
- Docker & Docker Compose  

---

## 🚀 Setup
```bash
git clone https://github.com/erfanmhi-23/appointment.git
cd appointment

# Run containers
docker compose up --build

# Apply migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

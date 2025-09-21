# 🩺 Appointment Project  

پروژه **مدیریت تایم ویزیت دکتر** ساخته شده با **Django** و **Docker**.  

---

## ✨ ویژگی‌ها
- مدیریت بیماران و پزشکان  
- رزرو وقت آنلاین  
- پنل ادمین جنگو  

---

## 🔧 پیش‌نیازها
برای اجرای پروژه نیاز به نصب موارد زیر دارید:  
- [Python 3.12](https://www.python.org/)  
- [Docker](https://www.docker.com/)  
- [Docker Compose](https://docs.docker.com/compose/)  
- Django (داخل کانتینر نصب می‌شود)  

---

## 🚀 نصب و راه‌اندازی  

### 1. کلون کردن پروژه
```bash
git clone https://github.com/erfanmhi-23/appointment.git
cd appointment
 
#Docker
docker compose up --build

#migrate
docker compose exec web python manage.py migrate

#superuser
docker compose exec web python manage.py createsuperuser

#addres
http://localhost:8000
#admin panel(django)
http://localhost:8000/admin

#ساختار پروژه 
app doctor
app patient
app wallet
app review
app user


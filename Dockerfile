<<<<<<< HEAD
FROM python:3.11
=======
FROM docker.arvancloud.ir/python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
>>>>>>> Erfan

WORKDIR /app

COPY requirements.txt .
<<<<<<< HEAD
=======

RUN pip install --upgrade pip
>>>>>>> Erfan
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

<<<<<<< HEAD
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
=======
EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
>>>>>>> Erfan

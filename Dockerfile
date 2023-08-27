FROM python:3.11.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV SECRET_KEY=django-insecure-p^*p!+dt8ccl@aac(mh%wy&wy=+bapiw4r+psw&0r&2=*cegiw
ENV IS_DEVELOPMENT=True
ENV APP_HOST=*

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]

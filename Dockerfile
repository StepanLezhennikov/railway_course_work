FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

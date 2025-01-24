FROM python:3.12-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "until pg_isready -h db -p 5431 -U django -d mydatabase; do sleep 2; done; python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

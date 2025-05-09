FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install flask pika

EXPOSE 5000

CMD ["python", "rabbitmq.py"]
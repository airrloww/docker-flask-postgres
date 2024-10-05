FROM python:3.9-slim

RUN apt update && apt install netcat-traditional

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env .

COPY entrypoint.sh .
RUN chmod +x /app/entrypoint.sh

EXPOSE 5000

CMD ["/app/entrypoint.sh"]

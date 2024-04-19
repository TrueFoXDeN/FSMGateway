FROM python:3.11-alpine

WORKDIR /app

COPY . .
RUN mkdir /app/cert
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-u", "app.py"]
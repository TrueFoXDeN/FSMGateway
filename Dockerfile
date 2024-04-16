FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .
RUN mkdir /app/cert
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
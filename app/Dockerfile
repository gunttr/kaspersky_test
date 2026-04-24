FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt ./
COPY wheels/ ./wheels/

RUN pip install --no-index --find-links=./wheels --no-cache-dir -r requirements.txt

COPY service.py .

EXPOSE 8080

CMD ["python3", "service.py"]
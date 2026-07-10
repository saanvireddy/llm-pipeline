FROM python:3.11-slim

WORKDIR /app

COPY requirements-serve.txt .
RUN pip install --no-cache-dir -r requirements-serve.txt

COPY serving/ ./serving/
COPY training/adapter/ ./training/adapter/

EXPOSE 8000

CMD ["uvicorn", "serving.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
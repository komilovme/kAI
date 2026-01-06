FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai_server.py .

EXPOSE 10000
CMD ["python", "ai_server.py"]

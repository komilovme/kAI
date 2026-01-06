FROM python:3.11-slim

# system deps
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# workdir
WORKDIR /app

# install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY main.py .

# start server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

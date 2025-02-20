FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Set environment variables to suppress TensorFlow warnings
ENV TF_ENABLE_ONEDNN_OPTS=0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

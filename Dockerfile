# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
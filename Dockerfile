FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=covidhelp.settings
ENV ALLOWED_HOSTS=*

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "covidhelp.wsgi:application", "--bind", "0.0.0.0:8000"] 
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
ENV PORT=8000

# Create a simple startup script
RUN echo '#!/bin/bash\n\
echo "Starting Django server..."\n\
python manage.py migrate --noinput\n\
python manage.py collectstatic --noinput\n\
gunicorn covidhelp.wsgi:application --bind 0.0.0.0:$PORT --log-level debug\n'\
> /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"] 
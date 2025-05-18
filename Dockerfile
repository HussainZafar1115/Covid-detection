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

# Create a startup script with better error handling and logging
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting deployment checks..."\n\
\n\
echo "Running database migrations..."\n\
python manage.py migrate --noinput\n\
\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
\n\
echo "Testing Django configuration..."\n\
python manage.py check --deploy\n\
\n\
echo "Starting Gunicorn..."\n\
exec gunicorn covidhelp.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120 --access-logfile - --error-logfile - --log-level debug\n'\
> /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Run the startup script
CMD ["/app/start.sh"] 
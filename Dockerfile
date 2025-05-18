FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

# Create a startup script that uses the PORT env var
RUN echo '#!/bin/bash\nport="${PORT:-8000}"\ngunicorn covidhelp.wsgi:application --bind "0.0.0.0:$port" --log-level debug' > /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"] 
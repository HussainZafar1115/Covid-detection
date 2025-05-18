FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "debug"] 
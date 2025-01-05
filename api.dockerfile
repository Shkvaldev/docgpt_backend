FROM python:3.12-slim

COPY api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

CMD uvicorn api:app --host 0.0.0.0 --port 80 --workers 3

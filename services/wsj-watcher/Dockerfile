FROM mcr.microsoft.com/playwright/python:v1.63.0-noble
USER root
RUN apt-get update && apt-get install -y --no-install-recommends nginx apache2-utils x11-utils x11vnc novnc websockify && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY watcher.py entrypoint.sh ./
RUN chmod +x entrypoint.sh && mkdir -p /data && chown -R pwuser:pwuser /app /data
ENV DATA_DIR=/data DISPLAY=:99 MODE=login PORT=8080 PYTHONUNBUFFERED=1
ENTRYPOINT ["/app/entrypoint.sh"]

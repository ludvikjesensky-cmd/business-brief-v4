FROM python:3.12-slim
WORKDIR /app
COPY bridge/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY bridge /app/bridge
COPY src/business_brief/contracts.py /app/bridge/contracts.py
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "bridge.server"]

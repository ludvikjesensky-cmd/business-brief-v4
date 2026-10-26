FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir 'psycopg[binary]==3.2.12'
COPY src/business_brief/__init__.py src/business_brief/dashboard.py src/business_brief/dashboard.sql /app/business_brief/
ENV PORT=8080
USER 65534:65534
EXPOSE 8080
CMD ["python", "-m", "business_brief.dashboard"]

FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy


RUN useradd -m -u 1000 sentineluser

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium


COPY --chown=sentineluser:sentineluser . .
RUN mkdir -p /app/evidence && chown sentineluser:sentineluser /app/evidence


USER sentineluser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================================
# Dockerfile — analytics_app (FastAPI + loader)
# Variant 9: Liquidity App / FastAPI + ARG app version
# ============================================================
FROM python:3.10-slim

ARG APP_VERSION=0.1.0
ENV APP_VERSION=${APP_VERSION}

LABEL maintainer="student" \
      description="Liquidity analytics stack: ETL loader + FastAPI"

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser -u 1000 -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY loader.py main.py ./

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

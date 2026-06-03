FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    INSIGHT_AGENT_ROOT=/app \
    HOST=0.0.0.0 \
    PORT=8081

COPY pyproject.toml README.md ./
COPY app ./app
COPY data ./data
COPY prompts ./prompts
COPY payloads ./payloads
COPY templates ./templates
COPY static ./static

RUN pip install --no-cache-dir .

EXPOSE 8081

CMD ["insight-agent"]

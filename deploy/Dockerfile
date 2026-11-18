# syntax=docker/dockerfile:1
# ─────────────────────────────────────────────────────────────
# MllyMed — production konteyneri
# Mahsulot kodi O'ZGARTIRILMAYDI: backend ataylab 127.0.0.1 da ishlaydi
# (xavfsiz default). Konteynerda socat 0.0.0.0:8200 → 127.0.0.1:9000
# ko'prigi yoqiladi — kodga bir satr ham tegilmaydi.
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    INTERNAL_PORT=9000 \
    PUBLIC_PORT=8200

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir "requests>=2.31,<3" \
    && useradd --system --uid 10001 --shell /usr/sbin/nologin mllymed

WORKDIR /app

# Faqat kerakli fayllar (qolgani deploy/.dockerignore da chiqarib tashlangan)
COPY --chown=mllymed:mllymed . /app

# Runtime yozuv papkalari (SQLite + agent outbox) — yoziladigan bo'lishi shart
RUN mkdir -p /app/built/data/runtime /app/orindor/data/runtime \
    && chown -R mllymed:mllymed /app/built/data/runtime /app/orindor/data/runtime \
    && chmod +x /app/deploy/entrypoint.sh

USER mllymed

EXPOSE 8200

HEALTHCHECK --interval=30s --timeout=4s --start-period=20s --retries=3 \
    CMD python3 -c "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:9000/api/health',timeout=3).status==200 else 1)"

ENTRYPOINT ["/app/deploy/entrypoint.sh"]

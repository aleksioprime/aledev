FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/src/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=Europe/Moscow

# netcat-openbsd — ожидание базы в entrypoint.sh, tzdata — часовой пояс
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY . .

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

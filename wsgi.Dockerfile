# docker build --tag django_ecs .
# docker run -p 8000:8000 --rm -it django_ecs:latest
# wrk -t2 -c5 -d30s http://127.0.0.1:8000/json/
FROM python:3.13-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD ./ /django

WORKDIR /django/django_ecs_performance_tests

RUN uv sync --locked
ENV PATH="/django/.venv/bin:$PATH"

EXPOSE 8000

# WSGI
# Gevent
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_ecs_performance_tests.wsgi", "-k", "gevent", "--workers", "1"]
# Sync
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_ecs_performance_tests.wsgi", "-k", "sync", "--workers", "1"]
# Gthread
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_ecs_performance_tests.wsgi", "-k", "gthread", "--workers", "1", "--threads", "100"]
# Granian
CMD [ \
    "granian", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "django_ecs_performance_tests.wsgi:application", \
    "--interface", "wsgi", \
    "--workers", "1", \
    "--backpressure", "34", \
    "--no-ws", \
    "--loop","uvloop", \
    "--log-level","info",\
    "--log", \
    "--workers-lifetime", "10800", \
    "--respawn-interval", "30" \
]

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
# CMD [ \
#     "taskset", "-c", "0", \
#     "granian", \
#     "--host", "0.0.0.0", \
#     "--port", "8000", \
#     "django_ecs_performance_tests.wsgi:application", \
#     "--interface", "wsgi", \
#     "--workers", "100", \
#     # "--backpressure", "34", \
#     "--no-ws", \
#     "--loop","uvloop", \
#     "--log-level","error",\
#     "--log", \
#     "--workers-lifetime", "10800", \
#     "--respawn-interval", "30" \
# ]

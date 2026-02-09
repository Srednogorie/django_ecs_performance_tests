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

# ASGI
# Granian
CMD [ \
    "granian", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "django_ecs_performance_tests.asgi:application", \
    "--interface", "asgi", \
    "--workers", "1", \
    "--backpressure", "2000", \
    "--no-ws", \
    "--loop","uvloop", \
    "--log-level","error", \
    "--backlog", "2048" \
]

# Daphne
# CMD [ \
#     "daphne", \
#     "-b", "0.0.0.0", \
#     "-p", "8000", \
#     "django_ecs_performance_tests.asgi:application" \
# ]

# Uvicorn
# CMD [ \
#     "gunicorn", \
#     "django_ecs_performance_tests.asgi:application", \
#     "-w", "4", \
#     "-k", "uvicorn.workers.UvicornWorker", \
#     "--bind", "0.0.0.0:8000", \
#     "--backlog", "2048", \
#     "--worker-connections", "2000", \
#     "--max-requests", "10000", \
#     "--max-requests-jitter", "100", \
#     "--timeout", "60", \
#     "--keep-alive", "5", \
#     "--access-logfile", "/dev/null", \
#     "--log-level", "error" \
# ]

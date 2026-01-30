# docker run -p 8000:8000 -it django-ecr
FROM python:3.13-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD ./ /django

WORKDIR /django/django_ecs_performance_tests

RUN uv sync --locked
ENV PATH="/django/.venv/bin:$PATH"

EXPOSE 8000

# CMD gunicorn --pid=gunicorn.pid django_ecs_performance_tests.wsgi:application -c gunicorn_conf.py
# CMD ["gunicorn", "--worker-class", "gevent", "django_ecs_performance_tests.django_ecs_performance_tests.wsgi:application"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "django_ecs_performance_tests.wsgi", "-k", "gevent", "--workers", "4"]

FROM python:slim

# ARG UID=10001
# RUN adduser \ --disabled-password \ --gecos "" \ --home "/nonexistent" \ --shell "/sbin/nologin" \ --no-create-home \ --uid "${UID}" \ appuser
# USER appuser

RUN python -m pip install Django uvicorn
WORKDIR /app

COPY main.py main.py

EXPOSE 8000

# We dont need it if .env file used
ENV DJANGO_SETTINGS_MODULE=settings

CMD uvicorn main:asgi --host 0.0.0.0 --lifespan=off --factory
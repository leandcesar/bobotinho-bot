# syntax=docker/dockerfile:1

FROM python:3.9-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements/prod.txt .
RUN pip install -r requirements/prod.txt

COPY . .
CMD ["python", "-m", "bobotinho"]
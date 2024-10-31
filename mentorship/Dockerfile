FROM python:3.10-slim

WORKDIR /appпше

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY . .

RUN poetry install --no-root --no-interaction --no-ansi

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "mentorship.wsgi:application"]

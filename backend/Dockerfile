FROM python:3.11-slim

WORKDIR /app

COPY ./backend /app
COPY ./model /app/model

ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]

FROM python:3.11-slim

WORKDIR /app

COPY . . 

ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]

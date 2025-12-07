FROM python:3.11-slim

WORKDIR /app

COPY requirementes.txt .

RUN pip install --no-cache-dir -r requirementes.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

EXPOSE 5050

CMD ["python", "app.py"]


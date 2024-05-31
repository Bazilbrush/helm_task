FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py app.py
COPY birds.db birds.db


EXPOSE 80

# Define the command to run the application
CMD ["python", "app.py"]

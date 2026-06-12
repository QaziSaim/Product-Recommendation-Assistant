FROM python:3.12-slim

WORKDIR /app

COPY . .

# Fix is right here: double dashes!
RUN pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.13
WORKDIR /app

COPY requirements.txt .
COPY app ./app
COPY .env .

RUN pip install -r requirements.txt

EXPOSE 8000
ENV OLLAMA_HOST=http://host.docker.internal:11434
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
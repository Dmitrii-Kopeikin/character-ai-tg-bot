FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5080"]
# CMD ["gunicorn", "app.main:app", "-b", "0.0.0.0:5080", "-w", "1", "-k", "uvicorn.workers.UvicornWorker"]
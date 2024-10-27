FROM python:3.9

WORKDIR /opt/truematch
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN apt update
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod a+x /opt/truematch/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

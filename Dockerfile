FROM python:3.9-slim

# Install MySQL client
RUN apt-get update && \
  apt-get install -y mariadb-client && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backup_restore.py .

RUN pip install mysql-connector-python==8.0.26

RUN mkdir /backups

CMD ["python", "backup_restore.py"]

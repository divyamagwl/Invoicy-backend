FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev default-libmysqlclient-dev build-essential iputils-ping -y

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
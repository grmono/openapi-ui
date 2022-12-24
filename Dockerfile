FROM python:3.8.6 as base
FROM base as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    python3 -m ensurepip && \
    pip install --upgrade pip

COPY /requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

# copy source files
COPY app ./app
WORKDIR /app
RUN chmod +x start_app.sh
ENTRYPOINT ["/bin/bash", "start_app.sh"]

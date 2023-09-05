FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
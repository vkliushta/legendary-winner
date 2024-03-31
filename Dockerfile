FROM python:3.12-slim

# for more info see https://github.com/PyMySQL/mysqlclient/blob/main/README.md#linux
RUN apt-get update && \
    apt-get -y install python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN mkdir /legendary-winner-app
WORKDIR /legendary-winner-app

COPY reqs ./reqs
RUN pip install --no-cache-dir -r reqs/test-requirements.txt

COPY . .

EXPOSE 8000

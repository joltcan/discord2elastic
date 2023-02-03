FROM python:3.10-alpine

LABEL maintainer="Fredrik Lundhag <f@mekk.com>"

RUN pip3 install discord elasticsearch

COPY . /app
WORKDIR /app

USER nobody

CMD ["./discord2elastic.py"]

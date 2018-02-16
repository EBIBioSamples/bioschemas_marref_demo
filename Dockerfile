FROM python:3.6
COPY ./crawler /
WORKDIR /crawler
RUN pip install -r requirements.txt

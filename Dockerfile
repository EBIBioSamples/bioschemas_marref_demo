FROM python:2.7

WORKDIR /MarRef/
EXPOSE 8080

CMD ["python", "-m", "SimpleHTTPServer", "8080"]

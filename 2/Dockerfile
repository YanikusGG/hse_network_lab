FROM python:3.10-alpine

WORKDIR /script

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apk update && apk add iputils

ENTRYPOINT ["python", "main.py"]

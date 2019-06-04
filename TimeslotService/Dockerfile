FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /TimeslotService
COPY . /TimeslotService
RUN pip3 install -r requirements.txt
EXPOSE 8888
WORKDIR /TimeslotService/demo
CMD python3 __init__.py

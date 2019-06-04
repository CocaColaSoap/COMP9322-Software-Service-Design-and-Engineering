FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /DoctorService
COPY . /DoctorService
RUN pip3 install -r requirements.txt
EXPOSE 5000
WORKDIR /DoctorService/demo
CMD python3 __init__.py

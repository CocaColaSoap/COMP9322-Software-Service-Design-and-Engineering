docker build -t doctor_service .
docker run -p 127.0.0.1:5000:5000 -t doctor_service
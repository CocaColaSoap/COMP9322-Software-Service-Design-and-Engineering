docker build -t timeslot_service .
docker run -p 127.0.0.1:8888:8888 -t timeslot_service
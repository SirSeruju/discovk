FROM python:3.9.6-slim
WORKDIR /discovk
COPY ./src /discovk
RUN apt update &&\
    apt install -y git ffmpeg &&\
    pip install -r /discovk/requirements.txt &&\
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
CMD ["python", "/discovk/main.py"]

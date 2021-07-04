FROM python:3.9.6-slim
WORKDIR /
RUN apt update &&\
    apt install -y git ffmpeg &&\
    git clone https://github.com/SirSeruju/discovk &&\
    pip install -r /discovk/requirements.txt
COPY config.py /discovk/
CMD ["python", "/discovk/main.py"]

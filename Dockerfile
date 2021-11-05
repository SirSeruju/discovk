FROM alpine
WORKDIR /discovk
COPY ./src /discovk
RUN apk update &&\
    apk add --no-cache python3 ffmpeg &&\
    apk add --no-cache py3-pip gcc python3-dev musl-dev libffi-dev make &&\
    pip3 install -r /discovk/requirements.txt &&\
    apk del gcc python3-dev musl-dev libffi-dev make
CMD ["python3", "/discovk/main.py"]

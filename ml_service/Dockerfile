FROM python:3.10

SHELL [ "/bin/bash", "-c" ]

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6  -y && \
    pip install --upgrade pip && \ 
    pip install -r /app/requirements.txt

CMD python3 run.py
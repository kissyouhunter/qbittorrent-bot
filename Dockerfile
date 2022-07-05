FROM python:3.8-slim-buster
ADD . /app
RUN apt update && apt install -y gcc zip curl \
    && curl https://rclone.org/install.sh | bash \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apt purge -y zip curl \
    && apt clean all \
    && apt-get autoremove --purge \
    && mkdir -p /Downloads \
    && cd /app && pip3 install -r requirements.txt
WORKDIR /app
ENTRYPOINT python main.py

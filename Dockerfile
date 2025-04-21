FROM python:3.12-slim

# 替换为国内源
RUN echo  "deb http://mirrors.aliyun.com/debian bullseye main" >/etc/apt/sources.list 
RUN echo  "deb http://mirrors.aliyun.com/debian-security bullseye-security main" >>/etc/apt/sources.list 
RUN echo  "deb http://mirrors.aliyun.com/debian bullseye-updates main" >>/etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

COPY wcocr.cpython-312-x86_64-linux-gnu.so /app/wcocr.cpython-312-x86_64-linux-gnu.so

COPY wx /app/wx

COPY main.py /app/main.py

WORKDIR /app

CMD ["python", "main.py"]
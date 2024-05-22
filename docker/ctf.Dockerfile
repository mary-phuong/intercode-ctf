FROM ubuntu:latest

# Install required dependencies
RUN apt-get update && \
    apt-get install -y bash python3 python3-pip psmisc bsdmainutils cron imagemagick dnsutils git wget gcc sleuthkit netcat-traditional unzip curl gdb poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install required pip dependencies
RUN mv /usr/lib/python3.12/EXTERNALLY-MANAGED /usr/lib/python3.12/EXTERNALLY-MANAGED.old
RUN pip3 install pycryptodome

# Load in per-task assets
COPY data/ctf/task_assets/. /ctf/
RUN find /ctf/ -type d -name solution -prune -exec rm -rf {} \;

RUN cd /ctf/1 \
  && wget https://mercury.picoctf.net/static/aed64c508175df5fe23207c10e0e47e5/dds2-alpine.flag.img.gz
RUN cd /ctf/14 \
  && git clone https://github.com/ReFirmLabs/binwalk.git
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install binwalk gdb tshark bc fcrackzip fdisk inetutils-ping john parallel # mlocate
RUN pip3 install cryptography

# Commit custom file system to determine diffs
COPY docker/docker.gitignore /
RUN mv docker.gitignore .gitignore
RUN git config --global user.email "intercode@pnlp.org"
RUN git config --global user.name "intercode"
RUN git init
RUN git add -A
RUN git commit -m 'initial commit'

WORKDIR /ctf
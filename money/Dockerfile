FROM ubuntu:jammy

RUN groupadd --gid 1001 devteam

RUN useradd -s /bin/bash -d /home/money -m money --gid 1001 --uid 1000
WORKDIR /home/money

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install --no-install-recommends -y python3-dev && \
  apt-get install --no-install-recommends -y libmysqlclient-dev && \
  apt-get install --no-install-recommends -y python3-pip && \
  apt-get install --no-install-recommends -y pkg-config && \
  apt-get install --no-install-recommends -y build-essential && \
  apt-get install --no-install-recommends -y sudo && \
  apt-get install --no-install-recommends -y cron && \
  apt-get install --no-install-recommends -y tzdata && \
  rm -rf /var/lib/apt/lists/*

RUN usermod -aG sudo money && \
  echo "money ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN touch /var/log/cron.log

USER money
COPY ./requirements.txt .

RUN sudo chown money:devteam requirements.txt

RUN pip install --no-cache-dir --requirement requirements.txt && \
  pip install --no-cache-dir pytz --upgrade && \
  pip install --no-cache-dir tzdata --upgrade

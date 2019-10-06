FROM continuumio/anaconda3:2019.03

RUN apt-get update && \
        apt-get install -y gcc build-essential libomp-dev libopenblas-dev

ADD requirements.txt /tmp/
WORKDIR /tmp
RUN pip install -r requirements.txt
ARG CACHEBUST=1
ADD requirements_dev.txt /tmp/
RUN pip install -r requirements_dev.txt

RUN mkdir -p ${HOME}/docsim

FROM continuumio/anaconda3:2019.03

RUN apt-get update && \
        apt-get install -y gcc build-essential libomp-dev libopenblas-dev

ADD requirements.txt /tmp/
WORKDIR /tmp
RUN pip install -r requirements.txt

RUN mkdir -p ${HOME}/docsim

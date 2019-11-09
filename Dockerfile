FROM continuumio/anaconda3:2019.03

WORKDIR /workplace
RUN apt-get update && \
        apt-get install -y gcc build-essential libomp-dev libopenblas-dev cmake pkg-config gfortran

WORKDIR /tmp
ENV SENTENCEPIECE_HOME /tmp/sentencepiece
ENV PKG_CONFIG_PATH ${SENTENCEPIECE_HOME}/lib/pkgconfig
RUN wget https://github.com/google/sentencepiece/archive/v0.1.84.zip && \
    unzip v0.1.84.zip
WORKDIR sentencepiece-0.1.84
RUN mkdir -p build
WORKDIR ./build
RUN cmake -DCMAKE_INSTALL_PREFIX=${SENTENCEPIECE_HOME} ..  && make -j4 && make install
WORKDIR ../python
RUN python setup.py install

RUN mkdir /workplace/.env
ADD .env/main.env /workplace/.env/main.env

ARG CACHEBUST=1
WORKDIR /workplace
RUN pip install numpy scipy Cython
ADD requirements_mine.txt /workplace/
RUN pip install -r requirements_mine.txt
ADD requirements_dev.txt /workplace/
RUN pip install -r requirements_dev.txt
ADD requirements.txt /workplace/
RUN pip install -r requirements.txt
# NLP Kits
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

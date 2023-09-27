FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install dependencies
RUN apt update -y
RUN apt install -y software-properties-common build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libsctp-dev git nano python3-pip lsof
RUN pip3 install libconf google-cloud-storage
# Install USRP drivers
#RUN add-apt-repository ppa:ettusresearch/uhd
RUN apt install -y libuhd-dev uhd-host

# Install libasn
RUN git clone https://github.com/j0lama/libasn.git
WORKDIR libasn
RUN make -j$(nproc --ignore=1)
RUN make install
WORKDIR ../

# Download USRP images
RUN /usr/lib/uhd/utils/uhd_images_downloader.py

# Build ng-scope
RUN git clone https://github.com/YaxiongXiePrinceton/NG-Scope ng-scope
WORKDIR ng-scope/
RUN mkdir build
WORKDIR build/
RUN cmake ../
RUN make -j$(nproc --ignore=1)
WORKDIR ngscope/src/
RUN mkdir logs

# Copy tools
COPY tools/* .
COPY tools/utils/* .
COPY start.sh .
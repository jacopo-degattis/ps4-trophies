FROM ubuntu:22.04

# TODO: move from python3 to golang compiled program to setup so it doesn't use all that space and it's faster
RUN apt update &&  apt install -y wget unzip make clang lld jq curl git llvm

# Configure needed libSSL
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb
RUN dpkg -i libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb
RUN rm libssl1.0.0_1.0.2n-1ubuntu5_amd64.deb

# Download the last orbis-toolchain
WORKDIR /opt
ADD ./setup.sh /opt/setup.sh
RUN chmod +x /opt/setup.sh && /opt/setup.sh
RUN unzip toolchain-llvm-18.zip
RUN tar -xvf toolchain-llvm-18.tar.gz

# Now cleanup
RUN apt remove -y unzip wget
RUN rm /opt/setup.sh toolchain-llvm-18.zip toolchain-llvm-18.tar.gz

COPY build_rules.mk /opt/OpenOrbis/PS4Toolchain/build_rules.mk
ENV OO_PS4_TOOLCHAIN=/opt/OpenOrbis/PS4Toolchain

RUN ls $OO_PS4_TOOLCHAIN

# Install libjbc
RUN git clone https://github.com/bucanero/ps4-libjbc.git && \
    cd ps4-libjbc && \
    make && \
    cp -frv libjbc.h $OO_PS4_TOOLCHAIN/include && \
    cp -frv libjbc.a $OO_PS4_TOOLCHAIN/lib

RUN echo "[+] Done"
FROM ubuntu:22.04

# TODO: move from python3 to golang compiled program to setup so it doesn't use all that space and it's faster
RUN apt update &&  apt install -y wget unzip make clang lld jq curl

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

ENV OO_PS4_TOOLCHAIN=/opt/OpenOrbis/PS4Toolchain

RUN echo "[+] Done"
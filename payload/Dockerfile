FROM alpine:3.18

# Install dependencies
RUN apk update && apk add --no-cache \
    git \
    make \
    build-base \
    clang \
    llvm \
    lld \
    cmake \
    python3 \
    bash \
    wget \
    && rm -rf /var/cache/apk/*

# Clone and install PS4 Payload SDK
WORKDIR /build
RUN git clone https://github.com/Scene-Collective/ps4-payload-sdk.git
WORKDIR /build/ps4-payload-sdk
RUN chmod +x install.sh && ./install.sh

# Set up environment variables
ENV PS4SDK=/lib/ps4-payload-sdk/
ENV PATH=$PS4SDK/toolchain/bin:$PATH

# Set working directory for user's source code
WORKDIR /src

# Default command: bash shell
CMD ["make"]
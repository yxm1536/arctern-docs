FROM ubuntu:18.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends wget build-essential tree git ca-certificates curl \
    libgl-dev libosmesa6-dev libglu1-mesa-dev  && \
    wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    apt-get remove --purge -y && \
    mkdir /arctern-docs && \
    rm -rf /var/lib/apt/lists/*

COPY docker/docker-entrypoint.sh /opt/docker-entrypoint.sh

ENTRYPOINT [ "/opt/docker-entrypoint.sh" ]

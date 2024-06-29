ARG CUDA_VERSION=11.6.1
ARG UBUNTU_VERSION=20.04
FROM nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    git \
    python3 \
    python3-dev \
    python3-pip \
    python3-tk \
    libopencv-dev
RUN rm -rf /var/lib/apt/lists/*
RUN rm /etc/apt/apt.conf.d/docker-clean

USER $USERNAME
ENV SHELL /bin/bash

RUN wget -O ~/requirements.txt https://github.com/cvg/LightGlue/raw/main/requirements.txt
RUN pip3 install -r ~/requirements.txt
RUN pip3 install git+https://github.com/cvg/LightGlue

CMD ["/bin/bash"]

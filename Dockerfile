FROM ubuntu:18.04

# install some utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    bzip2 \
    ca-certificates \
    curl \
    git \
    locales \
    nano \
    sudo \
    unzip \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# configure environment
SHELL ["/bin/bash", "-c"]
RUN locale-gen en_US.UTF-8
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    HOME=/home/root
WORKDIR $HOME
RUN echo 'PS1="(docker) \W/ \$ "' > .bashrc

# install miniconda
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O miniconda.sh
RUN chmod +x miniconda.sh && ./miniconda.sh -b -p miniconda && rm miniconda.sh
ENV PATH "$HOME/miniconda/bin:$PATH"
RUN conda update -y conda && conda update -y --all && conda config --add channels conda-forge

# configure project
COPY . cerberus
WORKDIR $HOME/cerberus
# RUN make install

EXPOSE 8080
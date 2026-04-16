FROM fedora:latest

# システム更新 & Python環境
RUN dnf -y update && \
    dnf -y install \
        python3 \
        python3-pip \
        python3-devel \
        gcc \
        gcc-c++ \
        make \
        openblas-devel \
        lapack-devel \
        && dnf clean all

# pip更新
RUN python3 -m pip install --upgrade pip

# pythonライブラリ
RUN pip install \
        numpy \
        scipy \
        pandas \
        matplotlib \
        ruff \
        pytest \
        pytest-cov


WORKDIR /balloon-simulation
COPY . /balloon-simulation

ENV PYTHONPATH=/balloon-simulation/py
CMD ["bash"]
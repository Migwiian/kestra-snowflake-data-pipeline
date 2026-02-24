FROM kestra/kestra:v1.1

USER root

# Install Kaggle CLI (python3 + pip)
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && pip3 install --no-cache-dir kaggle \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER root

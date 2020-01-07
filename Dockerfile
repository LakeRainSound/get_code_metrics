FROM python:3.7.6-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cloc && \
    pip install --no-cache-dir pipenv && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/list/*

WORKDIR /opt/gcm

COPY . ./

RUN pipenv install --system && \
    rm -rf $HOME/.cache/pip && \
    rm -rf $HOME/.cache/pipenv

CMD ["/bin/bash", "./gcm_exe.sh"]

FROM python:3.7.6-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        cloc \
	git \
	wget \
	locales-all && \
    wget https://github.com/AlDanial/cloc/releases/download/1.84/cloc-1.84.pl && \
    mv ./cloc-1.84.pl /usr/local/bin/cloc && \
    chmod +x /usr/local/bin/cloc && \
    pip install --no-cache-dir pipenv && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/list/*

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /opt/gcm

COPY . ./

RUN pipenv install --system && \
    rm -rf $HOME/.cache/pip && \
    rm -rf $HOME/.cache/pipenv

CMD ["/bin/bash", "./gcm_exe.sh"]
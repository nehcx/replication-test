FROM python:3.8-buster as builder

LABEL maintainer="xchen@shs.titech.ac.jp"

WORKDIR /opt/app

# Environment
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -yq ssh git curl apt-utils && \
    apt-get install -yq gcc g++ cmake && \
    apt-get install -y r-base r-cran-rcppeigen

# Code
RUN git clone -b main --depth=1 --recursive https://github.com/nehcx/replication-test
# RUN mkdir replication-test
# COPY ./ /opt/app/replication-test

# Python dependencies
RUN pip install -r replication-test/requirements.lock

# R dependencies
RUN R -e "install.packages(c('tidyverse', 'ggplot2', 'svglite', 'ggpubr', 'showtext'), repos = 'http://cran.us.r-project.org')"

# Data
RUN wget -c https://raw.githubusercontent.com/nehcx/hachidaishu/main/hachidai.db -O replication-test/data/hachidai.db
RUN wget -c https://gist.githubusercontent.com/nehcx/a09664d75d9151538457ab697ee6a98c/raw/74e3a0e0ca7df5af5572912881035829168ac0e8/example.csv -O replication-test/data/example.csv

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
RUN R -e "install.packages(c('tidyverse', 'ggplot2', 'svglite', 'ggpubr'), repos = 'http://cran.us.r-project.org')"

# Data
RUN wget -c https://raw.githubusercontent.com/nehcx/hachidaishu/main/hachidai.db -O replication-test/data/hachidai.db

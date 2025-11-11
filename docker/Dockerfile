FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y git make python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# TODO: pandoc/latex/manubot hier installieren

CMD ["make", "html"]

FROM golang:1.20.2 as builder

WORKDIR /usr/src
RUN git clone https://github.com/grafana/k6.git
WORKDIR /usr/src/k6
RUN CGO_ENABLED=0 GOARCH=arm64 go build -o /usr/bin/k6 .

FROM alpine:3

RUN apk add --no-cache bash

COPY --from=builder /usr/bin/k6 /usr/bin/k6

ADD assets /home/k6/assets
ADD k6-load-test-1.js /home/k6/k6-load-test-1.js
ADD run.sh /home/k6/run.sh

WORKDIR /home/k6

ENTRYPOINT ["bash", "run.sh"]

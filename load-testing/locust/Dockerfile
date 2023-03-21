FROM locustio/locust:2.15.1

WORKDIR /home/locust

ADD assets assets
ADD locustfile.py ./
ADD run.sh ./

ENV PYTHONUNBUFFERED=1
ENV SIMOD_HTTP_URL=http://simod-http:8000

EXPOSE 8089
EXPOSE 5557

ENTRYPOINT ["bash", "run.sh"]
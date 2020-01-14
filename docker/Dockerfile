FROM openjdk:slim
COPY --from=python:3.6-slim / /
RUN apt update && \
    apt install -y git build-essential wget 
RUN git clone https://github.com/jax79sg/artyins-jobservice && \
    cd artyins-jobservice && \
    pip install -r requirements.txt 
EXPOSE 9891
WORKDIR artyins-jobservice
ENTRYPOINT ["gunicorn","--bind","0.0.0.0:9891","--workers","10","wsgi:app"]


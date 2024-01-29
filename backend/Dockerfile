FROM python:3.11-slim

WORKDIR /usr/src/app

COPY .. .

RUN apt-get update && apt-get install -y \
    curl \
    && curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz \
    && mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh \
    && rm /tmp/google-cloud-sdk.tar.gz

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -e 'backend/src'

RUN mkdir -p /etc/ssl

# Prod settings
RUN echo "$SSL_CERTIFICATE" > /etc/ssl/cert.crt
RUN echo "$SSL_KEY" > /etc/ssl/cert.key

# Dev settings
#COPY frontend/cert.pem /etc/ssl/cert.pem
#COPY frontend/key.pem /etc/ssl/key.pem

EXPOSE 8000

CMD ["uvicorn", "backend.src.mlcb_services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ssl-certfile", "/etc/ssl/cert.pem", "--ssl-keyfile", "/etc/ssl/key.pem"]

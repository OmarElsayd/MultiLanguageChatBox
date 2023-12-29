FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y \
    curl \
    && curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz \
    && mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh \
    && rm /tmp/google-cloud-sdk.tar.gz

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN pip install --no-cache-dir -e 'backend/src'

EXPOSE 8000

CMD ["uvicorn", "backend.src.rtvt_services.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

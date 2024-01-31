FROM python:3.11-slim

WORKDIR /usr/src/app

# Copy application source code
COPY .. .

# Install necessary packages and Google Cloud SDK
RUN apt-get update && apt-get install -y curl \
    && curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz \
    && mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh \
    && rm /tmp/google-cloud-sdk.tar.gz

ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# Install Python dependencies
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -e 'backend/src'

# Optionally set up SSL (for local development)
# RUN mkdir -p /etc/ssl
# COPY frontend/cert.pem /etc/ssl/cert.pem
# COPY frontend/key.pem /etc/ssl/key.pem


EXPOSE 8000

# Use an entrypoint script to dynamically use the PORT environment variable
COPY backend/entrypoint.sh /usr/src/app
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

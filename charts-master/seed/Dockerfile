FROM google/cloud-sdk:alpine

ENV VAULT_VERSION 0.10.1

# Custom stuff we use in our scripts
RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools requests && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN apk add --no-cache curl \
    bash \
    make \
    coreutils

# Install Kubectl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

# Install VAULT
RUN wget -qO /tmp/vault.zip "https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip" && \
unzip -d /bin /tmp/vault.zip && \
chmod 755 /bin/vault && \
rm /tmp/vault.zip

COPY src/ seed/

WORKDIR /seed

CMD ["python3", "seed_main.py"]

FROM python:3.9-slim

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# COPY . /app/
COPY setup.py /app/
COPY logo.png /app/
COPY requirements.txt /app/
COPY app.py /app/

COPY components /app/components
COPY .streamlit /app/.streamlit

RUN apt-get update && apt-get install -y ca-certificates
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
RUN pip install --default-timeout=100 kaleido==0.2.1
RUN pip install --default-timeout=100 -r requirements.txt



EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]
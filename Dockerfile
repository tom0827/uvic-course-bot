FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN openssl s_client -showcerts -connect heat.csc.uvic.ca:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > server_cert.pem
RUN apt-get update && apt-get install -y curl
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

CMD ["python", "main.py"]
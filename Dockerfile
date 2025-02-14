FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 python3-pip nodejs npm curl git && \
    apt-get clean

COPY . .

RUN pip3 install --no-cache-dir -r Telegram/requirements.txt

RUN npm install --prefix Discord \
    && npm install --prefix WhatsApp \
    && npm install --prefix Instagram \
    && npm install --prefix X

RUN chmod +x start.sh

CMD ["sh", "-c", "./start.sh"]

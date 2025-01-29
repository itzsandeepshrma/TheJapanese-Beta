FROM python:3.8-slim AS build

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    python3-dev \
    build-essential \
    git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/TeamJapanese/The-Japanese.git /app/TeamJapanese

WORKDIR /app/TeamJapanese

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY --from=build /app/TeamJapanese /app/TeamJapanese

ENV API_ID=$API_ID \
    API_HASH=$API_HASH \
    BOT_TOKEN=$BOT_TOKEN \
    STRING_SESSION=$STRING_SESSION \
    OWNER_ID=$OWNER_ID \
    WA_API_ID=$WA_API_ID \
    WA_API_HASH=$WA_API_HASH \
    WA_BOT_TOKEN=$WA_BOT_TOKEN \
    INSTAGRAM_USERNAME=$INSTAGRAM_USERNAME \
    INSTAGRAM_PASSWORD=$INSTAGRAM_PASSWORD \
    INSTAGRAM_API_KEY=$INSTAGRAM_API_KEY \
    ENCRYPTION_KEY=$ENCRYPTION_KEY

EXPOSE 5000

CMD ["python", "main.py"]

# ClairDiceBot

Telegram dice bot for WoD system


Собрать докер контейнер из исходников репозитория, запустить и удалить после себя:

```
git clone https://github.com/wod-serial/ClairDiceBot.git
cd ClairDiceBot.git
sudo docker run -e TOKEN=TELEGRAM_TOKEN --rm -it $(sudo docker build -q .)
```

Скачать готовый контейнер и запустить:

```
sudo docker run -e TOKEN=TELEGRAM_TOKEN --rm -it ghcr.io/wod-serial/clairdicebot:latest
```

docker-compose:

```
version: "3.8"

services:
  diun:
    image: ghcr.io/wod-serial/clairdicebot:latest
    restart: unless-stopped
    environment:
      TOKEN: ${TOKEN}
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 100M
    mem_swappiness: 0
    memswap_limit: 0
 ```
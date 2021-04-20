# FindGameBot
Simple Telegram bot that searches games, and the stores that sell them, using [RAWG](https://rawg.io). 
Currently can be found on [@find_game_bot](https://t.me/find_game_bot)

## Dependencies
* python-telegram-bot
* requests
* dataclasses-json

## Docker support
You will need to pass your token to the container using `-e` or `--env-file`.

Run command will look something like this:

```
docker run -d \
    --restart unless-stopped \
    --name gamefinderbot \
    --env-file params.env \
    ghcr.io/graynk/astrologers_bot:latest
```

## Usage
1. In the "Write a message" field put "@find_game_bot Portal 2"
1. Select the needed result

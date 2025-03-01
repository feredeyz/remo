## ***<p align="center">Remo Telegram Bot<p>***

## Description
Remo is a bot created to easily connect to different servers and proceeds commands on it. Connections may be done localy or with SSH.

## Installation
To install Remo, run these commands:
```
git clone https://github.com/feredeyz/remo remo
cd remo
```

## Setting Up
1. ***For Linux***: To set up Remo, run `sh ./scripts/setup.sh` and `source .venv/bin/activate`.
2. ***For Windows***: To set up Remo, run `run ./scripts/setup.bat`.

After that, install `cloudflared` package to run Flask server and run `sh run_server.sh`.
Then, copy URL you got from cloudflared and paste it into `webapp_url` in `config.json`.
Next, insert your Telegram Bot Token into `TOKEN` in `config.json`.
To enable proceeding commands localy, insert your chat id in `admins` in `config.json`.

## Contacts
k.dmitriev1@yandex.ru
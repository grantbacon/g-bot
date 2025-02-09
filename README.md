# signal_bot

This is a small implementation of a bot for Signal that has several commands. This repo relies on [filipre/signalbot](https://github.com/filipre/signalbot) latest version v0.12.0.
It relies on an instance of [signal-cli-rest-api](https://github.com/signal-cli-rest-api) to be running.

Currently you can install by running

```bash
pip install -r requirements.txt
python bot.py
```

You should set any needed credentials as well as the SIGNAL_ADDR and PHONE_NUM in `.env` (see `.env.example`)

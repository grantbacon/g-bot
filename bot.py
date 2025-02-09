from commands import (
    UptimeCommand,
    WeatherCommand,
    DeepSeekCommand,
    BalanceCommand,
    GarfieldCommand,
    HelpCommand,
    RollCommand,
)
from signalbot import SignalBot
from dotenv import dotenv_values


def main():
    config = dotenv_values(".env")
    # logging.getLogger().setLevel(logging.INFO)
    bot = SignalBot(
        {
            "signal_service": config["SIGNAL_ADDR"],
            "phone_number": config["PHONE_NUM"],
            "storage": {"redis_host": "127.0.0.1", "redis_port": "6397"},
        }
    )
    bot.register(UptimeCommand())
    bot.register(WeatherCommand())
    bot.register(DeepSeekCommand())
    bot.register(BalanceCommand())
    bot.register(GarfieldCommand())
    bot.register(HelpCommand())
    bot.register(RollCommand())

    bot.start()


if __name__ == "__main__":
    main()

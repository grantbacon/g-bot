import subprocess

from signalbot import Context, triggered

from commands import GCommand


class UptimeCommand(GCommand):
    def describe(self) -> str:
        return ".uptime - get uptime of system running bot"

    @triggered(".uptime", case_sensitive=False)
    async def handle(self, context: Context):
        await super().handle(context)
        result = subprocess.run(["uptime"], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8").strip()
        await context.reply("uptime: " + output)
        return

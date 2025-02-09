from signalbot import Command, Context


class GCommand(Command):
    def describe(self) -> str:
        return ""

    async def handle(self, context: Context):
        # c = context
        # logging.warn(
        #     str(self.__class__)
        #     + "[ "
        #     + c.message.source
        #     + "@"
        #     + c.message.recipient()
        #     + "]: "
        #     + c.message.text
        # )
        return

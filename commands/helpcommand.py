from signalbot import Context, regex_triggered
from commands import GCommand

import os
import importlib
import inspect


def aggregate_descriptions(base_class, directory):
    descriptions = []

    for filename in os.listdir(directory):
        if filename.endswith("command.py") and filename != "__init__.py":
            module_name = filename[:-3]  # Remove '.py' from filename
            module = importlib.import_module(f"{directory}.{module_name}")

            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, base_class)
                    and obj != base_class
                ):
                    instance = obj()
                    descriptions.append(instance.describe())

    return descriptions


class HelpCommand(GCommand):
    def describe(self) -> str:
        return ".help - get list of commands"

    @regex_triggered(r"^\.help")
    async def handle(self, context: Context):
        await super().handle(context)

        descriptions = aggregate_descriptions(GCommand, "commands")

        await context.start_typing()
        await context.reply("\n".join(descriptions))
        await context.stop_typing()

import random
from commands import GCommand
from signalbot import regex_triggered, Context


class RollCommand(GCommand):
    def describe(self) -> str:
        return ".roll [N] [D<M>] - roll N dice of size M (default: 1 D6)"

    @regex_triggered(r"\.roll\s?\d*\s?[dD]?\d*")
    async def handle(self, context: Context):
        await super().handle(context)

        # Extract the number of dice and die size from the command
        text = context.message.text.strip()
        parts = text.split()

        num_dice = 1  # Default to 1 die
        die_size = 6  # Default to a 6-sided die

        if len(parts) > 1:
            # Check if first part is a number (number of dice)
            if parts[1].isdigit():
                num_dice = int(parts[1])
                if num_dice < 1:
                    await context.reply("Number of dice must be at least 1.")
                    return

                # Check if there's a die size specified
                if len(parts) > 2:
                    die_arg = parts[2].upper()
                    if (die_arg.startswith("D") or die_arg.startswith("d")) and die_arg[
                        1:
                    ].isdigit():
                        die_size = int(die_arg[1:])
            else:
                # Only die size specified
                die_arg = parts[1].upper()
                if (die_arg.startswith("D") or die_arg.startswith("d")) and die_arg[
                    1:
                ].isdigit():
                    die_size = int(die_arg[1:])

        if die_size < 2:
            await context.reply("Die size must be at least 2.")
            return

        if num_dice > 1024:
            await context.reply("# of die must be <= 1024")
            return

        # Roll the dice
        results = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(results)

        if num_dice == 1:
            await context.reply(f"🎲 You rolled a {results[0]} (D{die_size})")
        else:
            await context.reply(
                f"🎲 You rolled {results} = {total} ({num_dice}D{die_size})"
            )

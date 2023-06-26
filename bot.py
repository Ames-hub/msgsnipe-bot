from extensions.botlib.botlib import bot, botprint, token, standardized_strftime, hikari, os, time
from hikari import presences

@bot.listen()
async def on_ready(event: hikari.events.ShardReadyEvent):
    print("Shard is ready!")

bot.load_extensions_from("extensions/active/")
bot.load_extensions_from("extensions/active/api/")
# bot.load_extensions_from("extensions/tasks_directory/")

try:
    bot.run(enable_signal_handlers=True, status=presences.Status.IDLE)
except hikari.errors.UnauthorizedError:
    # Surprisingly, this wont cause an error as APPARENTLY errors.UnauthorizedError exists as a potentially provided error for bot.run
    botprint("Invalid token provided. Token = "+ str(token))
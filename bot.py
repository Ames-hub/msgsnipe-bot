from extensions.botlib.botlib import bot, botprint, token, standardized_strftime, hikari, os, time
from hikari import presences

@bot.listen()
async def on_ready(event: hikari.events.ShardReadyEvent):
    print("Shard is ready!")

bot.load_extensions_from("extensions/active/")
bot.load_extensions_from("extensions/active/api/")
# bot.load_extensions_from("extensions/tasks_directory/")

if os.name != "nt":
    if os.path.exists("data/guilds/"):
        amount = len(os.listdir("data/guilds/")) * 5
        amount += 5
    else:
        amount = 5
else:
    amount = 1

try:
    bot.run(enable_signal_handlers=True, status=presences.Status.IDLE, shard_count=amount)
except hikari.errors.UnauthorizedError:
    # Surprisingly, this wont cause an error as APPARENTLY errors.UnauthorizedError exists as a potentially provided error for bot.run
    botprint("Invalid token provided. Token = "+ str(token))
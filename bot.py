from extensions.botlib.botlib import *
from hikari import presences

if not os.path.exists("data/logs/"):
    os.mkdir("data/logs/")
if not os.path.exists("data/logs/time_tracker"):
    with open("data/logs/time_tracker", "w+") as f:
        f.write(time.strftime(standardized_strftime))

@bot.listen()
async def on_ready(event: hikari.events.ShardReadyEvent):
    print("Shard is ready!")

bot.load_extensions_from("extensions/active/")
# bot.load_extensions_from("extensions/tasks_directory/")

try:
    bot.run(enable_signal_handlers=True, status=presences.Status.IDLE)
except hikari.errors.UnauthorizedError:
    botprint("Invalid token provided. Token = "+ str(token))
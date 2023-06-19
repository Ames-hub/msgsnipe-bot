from ..botlib.botlib import *

@tasks.task(s=5, wait_before_execution=True, auto_start=True)
async def undefined_task():
    print("undefined task!")

# The name that'll show up when the bot loads the plugin
ext = "task_name"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
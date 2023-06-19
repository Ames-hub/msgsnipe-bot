from ..botlib.botlib import *
import lightbulb

# Refers to being a child from the def in the group assigner template
@bot.command
@lightbulb.app_command_permissions(dm_enabled=True)
# enter the lines below this with options for the child if desired
# Adds a cooldown to the command
@lightbulb.add_cooldown(bucket=lightbulb.buckets.GuildBucket, length=5, uses=1)
@lightbulb.command("childname", "a template group child")
# Its a "slash sub command" opposed to a slash command in a group
@lightbulb.implements(lightbulb.SlashCommand)
# The command its self. Change "template" to the name of the group
async def template_command(ctx: lightbulb.SlashContext) -> None:
    pass

@template_command.set_error_handler
async def template_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    # The handler for if the bot command is on cooldown
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"We appreciate the enthusiasm\nBut the command is on cooldown!\nYou can use it again in {int(exception.retry_after)} seconds."
        )
        return True

# The name that'll show up when the bot loads the plugin
ext = "template"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
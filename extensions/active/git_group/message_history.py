from .git_group import git_group, git_plugin_name
from ....botlib.botlib import *
import lightbulb

# Refers to being a child from the def in the group assigner git
@git_group.child
@lightbulb.app_command_permissions(dm_enabled=True)
# enter the lines below this with options for the child if desired
# Adds a cooldown to the command
@lightbulb.add_cooldown(bucket=lightbulb.buckets.GuildBucket, length=5, uses=1)
@lightbulb.command("msghistory", "See all the messages in this guild that the bot can see")
# Its a "slash sub command" opposed to a slash command in a group
@lightbulb.implements(lightbulb.SlashSubCommand)
# The command its self. Change "git" to the name of the group
async def git_subcommand(ctx: lightbulb.SlashContext) -> None:
    
    await ctx.respond("I am a group child. Left in ./extensions as a example for future reference when making command groups.\nIf the bot is in production and you see me, a maintainer made a mistake and the issue will be resolved issue shortly.")
    botprint("WARNING! A git child was called! "+__name__)

@git_subcommand.set_error_handler
async def git_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    # The handler for if the bot command is on cooldown
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"We appreciate the enthusiasm\nBut the command is on cooldown!\nYou can use it again in {int(exception.retry_after)} seconds."
        )
        return True

# The name that'll show up when the bot loads the plugin
ext = f"{git_plugin_name}-childname"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
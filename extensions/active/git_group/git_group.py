# Defines if debug for the group is on or off
git_debug = False

import lightbulb
# defines the plugin
git_plugin_name = "git"
git_plugin = lightbulb.Plugin(git_plugin_name)
@git_plugin.command
# The title of the group and its description
@lightbulb.command("git", "A Command group which handles all data retrieval commands")
@lightbulb.implements(lightbulb.SlashCommandGroup)
# This is what you import V to use the group.child
async def git_group(_) -> None:
    pass  # as slash commands cannot have their top-level command run, we simply pass here

# Loads the plugin. (Not the other children to the plugin)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(git_plugin)
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(git_plugin)
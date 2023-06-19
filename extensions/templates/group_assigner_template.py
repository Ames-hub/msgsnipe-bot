# Defines if debug for the group is on or off
template_debug = False

import lightbulb
# defines the plugin
template_plugin_name = "template"
template_plugin = lightbulb.Plugin(template_plugin_name)
@template_plugin.command
# The title of the group and its description
@lightbulb.command("template", "a group assigner template")
@lightbulb.implements(lightbulb.SlashCommandGroup)
# This is what you import V to use the group.child
async def template_group(_) -> None:
    pass  # as slash commands cannot have their top-level command run, we simply pass here

# Loads the plugin. (Not the other children to the plugin)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(template_plugin)
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(template_plugin)
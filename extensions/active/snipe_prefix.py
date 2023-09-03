from ..botlib.botlib import *
import lightbulb
from ..botlib.datatables.new_msg_dt import dt as msg_dt

# Refers to being a child from the def in the group assigner template
@bot.command
@lightbulb.app_command_permissions(dm_enabled=False)
# enter the lines below this with options for the child if desired
# Adds a cooldown to the command
@lightbulb.add_cooldown(bucket=lightbulb.buckets.GuildBucket, length=5, uses=1)
@lightbulb.option(
    name="time",
    description="The time in seconds to snipe back to",
    type=hikari.OptionType.INTEGER,
    required=False
)
@lightbulb.command("snipe", "Get the last deleted message")
# Its a "slash sub command" opposed to a slash command in a group
@lightbulb.implements(lightbulb.PrefixCommand)
# The command its self. Change "template" to the name of the group
async def snipe_command(ctx: lightbulb.PrefixContext) -> None:

    if not os.path.exists(
        "data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/"
    ):
        os.makedirs("data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/")
        await ctx.respond("No messages to snipe? >.>")
        return

    try:
        time_threshold = ctx.options.time
        if time_threshold == None:
            time_threshold = 120
        else:
            time_threshold = int(time_threshold)
    except:
        time_threshold = 120

    msg_list = api.get.msg_list(
        guid=ctx.guild_id,
        chid=ctx.channel_id,
        time_threshold=time_threshold,
        deleted=True,
        created=False
    )

    message_list = []

    print(msg_list)
    if len(msg_list) == 0:
        await ctx.respond("No messages to snipe? >.>")
        return
    else:
        for msg in msg_list:

            msgd = {
                "content": msg[0],
                "author": msg[1],
                "time": msg[2],
            }

            # The embed that'll be sent
            await ctx.respond(
                "Sniped messages found! >:D",
            )
            for page in message_list:
                embed = hikari.Embed(
                    title="Sniped messages",
                    description="Here are the sniped messages",
                    color=0x00FF00
                )
                for msg in page:
                    embed.add_field(
                        name="Message",
                        value=msgd.content,
                        inline=False
                    )
                    embed.add_field(
                        name="Author",
                        value=msgd.author,
                        inline=False
                    )
                    embed.add_field(
                        name="Time",
                        value=msgd.time,
                        inline=False
                    )
                await ctx.respond(embed=embed)

@snipe_command.set_error_handler
async def template_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    # The handler for if the bot command is on cooldown
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            str(int(exception.retry_after))+" seconds until you can use this again.\nSorry!"
        )
        return True
    elif isinstance(exception, ValueError):
        await event.context.respond(
            "sorry, but a message couldn't be sniped due to time calculation errors"
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
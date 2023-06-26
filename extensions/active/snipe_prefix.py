from ..botlib.botlib import *
import lightbulb
from ..botlib.datatables.new_msg_dt import dt as msg_dt

time_threshold = 45

# Refers to being a child from the def in the group assigner template
@bot.command
@lightbulb.app_command_permissions(dm_enabled=False)
# enter the lines below this with options for the child if desired
# Adds a cooldown to the command
@lightbulb.add_cooldown(bucket=lightbulb.buckets.GuildBucket, length=5, uses=1)
@lightbulb.command("snipe", "Get the last deleted message")
# Its a "slash sub command" opposed to a slash command in a group
@lightbulb.implements(lightbulb.PrefixCommand)
# The command its self. Change "template" to the name of the group
async def snipe_command(ctx: lightbulb.PrefixContext) -> None:
    content_list = []
    authors = []
    time_stamps = []

    if not os.path.exists(
        "data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/"
    ):
        os.makedirs("data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/")
        await ctx.respond("No messages to snipe? >.>")
        return

    msg_list = os.listdir("data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/")

    for message in msg_list:
        jdir = "data/guilds/" + str(ctx.guild_id) + "/channels/" + str(ctx.channel_id) + "/deleted/" + message

        author_id = api.json.getvalue(
            dt=msg_dt,
            json_dir=jdir,
            key="author.uuid",
            default=None
        )

        if author_id == None:
            os.remove(jdir)
            continue

        # Validates and fetches time
        timestamp = api.json.getvalue(
            dt=msg_dt,
            json_dir=jdir,
            key="timestamp",
            default=None
        )
        del_timestamp = api.json.getvalue(
            dt=msg_dt,
            json_dir=jdir,
            key="del_timestamp",
            default=None
        )

        if timestamp or del_timestamp == None:
            os.remove(jdir)
            continue

        # Checks if the message is too old to be sniped
        if time.time() - del_timestamp > time_threshold:
            continue

        content = api.json.getvalue(
            dt=msg_dt,
            json_dir=jdir,
            key="content",
            default=None
        )

        if content == None:
            content = "No content detected!\n||Hint: We can't see images or embeds!||"

        authors.append(str(author_id))
        time_stamps.append(str(timestamp))
        content_list.append(content)

    formatted_snipes = []
    for author, timestamp, message in zip(authors, time_stamps, content_list):
        timenow = str(api.convert_time(timestamp))
        # This doesn't work for some reason.
        # Not gonna bother to figure it out. I am so tired 
        timenow.replace("_", " ")
        timenow.replace("-", "/")

        snipe_entry = "**<@" + author + "> | " + timenow + "**\n" + message + "\n\n"
        formatted_snipes.append(snipe_entry)

    if formatted_snipes:
        await ctx.respond(str(len(formatted_snipes)) + " Messages Sniped >:D")
        await ctx.respond("\n".join(formatted_snipes))
    else:
        await ctx.respond("No messages to snipe? >.>")

@snipe_command.set_error_handler
async def template_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    # The handler for if the bot command is on cooldown
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            str(int(exception.retry_after))+" seconds until you can use this again.\nSorry!"
        )
        return True
    # elif isinstance(exception, ValueError):
    #     await event.context.respond(
    #         "So sorry, but a message couldn't be sniped due to time calculation errors"
    #     )
    #     return True

# The name that'll show up when the bot loads the plugin
ext = "template"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
from ...botlib.botlib import *
import lightbulb

# Refers to being a child from the def in the group assigner template
@bot.command
@lightbulb.app_command_permissions(dm_enabled=True)
# enter the lines below this with options for the child if desired
# Adds a cooldown to the command
@lightbulb.add_cooldown(bucket=lightbulb.buckets.GuildBucket, length=5, uses=1)
@lightbulb.command("apisnipe", "Fetch a series of deleted messages")
# Its a "slash sub command" opposed to a slash command in a group
@lightbulb.implements(lightbulb.PrefixCommand)
# The command its self. Change "template" to the name of the group
async def snipe_command(ctx: lightbulb.PrefixContext) -> None:
    
    # As this is a API command, Only bots can use it
    if not ctx.user.is_bot:
        return
    
    content = str(ctx.event.content)

    split_content = content.split(" ")
    # Finds the guild_id
    for word in split_content:
        if "guild:" in str(word):
            guild_id = word.replace("guild:", "")
            for char in guild_id:
                if str(char).isnumeric() == False:
                    guild_id = None
                    break

    # Finds the channel_id
    for word in split_content:
        if "channel:" in str(word):
            channel_id = word.replace("channel:", "")
            for char in channel_id:
                if str(char).isnumeric() == False:
                    channel_id = None
                    break

    # Finds the time threshold
    for word in split_content:
        if "time:" in word:
            time_threshold = word.replace("time:", "")
            for char in time_threshold:
                if str(char).isnumeric() == False:
                    time_threshold = None
                    break

    # Finds the time threshold
    for word in split_content:
        if "mention:" in word:
            word = word.replace("mention:", "").lower()
            if word == "true":
                mention = True
                break
            elif word == "false":
                mention = False
                break
    else:
        mention = False
    

    try:
        if guild_id == None:
            await ctx.respond("Missing guild id")
            return
    except UnboundLocalError:
        await ctx.respond("Missing guild id")
        return
    try:
        if channel_id == None:
            await ctx.respond("Missing channel id") # Verifies all required arguments are present
            return
    except UnboundLocalError:
        await ctx.respond("Missing channel id")
    try:
        if channel_id == None and guild_id == None:
            await ctx.respond("Missing guild and channel id")
            return
    except UnboundLocalError:
        await ctx.respond("Missing guild and channel id")
        return

    try:
        time_threshold # Checks if time_threshold is defined or not
    except UnboundLocalError:
        time_threshold = 120

    # Gets the full history of deleted messages
    returned_list = api.get.msg_list(
        guid=guild_id,
        chid=channel_id,
        time_threshold=time_threshold
    )
    
    # unpacks the list
    content_list = returned_list[0]
    author_list = returned_list[1]
    time_stamps = returned_list[2]

    del returned_list

    # If there are no messages to snipe, return
    if len(author_list) == 0:
        await ctx.respond("None")
        return
    
    # else, send the messages
    def _format_msgs(author_list, content_list, time_stamps):
        for i in range(len(author_list)):
            if mention == False:
                yield "author:'"+author_list[i]+"' time_stamp:'"+str(time_stamps[i])+"' content:"+content_list[i]
            elif mention == True:
                yield "author:'<@!"+author_list[i]+">' time_stamp:'"+str(time_stamps[i])+"' content:"+content_list[i]+" mention:"+author_list[i]

    await ctx.respond("\n".join(_format_msgs(author_list, content_list, time_stamps)))

@snipe_command.set_error_handler
async def template_error_handler(event: lightbulb.CommandErrorEvent):
    exception = event.exception.__cause__ or event.exception
    # The handler for if the bot command is on cooldown
    if isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            str(int(exception.retry_after))+" seconds until you can use this again.\nSorry!"
        )
        return True
    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond("Missing Arguments\n"+ str(exception.missing_options))
    # elif isinstance(exception, ValueError):
    #     await event.context.respond(
    #         "So sorry, but a message couldn't be sniped due to time calculation errors"
    #     )
    #     return True

# The name that'll show up when the bot loads the plugin
ext = "api_snipe"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
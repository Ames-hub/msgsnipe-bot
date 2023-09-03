from ...botlib.botlib import *
import lightbulb

@bot.listen()
async def snipe_command(ctx: hikari.MessageCreateEvent) -> None:

    if ctx.content.startswith("#apisnipe") == False:
        return

    content = str(ctx.content)

    if not ctx.is_bot and ctx.author.id != 913574723475083274 and "debug" not in content.lower():
        await ctx.message.respond("Only bots can access this command")
        return
    elif ctx.author.is_bot and "debug" in content.lower():
        await ctx.message.respond("Debug access denied")
        return
    
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
            await ctx.message.respond("Missing guild id\nSyntax: ``guild:(guild_id)``")
            return
    except UnboundLocalError:
        await ctx.message.respond("Missing guild id\nSyntax: ``guild:(guild_id)``")
        return
    try:
        if channel_id == None:
            await ctx.message.respond("Missing channel id\nSyntax: ``channel:(channel_id)``") # Verifies all required arguments are present
            return
    except UnboundLocalError:
        await ctx.message.respond("Missing channel id\nSyntax: ``channel:(channel_id)``")
        return
    try:
        if channel_id == None and guild_id == None:
            await ctx.message.respond("Missing guild and channel id")
            return
    except UnboundLocalError:
        await ctx.message.respond("Missing guild and channel id")
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
    if returned_list == "ERR: INVALID TIME THRESHOLD":
        await ctx.message.respond("Invalid time threshold")
    
    # unpacks the list
    content_list = returned_list[0]
    author_list = returned_list[1]
    time_stamps = returned_list[2]

    del returned_list

    # If there are no messages to snipe, return
    if len(author_list) == 0:
        await ctx.message.respond("None")
        return
    
    # else, send the messages
    def _format_msgs(author_list, content_list, time_stamps):
        for i in range(len(author_list)):
            if mention == False:
                yield "author:'"+author_list[i]+"' time_stamp:'"+str(time_stamps[i])+"' content:'"+content_list[i]+"'"
            elif mention == True:
                yield "author:'<@!"+author_list[i]+">' time_stamp:'"+str(time_stamps[i])+"' uuid:"+author_list[i]+" content:'"+content_list[i]+"'"

    await ctx.message.respond(list(_format_msgs(author_list, content_list, time_stamps)))

# The name that'll show up when the bot loads the plugin
ext = "api_snipe"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
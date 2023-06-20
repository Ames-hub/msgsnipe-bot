'''
This task deletes all old recorded messages from the database
As these messages will accumulate, and eventually take up a fuck ton of storage.

So to prevent that, I am making it delete all 14 day old messages
'''

testing = False
if testing == False:
    del_duration = 1,209,600 # 14 days of seconds to calc with time.time()
else:
    del_duration = 10

from ..botlib.botlib import *

@tasks.task(m=1, wait_before_execution=True, auto_start=True)
async def undefined_task():
    botprint("deleting all old messages")

    del_count = 0

    guild_list = os.listdir("data/guilds/")
    for guild in guild_list: # each guild will be a folder
        guild = str(guild)
        channel_list = os.listdir("data/guilds/"+guild+"/channels/")
        for channel in channel_list:
            channel = str(channel)
            msg_list = os.listdir("data/guilds/"+guild+"/channels/"+channel+"/")
            for message in msg_list:
                time_sent = api.json.getvalue(
                    key="timestamp",
                    json_dir="data/guilds/"+guild+"/channels/"+channel+"/created/"+message+".json",
                    default=time.time(),
                )

                if time.time() - time_sent >= del_duration:
                    os.remove("data/guilds/"+guild+"/channels/"+channel+"/created/"+message+".json")
                    del_count += 1
    else:
        botprint("deleted "+str(del_count)+" created messages")

    for guild in guild_list: # each guild will be a folder
        guild = str(guild)
        channel_list = os.listdir("data/guilds/"+guild+"/channels/")
        for channel in channel_list:
            channel = str(channel)
            msg_list = os.listdir("data/guilds/"+guild+"/channels/"+channel+"/")
            for message in msg_list:
                time_sent = api.json.getvalue(
                    key="timestamp",
                    json_dir="data/guilds/"+guild+"/channels/"+channel+"/deleted/"+message+".json",
                    default=time.time(),
                )

                if time.time() - time_sent >= del_duration:
                    os.remove("data/guilds/"+guild+"/channels/"+channel+"/deleted/"+message+".json")
                    del_count += 1
    else:
        botprint("deleted "+str(del_count)+" created messages")

# The name that'll show up when the bot loads the plugin
ext = "delete_old"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
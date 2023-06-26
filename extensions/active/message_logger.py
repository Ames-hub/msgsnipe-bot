from ..botlib.botlib import *
from ..botlib.datatables.new_msg_dt import dt as msg_dt

@bot.listen()
# Msg create can determine the author of the msg, the content, and the channel it was sent in for when the message is deleted
async def msg_create(event: hikari.events.GuildMessageCreateEvent):

    # As users cannot send embeds, do not handle embeds in this code.
    if event.message.author.is_bot or event.message.author.is_system:
        return
    
    api.json.getvalue( # Getvalue is used to create the file if it does not exist (Not intended purpose)
        dt=msg_dt,
        json_dir="data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/test.json",
        key="NotActuallyAKey",
    )
    os.remove("data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/test.json")

    # Determines the msg id
    #msg_id = 
    msg_id = event.message.id
    msg_id = str(msg_id)
    
    try:
        content = str(event.message.content)
    except:
        content = "Unknown Content?"

    jdir = "data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/"+msg_id+".json"

    if content == None:
        print(content)
        content = "Unknown Content?"

    api.json.setvalue(
        dt=msg_dt,
        json_dir=jdir,
        key="id",
        value=str(len(os.listdir("data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/")) + 1),
    )
    api.json.setvalue(
        dt=msg_dt,
        json_dir=jdir,
        key="content",
        value=content,
    )
    api.json.setvalue(
        dt=msg_dt,
        json_dir=jdir,
        key="event_channel",
        value=str(event.message.channel_id),
    )
    api.json.setvalue(
        dt=msg_dt,  
        json_dir=jdir,
        key="author.uuid",
        value=str(event.message.author.id),
    )
    api.json.setvalue(
        dt=msg_dt,
        json_dir=jdir,
        key="timestamp",
        value=time.time(),
    )

@bot.listen()
# Msg create can determine the author of the msg, the content, and the channel it was sent in for when the message is deleted
async def msg_delete(event: hikari.events.GuildMessageDeleteEvent):
    author_id = api.json.getvalue(
        dt=msg_dt,
        # created is correct. its fetching an old message logged
        json_dir="data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/"+str(event.message_id)+".json",
        key="author.uuid",
        default=None
    )

    # if Author ID is None, then the msg was not logged.
    if author_id == None:
        return False
    else:
        author_id = str(author_id)
    
        if not os.path.exists("data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/deleted/"):
            os.makedirs("data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/deleted/", exist_ok=True)

        api.json.setvalue(
            dt=msg_dt,
            json_dir="data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/"+str(event.message_id)+".json",
            key="del_timestamp",
            value=time.time(),
        )
        # Move instead of copy to save space on the disk
        shutil.move(
            src="data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/created/"+str(event.message_id)+".json",
            dst="data/guilds/"+str(event.guild_id)+"/channels/"+str(event.channel_id)+"/deleted/"+str(event.message_id)+".json",
            )

# The name that'll show up when the bot loads the plugin
ext = "Message Logger"
# loads the plugin (REQUIRED OR THE BOT WILL CRASH)
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lightbulb.Plugin(ext))
# Unloads the plugin. (Not the other children to the plugin)
def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
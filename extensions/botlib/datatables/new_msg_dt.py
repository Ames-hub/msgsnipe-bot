import time
dt = {
    # ID = how many msg's the bot has seen from this user
    "id": None,
    "content": None,
    "event_channel": None,
    # Set A time just incase it isn't logged in the msg_create event
    "timestamp": time.time(),
    "del_timestamp": None, # When the msg was deleted (if it was deleted)
    "author": {
        "uuid": None,
    }
}
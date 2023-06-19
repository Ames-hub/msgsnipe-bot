import time
dt = {
    # ID = how many msg's the bot has seen from this user
    "id": None,
    "content": None,
    "event_channel": None,
    # Set A time just incase it isn't logged in the msg_create event
    "timestamp": time.time(),
    "author": {
        "uuid": None,
    }
}
# msgsnipe-bot
a discord message sniping bot, much like how Dank memer was capable of doing so.

Prefix: #
Commands:
1. snipe

# API
This bot has a basic API.
This is the command that is used (Prefix command)

apisnipe guild:1057496622138929172 channel:1119693252401049660 time:1200
Lets break this down
``
#apisnipe
``
This calls the API section of the bot
``
guild:''
``
This section 'guild' refers to which guild to fetch deleted messages from
``
channel
``
Pretty simple. refers to which channel in THAT Guild to fetch from
``
time
``
Again, simple. How many seconds in the past should we look back for? 60? 120? 1200? It can be any number

Support server: https://discord.gg/HkKAsgvCzt

# Installation
1. Install python 3.11
2. Setup a venv
```
python3.11 -m venv venv
```
3. Activate the venv
```
source venv/bin/activate on linux, or venv\scripts\activate on windows
```
4. Install the requirements
```
pip install -r requirements.txt
```
5. Run the bot
```
python3.11 -O bot.py
```

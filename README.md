# msgsnipe-bot
a discord message sniping bot, much like how Dank memer was capable of doing so.

Prefix: #
Commands:
1. snipe

# API
This bot has a basic API.<br>
This is the command that is used (Prefix command) to call on a function of the API<br>

apisnipe guild:1057496622138929172 channel:1119693252401049660 time:1200<br><br>
Lets break this down<br>
``
#apisnipe
``
This calls the API section of the bot<br>
``
guild:
``
This section 'guild' refers to which guild to fetch deleted messages from<br>
``
channel:
``
Pretty simple. refers to which channel in THAT Guild to fetch from<br>
``
time:
``
Again, simple. How many seconds in the past should we look back for? 60? 120? 1200? It can be any number<br>

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

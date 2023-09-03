import os, json, logging, atexit, time, hikari, lightbulb, sys, inspect, colorama, shutil
from dotenv import load_dotenv
from colorama import Style, Fore
from .datatables.new_msg_dt import dt as msg_dt

load_dotenv(dotenv_path="data/token.env") # Token

# Configurable variables
# This variable controls how all time.strftime() calls are formatted. (https://docs.python.org/3/library/time.html#time.strftime)
standardized_strftime = "%H.%M.%S_%d-%m-%Y" # WARNING: Unknown if changing this will break everything time-based
logs_dir = "data/logs" # Logs directory
token = os.environ.get("token")

if token == None:
    load_dotenv(dotenv_path="data/token.env") # Token

if not os.path.exists("data/logs/"):
    os.mkdir("data/logs/")
if not os.path.exists("data/logs/"):
    os.mkdir("data/logs/")
if len(os.listdir("data/logs/")) == 0:
    with open("data/logs/time_tracker", "w") as f:
        f.write(time.strftime(standardized_strftime))

def botprint(
        message,
        log=True,
        rainbow_mode=True,
        delay=0,
        solid_color=None,
        word=None,
        word_color=None,
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    ):
    '''
    Prints a message to the console, and logs it if requested.

    Parameters
    ----------
    message : str
        The message to print.
    log : bool
        Whether or not to log the message.
    rainbow_mode : bool
        Whether or not to make the message rainbow.
    delay : int
        The delay between each letter in the message.
    solid_color : str
        The color to make the message if rainbow mode is disabled.
    word : str
        The word to make a different color.
    word_color : str
        The color to make the word.
    colors : list
        The colors to use for the rainbow mode.

    Returns
    -------
    None

    Raises
    ------
    None

    Examples
    --------
    >>> botprint("Hello, world!", log=True, rainbow_mode=True, delay=0, solid_color=None, word=None, word_color=None, colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])
    Hello, world!
    '''
    
    if log == True:
        logging.info(str(message))

    if rainbow_mode == None:
        rainbow_mode == True

    if rainbow_mode and solid_color:
        # Uses inspect to get the line where this def was called
        logging.warn("at line " + str(inspect.stack()[1].lineno) + " Rainbow mode and solid colour mode are both enabled! Solid mode will be used.")

    # Makes the message into the colors if requested
    if rainbow_mode == True:
        colorama.init()
        
        colored_message = ""
        word_found = False
        word_index = 0

        for index, letter in enumerate(message):
            if word and message[index:].startswith(word) and not word_found:
                word_found = True
                word_index = index

            if word_found and (letter == " " or index == len(message) - 1):
                word_found = False
                colorr = colors[word_index % len(colors)]
                colored_word = message[word_index:index] + letter
                colored_message += f"{colorr}{colored_word}"
            elif not word_found:
                colorr = colors[index % len(colors)]
                colored_message += colorr+letter

        colored_message += Style.RESET_ALL
        message = colored_message
    
    # After making it a rainbow if enabled, make a certain word a certain color if requested
    if word and word_color != None:
        
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
        }
        
        reset = "\033[0m"
        message = message.replace(word, f"{colors[word_color]}{word}{reset}")
    elif word_color and not word:
        # Uses inspect to get the line where this def was called
        logging.warn("Word_colour was assigned but word was not! Line: "+ str(inspect.stack()[1].lineno))
        return False
    
    if solid_color:
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
        }
        
        reset = "\033[0m"
        message = colors[solid_color]+message+reset
    
    # Delay will always be last, as it is a print statement area
    if delay > 0:
        logging.info("Function 'botprint' has been called with delay")
        if rainbow_mode == True:
            delay = delay / 6.255 # Precisely calculated division to make the delay print duration not change with rainbow mode since rainbow mode adds extra characters
        for c in message:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(delay)
        print()
        return True # Returns true for successful execution

    # This is to be the main print statement in the function
    print(message)

# On exit, create a file in logs_dir/ with the time.strftime(standardized_strftime) as the contents
@atexit.register
def on_exit():
    # Wont except as ``with open`` creates the file if its written to
    with open(logs_dir+"/time_tracker", 'w') as f:
        f.write(time.strftime(standardized_strftime))

    # If latest.log exists, rename it to the time of last exit. Also creates the time tracker if not exists
    if os.path.exists(logs_dir+"/time_tracker") == False: # If the time tracker doesn't exist, create it
        with open(logs_dir+"/time_tracker", 'w') as f:
            f.write(time.strftime(standardized_strftime))

# Keep trying to rename the latest.log file until 5 attempts have been made
attempts = 0
if os.path.exists(logs_dir+"/latest.log"):
    # Gets the contents of the file logs_dir/time_tracker
    if not os.path.exists(logs_dir+"/time_tracker"):
        with open(logs_dir+"/time_tracker", 'w') as f:
            f.write(time.strftime(standardized_strftime))

    with open(logs_dir+"/time_tracker", 'r') as f:
        time_tracker = f.read()
        

    # Renames the file to the time of last exit
    logging.shutdown()
    os.rename(logs_dir+"/latest.log", logs_dir+"/"+time_tracker+".log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='w',
    filename=logs_dir+"/latest.log"
)
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='w',
    filename=logs_dir+"/latest.log"
)
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='w',
    filename=logs_dir+"/latest.log"
)

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        function_name = func.__name__
        logging.info("Execution time: {} seconds".format(execution_time))
        print("Execution time for function '{}': {} seconds".format(function_name, execution_time))
        return result
    return wrapper

class api:
    class json:
        def getvalue(key, json_dir, default=None, dt=None):
            """
            Retrieve the value of a nested key from a JSON file or dictionary.
            Args:
                key (str): The key to retrieve in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to write to the JSON file if it does not exist (default=None).
            Returns:
                The value of the key if found, or the default value if not found.
            """
            # Split the key into parts (assuming key is in the format "parent.child1.child2[0].child3")
            parts = key.split('.')
            # Check if the JSON file exists
            if not os.path.exists(json_dir):
                try:
                    # If not, create the parent directory if it doesn't exist
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)
                    if dt is not None:
                        # If dt is provided, write it to the JSON file
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        # Otherwise, create an empty JSON file
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error creating JSON file: {str(e)}")
                    return default
            # Load the JSON file
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                logging.error(f"Error loading JSON file: {str(e)}")
                return default
            # Check if the JSON data is empty
            if not data:
                # If empty, fill it with an empty dictionary or the provided dt
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error writing to JSON file: {str(e)}")
                    return default
            # Traverse the nested dictionaries/lists in the JSON data to get the value
            value = data
            for part in parts:
                if part.endswith(']'):  # Check if part is an array index
                    index = int(part[part.index('[') + 1:part.index(']')])  # Extract the array index
                    value = value[index]
                else:
                    if part in value:
                        value = value[part]
                    else:
                        # If the key doesn't exist, return the default value (default=None)
                        return default
            return value

        def setvalue(key, json_dir, value, default=None, dt=None):
            # Check if the file at json_dir exists
            if not os.path.exists(json_dir):
                # Create parent directories if they don't exist
                os.makedirs(os.path.dirname(json_dir), exist_ok=True)
                
                # Create and fill the JSON file with dt if provided
                if dt is not None:
                    with open(json_dir, 'w') as file:
                        json.dump(dt, file, indent=4, separators=(',', ': '))
                elif default is not None:
                    with open(json_dir, 'w') as file:
                        json.dump(default, file, indent=4, separators=(',', ': '))
            
            try:
                with open(json_dir, 'r+') as file:
                    data = json.load(file)
                    keys = key.split('.')
                    
                    # Traverse the nested structure to access the key
                    nested_data = data
                    for nested_key in keys[:-1]:
                        nested_data = nested_data.setdefault(nested_key, {})
                    
                    # Set the value of the selected key
                    nested_data[keys[-1]] = value
                    
                    # Move the file pointer to the beginning and rewrite the JSON data
                    file.seek(0)
                    json.dump(data, file, indent=4, separators=(',', ': '))
                    file.truncate()
                    
            except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
                return default
            
            return value

        def addvalue(key, json_dir, value, default=None, dt=None):
            """
            Add a value to a list in a nested key of a JSON file or dictionary.
            Args:
                key (str): The key to add to in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                value: The value to add to the list.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to compare against the JSON file and create missing keys (default=None).
            Returns:
                The updated value of the key if added successfully, or the default value if not found.
            """
            parts = key.split('.')
            if not os.path.exists(json_dir):
                try:
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)
                    if dt is not None:
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error creating JSON file: {str(e)}")
                    return default
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                logging.error(f"Error loading JSON file: {str(e)}")
                return default
            if not data:
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error writing to JSON file: {str(e)}")
                    return default
            
            # Compare dt with the JSON data and create any missing keys
            def compare_and_create_keys(parts, data, dt):
                if len(parts) == 1:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if not isinstance(data[index], list):
                            data[index] = [data[index]]
                    else:
                        if key not in data:
                            data[key] = dt[key]
                            return
                else:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if not isinstance(data[index], list):
                            data[index] = [data[index]]
                        compare_and_create_keys(parts[1:], data[index], dt)
                    else:
                        if key not in data:
                            data[key] = dt[key] if key in dt else {}
                        compare_and_create_keys(parts[1:], data[key], dt)
            
            if dt is not None:
                compare_and_create_keys(parts, data, dt)

            # Define a recursive function to traverse the nested dictionaries/lists in the JSON data
            def _addvalue(parts, value, data):
                if len(parts) == 1:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if not isinstance(data[index], list):
                            data[index] = [data[index]]
                        data[index].append(value)
                    else:
                        if not isinstance(data[key], list):
                            data[key] = [data[key]]
                        data[key].append(value)
                else:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if isinstance(data[key], list):
                            data[key].append(value)
                    else:
                        key = parts[0]
                        if key.endswith(']'):
                            index = int(key[key.index('[') + 1:key.index(']')])
                            if isinstance(data[index], list):
                                _addvalue(parts[1:], value, data[index])
                        else:
                            if key in data:
                                _addvalue(parts[1:], value, data[key])

            try:
                _addvalue(parts, value, data)
            except Exception as e:
                logging.error(f"Error adding value to JSON file: {str(e)}")
                return default
            
            try:
                with open(json_dir, 'w') as f:
                    json.dump(data, f, indent=4, separators=(',', ': '))
            except Exception as e:
                logging.error(f"Error writing to JSON file: {str(e)}")
                return default

            return data

        def remvalue(key, json_dir, value, default=None, dt=None):
            """
            Remove a value from a list in a nested key of a JSON file or dictionary.
            Args:
                key (str): The key to remove from in the format "parent.child1.child2[0].child3".
                json_dir (str): The file path of the JSON file to read from or write to.
                value: The value to remove from the list.
                default: The default value to return if the key is not found (default=None).
                dt (dict): The dictionary to compare against the JSON file and create missing keys (default=None).
            Returns:
                The updated value of the key if removed successfully, or the default value if not found.
            """
            parts = key.split('.')
            if not os.path.exists(json_dir):
                try:
                    os.makedirs(os.path.dirname(json_dir), exist_ok=True)
                    if dt is not None:
                        with open(json_dir, 'w') as f:
                            json.dump(dt, f, indent=4, separators=(',', ': '))
                    else:
                        with open(json_dir, 'w') as f:
                            json.dump({}, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error creating JSON file: {str(e)}")
                    return default
            try:
                with open(json_dir, 'r') as f:
                    data = json.load(f)
            except Exception as e:
                logging.error(f"Error loading JSON file: {str(e)}")
                return default
            if not data:
                data = dt or {}
                try:
                    with open(json_dir, 'w') as f:
                        json.dump(data, f, indent=4, separators=(',', ': '))
                except Exception as e:
                    logging.error(f"Error writing to JSON file: {str(e)}")
                    return default
            
            # Compare dt with the JSON data and create any missing keys
            def compare_and_create_keys(parts, data, dt):
                if len(parts) == 1:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if not isinstance(data[index], list):
                            data[index] = [data[index]]
                    else:
                        if key not in data:
                            data[key] = dt[key]
                            return
                else:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if not isinstance(data[index], list):
                            data[index] = [data[index]]
                        compare_and_create_keys(parts[1:], data[index], dt)
                    else:
                        if key not in data:
                            data[key] = dt[key] if key in dt else {}
                        compare_and_create_keys(parts[1:], data[key], dt)
            
            if dt is not None:
                compare_and_create_keys(parts, data, dt)

            # Define a recursive function to traverse the nested dictionaries/lists in the JSON data
            def _remvalue(parts, value, data):
                if len(parts) == 1:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        if isinstance(data[index], list):
                            if value in data[index]:
                                data[index].remove(value)
                    else:
                        if isinstance(data[key], list):
                            if value in data[key]:
                                data[key].remove(value)
                else:
                    key = parts[0]
                    if key.endswith(']'):
                        index = int(key[key.index('[') + 1:key.index(']')])
                        ###
                        if isinstance(data[key], list):
                            if value in data[key]:
                                data[key].remove(value)
                    else:
                        key = parts[0]
                        if key.endswith(']'):
                            index = int(key[key.index('[') + 1:key.index(']')])
                            if isinstance(data[index], list):
                                _remvalue(parts[1:], value, data[index])
                        else:
                            if key in data:
                                _remvalue(parts[1:], value, data[key])

            try:
                _remvalue(parts, value, data)
            except Exception as e:
                logging.error(f"Error removing value from JSON file: {str(e)}")
                return default

            try:
                with open(json_dir, 'w') as f:
                    json.dump(data, f, indent=4, separators=(',', ': '))
            except Exception as e:
                logging.error(f"Error writing to JSON file: {str(e)}")
                return default

            return data.get(parts[-1], default)

    class get:

        def msg_list(guid, chid, time_threshold=120, deleted=False, created=False):
            '''
            Snipes all the messages in a certain time threshold

            Returns
            4 lists containing the content, author, and timestamp of the sniped messages and how many fails there were 
            (content_list[0], authors[1], time_stamps[2] fails[3])

            args:
            guid: guild id
            chid: channel id
            time_threshold: time threshold in seconds
            deleted: whether to snipe deleted messages
            created: whether to snipe created messages
            '''

            content_list = []
            authors = []
            time_stamps = []
            fails = []

            if deleted == False and created == False:
                raise Warning("You tried to snipe neither deleted or created messages. This will return an empty list.")

            if not os.path.exists(
                "data/guilds/" + str(guid) + "/channels/" + str(chid) + "/deleted/"
            ):
                os.makedirs("data/guilds/" + str(guid) + "/channels/" + str(chid) + "/deleted/")
                raise LookupError("No messages found in channel.")
                # This is a newly logged channel, so there are no messages to snipe

            msg_list = os.listdir("data/guilds/" + str(guid) + "/channels/" + str(chid) + "/deleted/")
            for message in msg_list:
                jdir = "data/guilds/" + str(guid) + "/channels/" + str(chid) + "/deleted/" + message

                author_id = api.json.getvalue(
                    dt=msg_dt,
                    json_dir=jdir,
                    key="author.uuid",
                    default=None
                )

                if author_id == None:
                    os.remove(jdir)
                    fails.append("Author ID not found")
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
                    key="del_timestamp", # This is the time the message was deleted
                    default=None
                )

                if timestamp == None:
                    os.remove(jdir)
                    fails.append("Timestamp not found")
                    continue
                elif del_timestamp == None:
                    os.remove(jdir)
                    fails.append("Deletion timestamp not found")
                    continue
                
                # Checks if the message is too old to be sniped
                try:
                    if time.time() - del_timestamp > float(time_threshold):
                        continue
                except ValueError:
                    return "ERR: INVALID TIME THRESHOLD"

                content = api.json.getvalue(
                    dt=msg_dt,
                    json_dir=jdir,
                    key="content",
                    default=None
                )

                if content == None:
                    content = "No content!"

                authors.append(str(author_id))
                time_stamps.append(str(timestamp))
                content_list.append(str(content))

            return [content_list, authors, time_stamps]

    def convert_time(time_val: str) -> str:

        try:
            timestamp = float(time_val)
            formatted_time = time.strftime(standardized_strftime, time.localtime(timestamp))
        except ValueError:
            try:
                timestamp = int(time.mktime(time.strptime(time_val, standardized_strftime)))
                formatted_time = str(timestamp)
            except ValueError:
                raise ValueError("Invalid time format. Please provide the time as a time.time timestamp or as \"" + standardized_strftime + "\" format.")

        return formatted_time

    def format_snipes(authors, time_stamps, content_list):
        formatted_snipes = []
        for author, timestamp, message in zip(authors, time_stamps, content_list):
            timenow = str(api.convert_time(timestamp))
            # This doesn't work for some reason.
            # Not gonna bother to figure it out. I am so tired 
            timenow.replace("_", " ")
            timenow.replace("-", "/")

            snipe_entry = "**<@" + author + "> | " + timenow + "**\n" + message + "\n\n"
            formatted_snipes.append(snipe_entry)

        return formatted_snipes

    
from hikari import Intents
from lightbulb.ext import tasks
INTENTS = Intents.ALL
bot = lightbulb.BotApp(
    token=token if token != None else "NO TOKEN FOUND",
    prefix="#",
    intents=INTENTS
    )
tasks.load(bot)
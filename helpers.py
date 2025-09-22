import time
import os
from rich import print
from datetime import datetime

def stopwatch():
    """
    Magically makes a timer in seconds which you can then use to measure time taken.
    """
    return time.monotonic()

def log(message: str, type: int, log_in_file: bool = False):
    """
    Logs a message in the console using rich to make the messsage types clearer.

    ### Types:
        0 SUCCES
        1 INFO
        2 WARNING
        3 ERROR
    ### Takes:
        message: str = The message you want to log
        type: int = The type of the message (1 - 4)
        log_in_file: bool = if you would like to log it in a log.txt file
    ### Returns:
        None
    """
    log_path = "log.txt"
    time = datetime.now().strftime("%d-%m-%Y %H:%M")

    types = [
        f"[b][green][SUCCES][/b]",
        f"[b][#f2c041][INFO][/b]",
        f"[b][#25515][WARNING][/b]",
        f"[b][red][ERROR][/b]"
    ]

    styled_message = fr"[white]{time}[/white] | {types[type]} {message}"

    if log_in_file:
        # Log the message in a txt file
        if not os.path.exists(log_path):
            with open(log_path, "x"): # Create the log file
                pass
        
        with open(log_path, "a") as file:
            file.write(styled_message + "\n")
    
    print(styled_message)
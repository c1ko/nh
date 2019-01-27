#!/usr/bin/env python3
import os, readline, sys

NH_HOME = os.environ["HOME"] + "/.nh"
ACTION_FILE = NH_HOME + "/action"

# Credit to https://stackoverflow.com/questions/8505163
def input_with_prefill(text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    
    readline.set_pre_input_hook(hook)
    result = input()
    readline.set_pre_input_hook()
    return result

with open(ACTION_FILE, "r") as action_file:
	action = action_file.read()

try:
	result = input_with_prefill(action)
except KeyboardInterrupt: 
	sys.exit(0) #Allow to end the programm with STRG+C without throwing an exception

with open(ACTION_FILE, "w") as action_file:
	action_file.write(result)

sys.exit(10)

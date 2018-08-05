from getpass import getpass
from colors import *
import pyperclip
import time
import sys

def safe_getpass(display_string):
    try:
        password = getpass(display_string + " ")
        return password
    except EOFError:
        return -1

def safe_input(display_string):
    try:
        text = input(display_string + " ")
        return text
    except EOFError as EOF:
        return -1 

def sensitive_on_screen(pwd):
    print(RED,"Password:",RESET,REVERSE,pwd,RESET)
    tmp = pyperclip.paste()
    pyperclip.copy(pwd)
    print("Password copied to clipboard for 10 seconds")
    print("The data will be erased in 10 seconds")
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)
    print(chr(27) + "[2J") # clear screen
    pyperclip.copy(tmp)

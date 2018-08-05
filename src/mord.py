from mord_crypto import *
from colors import *
from mord_utils import *
from getpass import getpass
from Databse import Database
import pyperclip
import sys
import time
import password_generator
import os
import yaml



def add(db):
    entry = dict()
    name = safe_input('name:')
    username = safe_input('Username:')
    if len(username) == 0:
        print('Cancelling add of new item')
        return
    entry['username'] = username
    decision = safe_input('Want to strong generated password?')
    password = ''
    if 'yes' in decision or 'y' in decision:
        password = password_generator.generate_passphrase(5)
    else:
        password = safe_getpass('Password:')

    if len(password) == 0:
        print('Cancelling add of new item')
        return
    entry['password'] = password

    url = safe_input('url:')
    if len(url) == 0:
        print('Cancelling add of new item')
        return
    entry['url'] = url

    extra = safe_input('extra:')
    if len(extra) == 0:
        print('Cancelling add of new item')
        return
    entry['extra'] = extra

    grouping = safe_input('grouping:')
    if len(grouping) == 0:
        print('Cancelling add of new item')
        return
    entry['grouping'] = grouping

    fav  = safe_input('fav:')
    if len(fav) == 0:
        print('Cancelling add of new item')
        return
    entry['fav'] = fav

    # Check for existing
    db.add(entry,name)

def gen_passphrase_helper(db):
    string = safe_input('number of words(default 5): ')
    num = 0
    if string is '':
        pwd = password_generator.generate_passphrase()
        sensitive_on_screen(pwd)
        return
    try:
        num = int(string)
        pwd = password_generator.generate_passphrase(num)
        sensitive_on_screen(pwd)
        return
    except ValueError:
        print('Please enter a number')
        gen_passphrase_helper(db)


def handle_reponses(arg, db):
    if arg == '1' or arg == 'find' or arg == 'f':
        return find_app(db)
    elif arg == '2' or arg == 'add' or arg == 'a':
        return add(db)
    elif arg == '3' or arg == 'exit' or arg == 'e':
        raise EOFError
    elif arg == '5' or arg == 'gen' or arg == 'g':
        return gen_passphrase_helper(db)
    elif arg == '6' or arg == 'list' or arg == 'l':
        db.get_keys()



def run_mord(db):
    while True:
        try:
            print('Choose action:')
            text = safe_input('find [1], add [2], exit [3], generate'+
                    'passphrase [5], list entries [6]:')
            handle_reponses(text, db)
        except EOFError as EOF:
            return

def find_app(db):
    try:
        text = safe_input('Enter application name:')
    except EOFError as EOF:
        return
    try:
        data = db.find(text)
        if not data:
            print(text, 'is not in the database')
            return
        print(GREEN,'Username:',data['username'],RESET)
        print(BLUE,'Url:',data['url'],RESET)
        print(CYAN,'Extra:',data['extra'],RESET)
        print(REVERSE,'Fav:',data['fav'],RESET)
        print(CYAN,'Grouping:',data['fav'],RESET)
         # restores cursor position and attributes
        sensitive_on_screen(data['password'])
        return
    except KeyError as ke:
        print(text, 'is not in the db')
        return



def get_database(ifp,pwd):
    stream = decrypt(ifp,pwd)
    db = dict()
    try:
        db = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        return None
    except UnicodeDecodeError as ude:
        print('Incorrect pwd!')
        return None
    return

def initialize_db():
    path = os.getenv('MORD_HOME', '')
    db_location = path+'/.db'
    try:
        return Database(db_location)
    except EOFError as eof:
        return None

def main():
    db = initialize_db()
    if(db == None):
        print('There seems to be an error with the db')
        return
    run_mord(db)
    db.save()

if __name__ == '__main__':
    main()

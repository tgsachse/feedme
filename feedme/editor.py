#! /usr/bin/env python3
#REMOVE ME PLEASE
import mitu
from mitu import confirm_input, rinput, rprint
import re
import os
import math
import shutil
import random
import sqlite3 as sql

#######TEMPORARY, will be removed###############################################
def TEMPORARY_POPULATE_DATABASE():
    try:
        db = sql.connect('data/PapaJohns.db')
    except:
        os.mkdir('data')
        db = sql.connect('data/PapaJohns.db')

    curse = db.cursor()
    print("test")
    try:
        curse.execute("CREATE TABLE obtain (method text)")
        curse.execute("CREATE TABLE payment (method text)")
        curse.execute("CREATE TABLE items (name text, options text)")
        curse.execute("CREATE TABLE options (name text, options text)")
    except:
        pass
    curse.execute("INSERT INTO obtain ('method') VALUES ('delivery')")
    curse.execute("INSERT INTO obtain ('method') VALUES ('carryout')")
    curse.execute("INSERT INTO payment ('method') VALUES ('cash')")
    curse.execute("INSERT INTO payment ('method') VALUES ('credit')")
    curse.execute("INSERT INTO payment ('method') VALUES ('venmo')")
    foods = [('cheese pizza','options1'),
             ('pepperoni pizza', 'options1'),
             ('diet coke', 'options0'),
             ('knots', 'options2')]
    for food in foods:
        curse.execute("INSERT INTO items VALUES (?,?)", (food[0], food[1]))
    options = [('options0', 'no options'),
               ('options1', 'extra cheese;no cheese;green pepper;blueberries'),
               ('options2', 'vegan;extra sauce')]
    for option in options:
        curse.execute("INSERT INTO options VALUES (?,?)", (option[0], option[1]))
    db.commit()

################################################################################
def main():
    header()

    print("Welcome to the FeedMe Editor Tool!")
    while True:
        print("What would you like to do? (type 'help' for a list of commands)")
        command = rinput('> ', COMMANDS.keys(), escape=[], regex=True)
        command_key = '^[{}{}]'.format(command[0], command[0].upper())
        COMMANDS[command_key]()

def get_establishments():
    data_contents = os.listdir('data/')
    establishments = []
    for establishment in data_contents:
        establishment = re.sub('.db$', '', establishment)
        establishment = re.sub('([a-z])([A-Z])', r'\1 \2', establishment) 
        establishments.append(establishment)
    return establishments

###Window methods###############################################################
def window_size():
    return shutil.get_terminal_size()

def clear_screen():#make for windows too
    os.system('clear')

def header():
    clear_screen()
    text = ['FeedMe: {}'.format(SPLASH)]
    template = [mitu.generate_template('center', window_size()[0])]
    rprint(template, text, [window_size()[0]], color='cyan')

def display_items(label, items, columns):##
    header()
    texts = []
    localitems = []
    localitems += items
    for howmanytimes in range(math.ceil(len(localitems)/columns)):
        texts.append([])
        for column in range(columns):
            try:
                texts[howmanytimes].append(localitems[0])
                localitems.pop(0)
            except IndexError:
                texts[howmanytimes].append('')

    templates = []
    spacings = []
    for column in range(columns):
        spacings.append(int(window_size()[0]/columns))
        templates.append(mitu.generate_template('center', 
                                                round(window_size()[0]/columns)))
    print("{}:".format(label))
    for each in texts:
        rprint(templates, each, spacings)

####Database methods############################################################
def db_query(establishment, table, column):
    base = sql.connect('data/{}.db'.format(establishment))
    cursor = base.cursor()
    command = "SELECT {0} FROM {1}".format(column, table)
    query_list = [row[0] for row in cursor.execute(command)]
    base.close()

    return query_list

def db_create_table(db_path, table, rows):##
    db = sql.connect(db_path)
    cursor = db.cursor()
    """try:
        command = "CREATE TABLE {} """

##Commands######################################################################
def create_formatted_match_list(matches):
    formatted_matches = []
    for match in matches:
        formatted_match = '(?i)' + match
        formatted_matches.append(re.sub(' ', ' ?', formmated_match))
    return formatted_matches

def command_help():##
    header()
    print("help screen")

def command_new():
    header()
    print("Enter a name for the order (e.g. 'fav pizza')")
    name = input("> ")
    establishments = get_establishments()
    display_items('Establishments', establishments, 5)
    print("\nSelect an establishment.")
    formatted_establishments = create_formatted_match_list(establishments)
    establishment = rinput("> ", formatted_establishments, regex=True)
    print(establishment)
    menu = db_query('PapaJohns', 'items', 'name')
    display_items('Menu', menu, 5)

    
    
    



def command_quit():
    header()
    if confirm_input(ask="Are you sure you'd like to quit? (Y/n)"):
        clear_screen()
        quit()
    else:
        header()

##Constants#####################################################################
SPLASHES = ['Over 1 billion fed!',
            'Written in python!',
            'Splash 3',
            'Randy sucks']

SPLASH = random.choice(SPLASHES)
COMMANDS = {'^[hH]' : command_help,
            '^[nN]' : command_new,
            '^[qQ]' : command_quit}

if __name__ == '__main__':
    TEMPORARY_POPULATE_DATABASE()
    main()

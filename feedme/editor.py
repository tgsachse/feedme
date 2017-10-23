#!/usr/bin/env python3
from mitu import confirm_input, rinput, rprint
import os
import json
import pickle

class Order:
    """
    """
    def __init__(self, name, establishment, delivery_method, address):
        self.name = name
        self.establishment = establishment
        self.delivery_method = delivery_method
        self.address = address
        self.items = {}
    
    def __add__(self, other):
        if self.establishment != other.establishment:
            raise TypeError("orders are from different establishments")
        if self.delivery_method != other.delivery_method:
            raise TypeError("orders use different delivery methods")
        if self.address != other.address:
            raise TypeError("orders are delivered to different addresses")
        
        new_name = '{0} and {1}'.format(self.name, other.name)
        new_order = Order(
                new_name, 
                self.establishment, 
                self.delivery_method, 
                self.address)
        new_order.items = self.items + other.items
        return new_order

    def __len__(self):
        return len(self.items)

    def __repr__(self):
        return 'Order(\'{0}\')'.format(self.name)

    def __str__(self):
        return 'Order \'{0}\', containing {1} items'.format(
                self.name,
                self.__len__())

    def add_item(self, name, options):
        self.items[name] = options

########################################
def main():
    header()
    
    while True:
        print("What would you like to do? ('help' for a list of commands)")
        command = rinput("> ", COMMANDS.keys())
        COMMANDS[command]()

def command_help():
    header()
    for key, value in COMMANDS.items():
        print(key, value)

def command_orders_list():
    header()
    for order in orders:
        print(order)
        print(order.items)

def command_orders_new():

    def new_item(order):
        print("Type the name of the item you'd like to add, or type 'list'")
        valid = list(items.keys()) + ['list']
        item = rinput("> ", valid)
        while item == 'list':
            for each in items.keys():
                print(each)
            item = rinput("> ", valid)

        print("Which options would you like to add for the item? Leave " + 
              "blank for no options.")
        valid = items[item][1::] + ['list', '']
        options = rinput("> ", valid)
        while options == 'list':
            for each in items[item][1::]:
                print(each)
            options = rinput("> ", valid)
        order.add_item(item, options)

    header()
    print("Enter a name for the order (e.g. 'favorite pizza')")
    name = input("> ")

    print("Enter establishment name or type 'list'")
    valid = list(establishments.keys()) + ['list']
    establishment = rinput("> ",
                           valid,
                           invalid="Establishment not available")
    while establishment == 'list':
        for each in establishments.keys():
            print(each)
        establishment = rinput("> ",
                               valid,
                               invalid="Establishment not available")

    if len(establishments[establishment]['delivery methods']) != 1:
        print("Enter delivery method or type 'list'")
        valid = establishments[establishment]['delivery methods'] + ['list']
        method = rinput("> ", valid, invalid="Invalid delivery method")
        while method == 'list':
            for each in establishments[establishment]['delivery methods']:
                print(each)
            method = rinput("> ", valid, invalid="Invalid delivery method")
    else:
        print("Only {} available. Selecting by default.".format(
            establishments[establishment]['delivery methods']))
        method = establishments[establishment]['delivery methods']
    
    if len(personal) != 0:
        prompt="(Y/n): "
        ask="Deliver to default address? ({0})".format(
            personal['address']['default'][0])
        if confirm_input(prompt, ask):
            address = personal['address']
        else:
            for address in personal['address']:
                print(personal['address'][address]) #fancy print##unfinished
    
    order = Order(name, establishment, method, address)
    new_item(order)
    print("Add more items, or finish order? (Type 'add' or 'finish')")
    question = rinput("> ", ['add', 'finish'])
    while question == 'add':
        new_item(order)
        print("Add more items, or finish order? (Type 'add' or 'finish')")
        question = rinput("> ", ['add', 'finish'])

    orders.append(order)

def command_quit():
    header()
    if confirm_input(ask="Are you sure you'd like to quit? (Y/n)"):
        os.system('clear')
        quit()
    else:
        header()

def command_save():
    with open(F_ORDERS, 'wb') as f:
        pickle.dump(orders, f)
    print("orders saved")

def header():
    os.system('clear')
    text = "FeedMe"
    print(text)

def load_file(FILE, return_type = {}, read_method='r', read_type = json):
    try:
        with open(FILE, read_method) as f:
            data = read_type.load(f)
    except FileNotFoundError:
        data = return_type
    return data


###################################################
F_ESTABLISHMENTS = 'data/establishments.json'
F_ORDERS = 'data/orders.data'
F_PERSONAL = 'data/personal.json'

COMMANDS = {'h':command_help,
            'l':command_orders_list,
            'n':command_orders_new,
            's':command_save,
            'q':command_quit}

items = {'cheeze': ['lipstick'], 'pepeer': ['nomayo','mayo'], 'suasage': []}
establishments = load_file(F_ESTABLISHMENTS)
orders = load_file(F_ORDERS,
                   return_type=[],
                   read_method='rb',
                   read_type=pickle)
personal = load_file(F_PERSONAL)
main()

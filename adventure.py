import sys
import json

game_map = {}

#check if mapper file is passed as argument with the python file or raise exception
arg_length=len(sys.argv)
if arg_length < 2:
    raise Exception('Game input type: python3 adventure.py (mapper_file.txt)')

#function that defines how to read the mapper file into game_map
def load(argv):
    global game_map
    try:
        with open(argv[1], 'r') as file:
            game_map = json.load(file)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit()


# Defining first room as current
present_room = 0
present_inventory = []
items = []
directions = []


def go_directions():
    global directions
    for room in game_map:
        if room.get('exits') is None:
            continue
        else:
            for dir in room.get('exits').keys():
                if dir in directions:
                    continue
                else:
                    directions.append(dir)


def room_items():
    global items
    for room in game_map:
        if room.get('items') is None:
            continue
        else:
            for item in room.get('items'):
                if item in items:
                    continue
                else:
                    items.append(item)


def show_inventory():
    if len(present_inventory) == 0:
        print('You\'re not carrying anything.')
        return
    else:
        print('Inventory:')
        for item in present_inventory:
            print(f'  {item}')


def get_data_of_room(room):
    leng=len(game_map)
    if leng > room >= 0:
        return game_map[room]
    else:
        print(f'The room with index {room} does not exists in map., \n')
        return None


def look(room):
    room_data = get_data_of_room(room)
    if room_data is None:
        return
    room_name = room_data.get('name')
    dsc = room_data.get('desc')
    str = " ".join(room_data['exits'].keys())
    print(f'> {room_name}\n')
    print(f'{dsc}\n')
    if room_data.get('items') is not None and len(room_data.get('items')) != 0:
        itm_str = ", ".join(room_data['items'])
        print('Items: ' + itm_str + '\n')
    print('Exits: ' + str + '\n')


def look_present_room():
    look(present_room)


def help():
    print('You can run the following commands:')
    for verb in verb_list:
        print(verb, ' : ', verb_list.get(verb).get('desc'))


def get_item_from_room(item_name, room_name):
    global present_inventory
    data_of_room = get_data_of_room(room_name)
    if data_of_room is not None:
        if item_name in data_of_room.get('items'):
            present_inventory.append(item_name)
            game_map[room_name]['items'].remove(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There is no {item_name} anything.")
    else:
        return


def drop_item_in_room(item_name, room_name):
    global present_inventory
    data_of_room = get_data_of_room(room_name)
    if data_of_room is not None:
        if item_name in present_inventory:
            present_inventory.remove(item_name)
            game_map[room_name].setdefault('items', []).append(item_name)
            print(f"You drop the {item_name}.")
        else:
            print(f"You aren't carrying a {item_name}.")
    else:
        return


def game_quit_now():
    print('Goodbye!')
    sys.exit()


def next_room_go(dir, room_name):
    global present_room
    data_of_room = get_data_of_room(room_name)
    if data_of_room is not None:
        if dir in data_of_room.get('exits'):
            present_room = data_of_room.get('exits').get(dir)
            print(f'You go {dir}.\n')
            look_present_room()
        else:
            print(f"There's no way to go {dir}.")
    else:
        return



def next_room_go_utils(args):
    if len(args) != 2:
        print(f'Sorry, you need to \'go\' somewhere.')
        return
    room_data = get_data_of_room(present_room)
    if room_data is None:
        return
    else:
        matched_directions = input_match(args[1], room_data.get('exits'))
        if len(matched_directions) == 0:
            print(f'There\'s no way to go {args[1]}.')
            return
        else:
            if len(matched_directions) > 1:
                current_items = list_join(matched_directions, " or ")
                print(f'Did you want to get the {current_items} ?')
                return
            next_room_go(matched_directions[0], present_room)


def item_get_utils(args):
    if len(args) != 2:
        print('Sorry, you need to \'get\' something.')
        return
    room_data = get_data_of_room(present_room)
    if room_data is None:
        return
    else:
        curr_items = room_data.get('items')
        try:
            curr_items = list(filter(lambda i: i not in present_inventory, room_data.get('items')))
        except:
            pass
        matched_items = input_match(args[1], curr_items)
        if len(matched_items) == 0:
            print(f'There\'s no {args[1]} anywhere.')
            return
        else:
            if len(matched_items) > 1:
                current_items = list_join(matched_items, " or the ")
                print(f'Did you want to get the {current_items} ?')
                return
            get_item_from_room(matched_items[0], present_room)


def item_drop_utils(args):
    if len(args) != 2:
        print('Sorry, you need to \'drop\' something.')
        return
    room_data = get_data_of_room(present_room)
    if room_data is None:
        return
    else:
        matched_items = input_match(args[1], present_inventory)
        if len(matched_items) == 0:
            print(f'There\'s no {args[1]} in inventory.')
            return
        else:
            if len(matched_items) > 1:
                current_items = list_join(matched_items, " or the ")
                print(f'Did you want to drop the {current_items} ?')
                return
            drop_item_in_room(matched_items[0], present_room)



verb_list = {
    'go': {
        'func': next_room_go_utils,
        'params': True,
        'desc': 'go <direction>. tries to go in the specified direction <direction> room from current room.'
    },
    'help': {
        'func': help,
        'params': False,
        'desc': 'keeps track of what the verbs in the game are and prints them'
    },
    'look': {
        'func': look_present_room,
        'params': False,
        'desc': 'show which room the person is in right now'
    },
    'get': {
        'func': item_get_utils,
        'params': True,
        'desc': 'get <item>. lets a player pick the item <item> that are in the room'
    },
    'inventory': {
        'func': show_inventory,
        'params': False,
        'desc': 'shows the player what they are carrying'
    },
    'quit': {
        'func': game_quit_now,
        'params': False,
        'desc': 'should exit the game. Also, sending an interrupt should end the game immediately'
    },
    'drop': {
        'func': item_drop_utils,
        'params': True,
        'desc': 'take the item <item> from your inventory and put it down in the room'
    }
}


def verb_match(string_input):
    verb_matches = []
    for verbe in verb_list:
        if verbe == string_input:
            return [verbe]
        else:
            if string_input in verbe:
                verb_matches.append(verbe)
    return verb_matches


def input_match(string_input, options_valid):
    verb_matches = []
    leng=len(options_valid)
    if options_valid is None or leng == 0:
        return verb_matches
    for verbe in options_valid:
        if verbe == string_input:
            return [verbe]
        else:
            if string_input in verbe:
                verb_matches.append(verbe)
    return verb_matches

def list_join(liste, iden):
    strr=", ".join(liste[:-1]).rstrip()
    return strr + iden + liste[-1]

def game_start():
    global present_room
    look_present_room()
    while True:
        try:
            intput = input("What would you like to do? ")
        except KeyboardInterrupt as e:
            raise e
        except EOFError:
            print('Use \'quit\' to exit.')
            continue

        arguments_act = intput.strip().lower().split()
        lengt=len(arguments_act)
        if lengt == 0:
            continue
        verbs_matched = verb_match(arguments_act[0])
        leng=len(verbs_matched)
        if leng == 0:
            print('invalid ip')
            continue
        else:
            if leng == 1:
                if verb_list.get(verbs_matched[0]).get('params'):
                    verb_list.get(verbs_matched[0]).get('func')(arguments_act)
                else:
                    verb_list.get(verbs_matched[0]).get('func')()
                continue
            else:
                str_match = list_join(verbs_matched, " or ")
                print(f"Did you want to {str_match} ?")
                continue



load(sys.argv)
go_directions()
room_items()
game_start()

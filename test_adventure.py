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
        print(f'ERROR: {e.with_traceback()}')
        sys.exit()

# load game map, our only game asset
load(sys.argv)
# print('Loaded map: ', game_map)

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
    print('Inventory:')
    for item in present_inventory:
        print(f'  {item}')


def get_room_data(room):
    leng=len(game_map)
    if leng > room >= 0:
        return game_map[room]
    else:
        print(f'The room with index {room} does not exists in map., \n')
        return None


def look(room):
    data_of_room = get_room_data(room)
    if data_of_room is None:
        return
    else:
        name_of_room = data_of_room.get('name')
        print(f'> {name_of_room} \n')
        print(data_of_room['desc'], '\n')
        if data_of_room.get('items') is None:
            print('Exits:', " ".join(data_of_room['exits'].keys()), '\n')
        else:
            print('Items:', " ".join(data_of_room['items']))
            print('Exits:', " ".join(data_of_room['exits'].keys()), '\n')


def look_present_room():
    look(present_room)


def help():
    print('You can run the following commands:')
    for verb in verb_list:
        print(verb, ' : ', verb_list.get(verb).get('desc'))


def get_item_from_room(item_name, room_name):
    global present_inventory
    data_of_room = get_room_data(room_name)
    if data_of_room is not None:
        if item_name in data_of_room.get('items'):
            present_inventory.append(item_name)
            game_map[room_name]['items'].remove(item_name)
            print(f"You pick up the {item_name}.")
        else:
            print(f"There's no {item_name} anywhere.")
    else:
        return


def drop_item_in_room(item_name, room_name):
    global present_inventory
    data_of_room = get_room_data(room_name)
    if data_of_room is not None:
        if item_name in present_inventory:
            present_inventory.remove(item_name)
            game_map[room_name].setdefault('items', []).append(item_name)
            print(f"You drop the {item_name}.")
        else:
            print(f"You are not carrying the item {item_name} in your inventory.")
    else:
        return


def game_quit_now():
    print('Goodbye!')
    sys.exit()


def go_to_next_room(dir, room_name):
    global present_room
    data_of_room = get_room_data(room_name)
    if data_of_room is not None:
        if dir in data_of_room.get('exits'):
            present_room = data_of_room.get('exits').get(dir)
            print(f'You go {dir}.')
            look_present_room()
        else:
            print(f"There's no way to go {dir}.")
    else:
        return





verb_list = {
    'go': {
        'alias': [],
        'func': go_to_next_room,
        'desc': 'go <direction>. tries to go in the specified direction <direction> room from current room.'
    },
    'help': {
        'alias': [],
        'func': help,
        'desc': 'keeps track of what the verbs in the game are and prints them'
    },
    'look': {
        'alias': [],
        'func': look_present_room,
        'desc': 'show which room the person is in right now'
    },
    'get': {
        'alias': [],
        'func': get_item_from_room,
        'desc': 'get <item>. lets a player pick the item <item> that are in the room'
    },
    'inventory': {
        'alias': [],
        'func': show_inventory,
        'desc': 'shows the player what they are carrying'
    },
    'quit': {
        'alias': [],
        'func': game_quit_now,
        'desc': 'should exit the game. Also, sending an interrupt should end the game immediately'
    },
    'drop': {
        'alias': [],
        'func': drop_item_in_room,
        'desc': 'take the item <item> from your inventory and put it down in the room'
    }
}


def verb_match(string_input):
    verb_matches = []
    for verbe in verb_list:
        if verbe == string_input:
            return [verbe]
        else:
            if verbe.startswith(string_input):
                verb_matches.append(verbe)
    return verb_matches


def match_input(string_input, options_valid):
    verb_matches = []
    for verbe in options_valid:
        if verbe == string_input:
            return [verbe]
        else:
            if string_input in verbe:
                verb_matches.append(verbe)
    return verb_matches


def game_start():
    global present_room
    look_present_room()
    while True:
        try:
            command = input("What would you like to do? ")

        except KeyboardInterrupt as e:
            raise e

        except EOFError:
            print('Use \'quit\' to exit. \n')
            continue

        action_args = command.strip().lower().split()
        verbs_matched = verb_match(action_args[0])
        lengt=len(verbs_matched)
        if lengt == 0:
            print(
                f"The command {command} could not be identified. See \'help\' to know more about set of valid "
                f"commands ")
            continue
        elif lengt == 1:
            this_verb = verbs_matched[0]
            if this_verb == "go":
                if len(action_args) != 2:
                    print(f'Sorry, you need to \'go\' somewhere.')
                    continue
                direction = match_input(action_args[1], directions)
                if len(direction) == 0:
                    print(f'There\'s no way to go {action_args[1]}.')
                    continue
                else:
                    if len(direction) > 1:
                        item = " or ".join(direction).rstrip()
                        print(f'Did you want to get the {item} ?')
                        continue
                go_to_next_room(direction[0], present_room)
            elif this_verb == "inventory":
                show_inventory()
            elif this_verb == "look":
                look_present_room()
            elif this_verb == "help":
                help()
            elif this_verb == "quit":
                game_quit_now()
            elif this_verb == "get":
                if len(action_args) != 2:
                    print('Sorry, you need to \'get\' something.')
                    continue
                matched_items = match_input(action_args[1], items)
                leng=len(matched_items)
                if leng == 0:
                    print(f'There\'s no {action_args[1]} anywhere.')
                    continue
                else:
                    if leng > 1:
                        item = " or ".join(matched_items).rstrip()
                        print(f'Did you want to get the {item} ?')
                        continue
                get_item_from_room(matched_items[0], present_room)
            elif this_verb == "drop":
                if len(action_args) != 2:
                    print('Sorry, you need to \'drop\' something.')
                    continue
                matched_items = match_input(action_args[1], items)
                leng=len(matched_items)
                if leng == 0:
                    print(f'There\'s no {action_args[1]} in inventory.')
                    continue
                else:
                    if leng > 1:
                        item = " or ".join(matched_items).rstrip()
                        print(f'Did you want to drop the {item} ?')
                        continue
                drop_item_in_room(matched_items[0], present_room)
            else:
                verb_list.get(this_verb).get('func')()
        else:
            list_matched = " or ".join(verbs_matched).rstrip()
            print(f"Did you want to {list_matched} ?")
            continue


go_directions()
room_items()
game_start()

import sys
import json

# Load the game maps
file_access_mode = 'r'
maps = {}

if len(sys.argv) < 2:
    raise Exception('Game init input: python3 adventure.py (map_json_file_name.txt)')


def load_file(argv):
    global maps
    try:
        with open(argv[1], file_access_mode) as maps_file:
            maps = json.load(maps_file)
    except Exception as e:
        print(f'ERROR: {e.with_traceback()}')
        sys.exit()


load_file(sys.argv)
# print('Loaded map: ', maps)

# Start the game in the first room
current_room = 0
current_inventory = []
directions = []
items = []


def get_predefined_directions():
    global directions
    for room in maps:
        if room.get('exits') is not None:
            for dir in room.get('exits').keys():
                if dir not in directions:
                    directions.append(dir)


def get_predefined_items():
    global items
    for room in maps:
        if room.get('items') is not None:
            for item in room.get('items'):
                if item not in items:
                    items.append(item)


def look_room(room):
    room_data = get_room_data(room)
    if room_data is None:
        return
    room_name = room_data.get('name')
    print(f'> {room_name} \n')
    print(room_data['desc'], '\n')
    if room_data.get('items') is not None:
        print('Items:', " ".join(room_data['items']))
    print('Exits:', " ".join(room_data['exits'].keys()), '\n')


def look_current_room():
    look_room(current_room)


def get_room_data(room):
    if len(maps) > room >= 0:
        room_data = maps[room]
        return room_data
    else:
        print(f'The room with index {room} does not exists in map., \n')
        return None


def help():
    print('---------- Available commands in the game ---------')
    for verb in verbs:
        print(verb, ' : ', verbs.get(verb).get('desc'))
    print('--------------------------------------------------- ')


def get_item(item, room):
    global current_inventory
    room_data = get_room_data(room)
    if room_data is None:
        return
    if item in room_data.get('items'):
        current_inventory.append(item)
        maps[room]['items'].remove(item)
        print(f"You pick up the {item}.")
    else:
        print(f"There is no {item} anything.")


def drop_item(item, room):
    global current_inventory
    room_data = get_room_data(room)
    if room_data is None:
        return
    if item in current_inventory:
        current_inventory.remove(item)
        maps[room].setdefault('items', []).append(item)
        print(f"You drop the {item}.")
    else:
        print(f"You aren't carrying a {item}.")


def show_inventory():
    print('Inventory:')
    for inv in current_inventory:
        print(f'  {inv}')


def go_to_next_room(direction, room):
    global current_room
    room_data = get_room_data(room)
    if room_data is None:
        return
    if direction in room_data.get('exits'):
        current_room = room_data.get('exits').get(direction)
        print(f'You go {direction}.')
        look_room(current_room)
    else:
        print(f"There's no way to go {direction}.")


def quit_game():
    print('Goodbye!')
    sys.exit()


verbs = {
    'go': {
        'alias': [],
        'func': go_to_next_room,
        'desc': 'go <direction>. take it to <direction> room from the current room.'
    },
    'help': {
        'alias': [],
        'func': help,
        'desc': 'print available command in the game'
    },
    'look': {
        'alias': [],
        'func': look_current_room,
        'desc': 'print the view of the current room'
    },
    'get': {
        'alias': [],
        'func': get_item,
        'desc': 'get <item>. collect the item <item> from the current room if it\'s available'
    },
    'inventory': {
        'alias': [],
        'func': show_inventory,
        'desc': 'print out the collected inventories'
    },
    'quit': {
        'alias': [],
        'func': quit_game,
        'desc': 'terminate the game. Even, CTRL+C can be used to terminate the game'
    },
    'drop': {
        'alias': [],
        'func': drop_item,
        'desc': 'drop <item>. drop the item <item> from the current collected inventory'
    }
}


def match_verbs(input_str):
    matches = []
    for option in verbs:
        if option == input_str:
            return [option]
        if option.startswith(input_str):
            matches.append(option)
    return matches


def match_input(input_str, valid_options):
    matches = []
    for option in valid_options:
        if option == input_str:
            return [option]
        if input_str in option:
            matches.append(option)
    return matches


def start_game():
    global current_room

    look_room(current_room)
    while True:
        try:
            command = input("What would you like to do? ")

        except KeyboardInterrupt as e:
            raise e

        except EOFError:
            print('Use \'quit\' to exit. \n')
            continue

        action_args = command.strip().lower().split()
        matched_verbs = match_verbs(action_args[0])
        if len(matched_verbs) == 0:
            print(
                f"Unidentified cmd_input input: {command}. Please enter \'help\' to know more about inbuilt "
                f"commands.")
            continue
        elif len(matched_verbs) == 1:
            current_verb = matched_verbs[0]
            if current_verb == "go":
                if len(action_args) != 2:
                    print(f'Sorry, you need to \'go\' somewhere.')
                    continue
                matched_directions = match_input(action_args[1], directions)
                if len(matched_directions) == 0:
                    print(f'There\'s no way to go {action_args[1]}.')
                    continue
                if len(matched_directions) > 1:
                    current_items = " or ".join(matched_directions).rstrip()
                    print(f'Did you want to get the {current_items} ?')
                    continue
                go_to_next_room(matched_directions[0], current_room)
            elif current_verb == "look":
                look_room(current_room)
            elif current_verb == "inventory":
                show_inventory()
            elif current_verb == "get":
                if len(action_args) != 2:
                    print('Sorry, you need to \'get\' something.')
                    continue
                matched_items = match_input(action_args[1], items)
                if len(matched_items) == 0:
                    print(f'There\'s no {action_args[1]} anywhere.')
                    continue
                if len(matched_items) > 1:
                    current_items = " or ".join(matched_items).rstrip()
                    print(f'Did you want to get the {current_items} ?')
                    continue
                get_item(matched_items[0], current_room)
            elif current_verb == "drop":
                if len(action_args) != 2:
                    print('Sorry, you need to \'drop\' something.')
                    continue
                matched_items = match_input(action_args[1], items)
                if len(matched_items) == 0:
                    print(f'There\'s no {action_args[1]} in inventory.')
                    continue
                if len(matched_items) > 1:
                    current_items = " or ".join(matched_items).rstrip()
                    print(f'Did you want to drop the {current_items} ?')
                    continue
                drop_item(matched_items[0], current_room)
            elif current_verb == "quit":
                quit_game()
            elif current_verb == "help":
                help()
            else:
                verbs.get(matched_verbs[0]).get('func')()
        else:
            list_matched = " or ".join(matched_verbs).rstrip()
            print(f"Did you want to {list_matched} ?")
            continue


get_predefined_directions()
get_predefined_items()
# print(verbs.keys())
# print(directions)
# print(items)
start_game()

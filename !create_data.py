import json
import os
import _main

file_names = os.listdir("layouts/")

past = []
layouts = []

for file in file_names:
    with open(f'layouts/{file}', 'r') as file:
        keyboard_layout = json.load(file)

    layout = ["~~~~~~~~~~","~~~~~~~~~~","~~~~~~~~~~"]
    unused_alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    for key in list(keyboard_layout["keys"].keys()):
        row_index = [keyboard_layout["keys"][key]['row']][0]
        col_index = [keyboard_layout["keys"][key]['col']][0]
        if row_index < 3:
            if key in unused_alpha and col_index <= 9: 
                unused_alpha.remove(key)
                new_row = layout[row_index][:col_index] + key + layout[row_index][col_index + 1:]
                new_row = ''.join([char if char in alpha else '~' for char in new_row])
                layout[row_index] = new_row

    try:
        if len(unused_alpha) == 0:
            e200 = _main.evaluate([layout], "english-200")

            if e200 not in past:
                past.append(e200)
                homerow = sorted([layout[1][6:10], layout[1][0:4][::-1]])
                homerow = homerow[0] + homerow[1]

                layouts.append({'name': keyboard_layout['name'], 
                                'user': keyboard_layout['user'],
                                'homerow': homerow,
                                'layout': [" ".join(layout[0]).upper(), " ".join(layout[1]).upper(), " ".join(layout[2]).upper()],
                                'english-200' : e200,
                                'english-1k'  : _main.evaluate([layout], "english-1k"),
                                'keymash'     : _main.evaluate([layout], "keymash"),
                                'monkey-type' : _main.evaluate([layout], "monkey-type"),
                                'discord'     : _main.evaluate([layout], "discord")})

    except:
        pass

json_string = json.dumps(layouts, indent=4)

with open("data1.json", "w") as f:
    f.write(json_string)

print("done")
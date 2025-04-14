import igraph
import copy
import hashlib
import json

with open("data.json", "r") as file:
    data = json.load(file)

def string_to_rgb_color(s):
    hash_val = hashlib.md5(s.encode('utf-8')).hexdigest()
    r = int(hash_val[0:2], 16)
    g = int(hash_val[2:4], 16)
    b = int(hash_val[4:6], 16) 

    return (r / 256, g / 256, b / 256)

group_amount = {}
group_colors = {}

for item in data:
    group = item['homerow']
    
    if group not in group_colors:
        group_colors[group] = string_to_rgb_color(group)
        group_amount[group] = 1
    else:
        group_amount[group] += 1 

for colour in copy.copy(group_amount):
    if group_amount[colour] == 1:
       group_colors[colour] = "#1D1C1A"

graph = igraph.Graph()

# Add vertices to the graph with names, colors, coordinates and size

graph.add_vertices(len(data))
graph.vs["name"] = [item['name'] for item in data]
graph.vs["color"] = [group_colors[item['homerow']] for item in data]
graph.vs["x"] = [item['stats']["Inrolls"] for item in data]
graph.vs["y"] = [item['stats']["Outrolls"] for item in data]
graph.vs["size"] = [item['stats']["Alt"]/(340*18) for item in data]

edge_colours = []

for i in range(len(data)):
    for j in range(i + 1, len(data)):
        if data[j]['homerow'] == data[i]['homerow']:
            graph.add_edge(i, j)
            edge_colours.append(graph.vs[i]["color"])

def shift_positions(layout, threshold=20*18, shift_amount=10*18):
    for _ in range(5):
        for i in range(len(layout)):
            for j in range(i + 1, len(layout)):
                dx = layout[j][0] - layout[i][0]
                dy = layout[j][1] - layout[i][1]
                distance = (dx**2 + dy**2)**0.5
                if distance < threshold:
                    if distance == 0:
                        dx = 1
                        dy = 1
                    else:
                        dx /= distance
                        dy /= distance
                    layout[i] = (layout[i][0] - dx * shift_amount, layout[i][1] - dy * shift_amount)
                    layout[j] = (layout[j][0] + dx * shift_amount, layout[j][1] + dy * shift_amount)
    return layout

# Plot the graph with vertex labels and save it as an image file
plot = igraph.plot(
    graph, bbox=(6000, 6000), 
    vertex_label=graph.vs["name"],
    vertex_color=graph.vs["color"], 
    edge_color=edge_colours,
    layout=shift_positions([(x, y) for x, y in zip(graph.vs["x"], graph.vs["y"])]),
    background="black",
    vertex_label_color="white", 
    margin=250, 
    edge_width=0.8,
    edge_curved=0.1)

plot.save("graphs/graph2.png")
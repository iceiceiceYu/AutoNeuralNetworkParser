import json
from graph_node import Node


class Curve:
    def __init__(self, c_id, name, from_id, to_id):
        self.c_id = c_id
        self.name = name
        self.from_id = from_id
        self.to_id = to_id


def loader(path):
    with open(path, 'r') as JSON_file:
        original = JSON_file.read()
    reformed = reform(original)
    data = json.loads(reformed)['pens']

    node_list = []
    curve_list = []

    for i in range(len(data)):
        tmp_data = data[i]
        if tmp_data['type'] == 0:
            node_list.append(Node(tmp_data['id'], tmp_data['name'], tmp_data['text'], tmp_data['data']))
        elif tmp_data['type'] == 1:
            curve_list.append(Curve(tmp_data['id'], tmp_data['name'], tmp_data['from']['id'], tmp_data['to']['id']))

    id2block = {}
    for i in range(len(node_list)):
        id2block[node_list[i].n_id] = node_list[i]
        print(node_list[i])

    for i in range(len(curve_list)):
        from_block = id2block[curve_list[i].from_id]
        to_block = id2block[curve_list[i].to_id]

        from_block.output.append(to_block)
        to_block.input.append(from_block)

    return node_list


def reform(original):
    return original.replace(
        '"fontFamily":"\"Hiragino Sans GB\", \"Microsoft YaHei\", \"Helvetica Neue\", Helvetica, Arial",', '')

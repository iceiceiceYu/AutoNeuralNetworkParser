import JSON_loader
from block import Block
from curve import Curve

b_list, c_list = JSON_loader.loader('src_demo.json')
print(c_list)
print(b_list)

id2block = {}
for i in range(len(b_list)):
    id2block[b_list[i].b_id] = b_list[i]
print(id2block)

for i in range(len(c_list)):
    from_block = id2block[c_list[i].from_id]
    to_block = id2block[c_list[i].to_id]

    from_block.output.append(to_block)
    to_block.input.append(from_block)

for i in range(len(b_list)):
    print(b_list[i].output)
    print(b_list[i].input)
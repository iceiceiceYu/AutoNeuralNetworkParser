from block import Block
from pytorch_block import PytorchBlockFactory

var_index = 0
"""

1. Input: (x)
2. Conv2D:
3. MaxPooling2D
4. ReLU
5. Linear
6. Softmax
7. Concat
8. ResIncp
"""


def generate(b_list):
    # find input block by name
    input_block = None
    for i in range(len(b_list)):
        if b_list[i].name == "Input":
            input_block = b_list[i]
            break

    res_code = ''

    # walk through the graph and mark nodes
    block_to_deal = [input_block]
    while len(block_to_deal) != 0:
        curr_block = block_to_deal.pop(0)
        if check_input(curr_block):
            curr_block.output_variable = var_generator()
            res_code += block_to_code(curr_block, curr_block.output_variable)
            block_to_deal.extend(curr_block.output)

    return res_code


def check_input(block:Block):
    for i in range(len(block.input)):
        if block.input[i].output_variable is None:
            return False
    return True


def var_generator():
    global var_index
    var_index += 1
    return 'out' + str(var_index)


def block_to_code(block, out_var_name):
    return PytorchBlockFactory.new_instance(block.name, block, out_var_name).to_pytorch_code() + '\n'

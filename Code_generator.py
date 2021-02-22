from block import Block

var_index = 0


def generate(b_list:list[Block]):
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
            res_code += block_to_code(curr_block)
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
    return 'x' + str(var_index)


def block_to_code(block):
    input_str = ', '.join([temp.output_variable for temp in block.input])
    return block.output_variable + ' = ' + block.name + '(' + input_str + ')\n'

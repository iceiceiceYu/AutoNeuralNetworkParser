from graph_node import Node
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
class Container:
    pass

class Translator:
    def __init__(self, n_list):
        self.template_code = \
"""
import torch
import torch.nn

class MyModel(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
[INIT_AREA]

    def forward(self, *input: Any, **kwargs: Any) -> T_co:
[FORWARD_PROPRAGATION_AREA]
"""
        self.template_code_init_replace = "[INIT_AREA]"
        self.template_code_forw_replace = "[FORWARD_PROPRAGATION_AREA]"

        self.var_index = 0
        self.out_index = 0
        self.node_list = n_list
        self.layer_names = []
        self.start_node = None

    def translate(self):
        self.model_init()
        self.repl_forward()
        return self.template_code

    def model_init(self):
        # find input node by name
        n_list = self.node_list
        input_node = None
        for i in range(len(n_list)):
            if n_list[i].name == "Input":
                input_node = n_list[i]
                self.start_node = input_node
                break

        init_declarations = []

        # walk through the graph and mark nodes
        node_to_deal = [input_node]
        while len(node_to_deal) != 0:
            curr_node = node_to_deal.pop(0)
            if Translator.check_input(curr_node):
                curr_node.declared_var_name = self.gen_var_name(curr_node)
                line_code = '\t\t' + Translator.node_to_var_declaration(curr_node, curr_node.declared_var_name)
                if line_code.strip(): init_declarations.append(line_code)
                # 用for循环是为了不重复加入
                for next_node in curr_node.output:
                    if next_node not in node_to_deal:
                        node_to_deal.append(next_node)

        self.template_code = self.template_code.replace(self.template_code_init_replace, '\n'.join(init_declarations))

    def repl_forward(self):
        # 给 Input 也加上之前的东西，这些都是Mock的家的东西
        mockInput = Container()
        mockInput.output_var_name = "input"
        mockInput.declared_var_name = "input"
        self.start_node.input.append(mockInput)

        node_to_deal = [self.start_node]
        forward_codes = []
        end_nodes = []  # 可能有多个返回值

        while len(node_to_deal) != 0 :
            curr_node = node_to_deal.pop(0)
            if Translator.check_input_2(curr_node):
                out_name = self.gen_out_name()
                curr_node.output_var_name = out_name
                forward_code = '\t\t' + Translator.node_to_calling(curr_node, out_name)
                forward_codes.append(forward_code)
                if len(curr_node.output) > 0:
                    for next_node in curr_node.output:
                        if next_node not in node_to_deal:
                            node_to_deal.append(next_node)
                else:
                    end_nodes.append(curr_node)

        return_stat = "\t\treturn (" + ", ".join([end_node.output_var_name for end_node in end_nodes]) + ")"
        forward_codes.append(return_stat)
        self.template_code = self.template_code.replace(self.template_code_forw_replace, "\n".join(forward_codes))

    def gen_out_name(self):
        self.out_index += 1
        return "out" + str(self.out_index)

    def gen_var_name(self, node: Node):
        self.var_index += 1
        return "self." + node.name.lower() + "_var_" + str(self.var_index)

    # 下面的两个东西只有一个变量不同，是因为阶段不同
    # 仔细想想逻辑
    @staticmethod
    def check_input(node: Node):
        for i in range(len(node.input)):
            if node.input[i].declared_var_name is None:
                return False
        return True

    @staticmethod
    def check_input_2(node: Node):
        for i in range(len(node.input)):
            if node.input[i].output_var_name is None:
                return False
        return True

    @staticmethod
    def node_to_var_declaration(node, out_var_name):
        return PytorchBlockFactory.new_instance(node.name, node).to_declare_code(out_var_name)

    @staticmethod
    def node_to_calling(node, out_forward_name):
        return PytorchBlockFactory.new_instance(node.name, node).to_forward_code(out_forward_name)
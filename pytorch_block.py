from block import Block

class PytorchBlockFactory:
    @staticmethod
    def new_instance(typename, block, output_name):
        if typename == "Conv2D":
            return Conv2D(block, output_name)
        elif typename == "MaxPooling2D":
            return MaxPooling2D(block, output_name)
        elif typename == "ReLU":
            return ReLU(block, output_name)
        elif typename == "Linear":
            return Linear(block, output_name)
        elif typename == "Softmax":
            return Softmax2D(block, output_name)
        else:
            return EmptyBlock(block, output_name)


class PytorchBlock:
    def __init__(self, block: Block, output_name: str):
        self.src_block = block
        self.arg_keys = {}
        self.args = {}
        self.mapping_name = ""
        self.output_name = output_name

    def to_pytorch_code(self):
        self.parse_args()
        ret = ""
        ret += self.output_name
        ret += " = "
        ret += self.mapping_name
        ret += "("
        for key, value in self.args.items():
            ret += key
            ret += "="
            ret += value
            ret += ", "
        if len(self.args.items()) != 0:
            ret = ret[0:-2]
        ret += ")"
        return ret

    def parse_args(self):
        for key in self.arg_keys:
            for di in self.src_block.data:
                if di['key'] == key:
                    self.args[key] = di['value']


class EmptyBlock(PytorchBlock):
    def to_pytorch_code(self):
        return ""


class Conv2D(PytorchBlock):
    def __init__(self, block: Block, output_name):
        super().__init__(block, output_name)
        self.mapping_name = "torch.nn.Conv2D"
        self.arg_keys = ["in_channels", "out_channels", "kernel_size", "stride", "padding"]


class MaxPooling2D(PytorchBlock):
    def __init__(self, block: Block, output_name):
        super().__init__(block, output_name)
        self.mapping_name = "torch.nn.MaxPool2d"
        self.arg_keys = ["kernel_size"]


class ReLU(PytorchBlock):
    def __init__(self, block: Block, output_name):
        super().__init__(block, output_name)
        self.mapping_name = "torch.nn.ReLU"
        self.arg_keys = []


class Linear(PytorchBlock):
    def __init__(self, block: Block, output_name):
        super().__init__(block, output_name)
        self.mapping_name = "torch.nn.Linear"
        self.arg_keys = ["in_features", "out_features"]


class Softmax2D(PytorchBlock):
    def __init__(self, block: Block, output_name):
        super().__init__(block, output_name)
        self.mapping_name = "torch.nn.Softmax2d"
        self.arg_keys = []


# class Concat(PytorchBlock):
#     def __init__(self, block: Block, output_name):
#         super().__init__(block, output_name)
#         self.mapping_name = "torch.stack"
#         self.arg_keys = ["in_channels", "out_channels", "kernel_size", "stride", "padding"]
#
# class ResInception(PytorchBlock):
#     def __init__(self, block: Block, output_name):
#         super().__init__(block, output_name)
#         self.mapping_name = "torch.nn.Conv2D"
#         self.arg_keys = ["in_channels", "out_channels", "kernel_size", "stride", "padding"]


if __name__ == '__main__':
    block = Block(
        "pxy is handsome",
        "Conv2D",
        "sb",
        {"in_channels": "1", "out_channels": "2", "kernel_size": "(3,3)", "stride": "1", "padding": "1"}
    )
    conv = Conv2D(block, "out1")
    print(conv.to_pytorch_code())
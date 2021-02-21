class Block:
    def __init__(self, b_id, name, text, data):
        self.b_id = b_id
        self.name = name
        self.text = text
        self.data = data
        self.input = []
        self.output = []
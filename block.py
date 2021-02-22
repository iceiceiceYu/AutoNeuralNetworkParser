class Block:
    def __init__(self, b_id, name, text, data):
        self.b_id = b_id
        self.name = name
        self.text = text
        self.data = data
        self.input = []
        self.output = []
        self.output_variable = None


    def __str__(self):
        return 'block info: [b_id: {}, name: {}, text: {}, data: {}]'.format(self.b_id, self.name, self.text, self.data)

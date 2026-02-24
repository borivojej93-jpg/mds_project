

class RackLimitError(Exception):
    def __init__(self, msg="Rack limit is reached!"):
        self.msg = msg
        super().__init__(self.msg)

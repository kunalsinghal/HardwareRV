class Circuit:
    def __init__(self, str):
        self.state = {}
    def verify(self):
        return True


x = Circuit('x')

print x.verify()

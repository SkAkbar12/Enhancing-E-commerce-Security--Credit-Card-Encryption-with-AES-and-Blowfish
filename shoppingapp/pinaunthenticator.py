
def otpaunthtnticate(p1, p2, p3, p4, p5, p6, pin):
    pins = [p1, p2, p3, p4, p5, p6]
    for i in range(len(pins)):
        if pins[i] != pin[i]:
            return False
    return True

class Data:
    def __init__(self):
        self.pins = list

    def pinaunthenticate(self, ll):
        print(self.pins)
        if len(ll) != len(self.pins):
            raise ValueError("Lengths of ll and pin must be equal")
        
        for i in range(len(ll)):
            if ll[i] != self.pins[i]:
                return False
        return True

list = []

def storingdata(pin):
    global list
    list = [digit for digit in pin]


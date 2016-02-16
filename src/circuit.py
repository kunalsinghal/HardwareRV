
class Circuit:
  def __init__(self, constraint):
    self.state = {}
    self.constraint = constraint.strip().split()

  def update(self, key, value):
    self.state[key] = value

  def value(self, key):
    try:
      return int(key)
    except:
      try:
        return self.state[key]
      except:
        if key == 'True':
          return True
        elif key == 'False':
          return False
        else:
          return None

  def verify(self):
    def isOperator(symbol):
      return True

    def getArity(symbol):
      return 2

    def evaluate(operator, args):
      return True

    stack = []

    for symbol in self.constraint:
      if isOperator(symbol):
        arity = getArity(symbol)
        if arity > len(stack):
          return False

        stack = stack[:-arity] + [ evaluate(operator, stack[-arity:]) ]
      else:
        val = self.value(symbol)
        if val is not None:
          stack.append(val)
        else:
          return False

    if len(stack) == 1:
      return True
    else:
      return False


if __name__ == '__main__':
  x = Circuit('x')
  print x.verify()

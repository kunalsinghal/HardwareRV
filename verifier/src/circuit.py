
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
    mapping = {
      '+': (2, lambda x: x[0] + x[1]),
      '-': (2, lambda x: x[0] - x[1]),
      '*': (2, lambda x: x[0] * x[1]),
      '/': (2, lambda x: x[0] / x[1]),
      '||': (2, lambda x: x[0] or x[1]),
      '&&': (2, lambda x: x[0] and x[1]),
      '>': (2, lambda x: x[0] > x[1]),
      '<': (2, lambda x: x[0] < x[1]),
      '>=': (2, lambda x: x[0] >= x[1]),
      '<=': (2, lambda x: x[0] <= x[1]),
      '!': (2, lambda x: not x[0])
    }

    def isOperator(symbol):
      return symbol in mapping

    def getArity(operator):
      return mapping[operator][0]

    def evaluate(operator, args):
      return mapping[operator][1](args)

    stack = []

    for symbol in self.constraint:
      if isOperator(symbol):
        arity = getArity(symbol)
        if arity > len(stack):
          return False

        stack = stack[:-arity] + [ evaluate(symbol, stack[-arity:]) ]
      else:
        val = self.value(symbol)
        if val is not None:
          stack.append(val)
        else:
          return False

    if len(stack) == 1 and stack[0] == True:
      return True
    else:
      return False


if __name__ == '__main__':
  c = Circuit('1 x <')
  c.update('x', 2)
  print c.verify()
  c.update('x', 0)
  print c.verify()

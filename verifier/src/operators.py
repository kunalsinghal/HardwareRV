mapping = {
  '+': (2, lambda x: x[0] + x[1], 5),
  '-': (2, lambda x: x[0] - x[1], 5),
  '*': (2, lambda x: x[0] * x[1], 6),
  '/': (2, lambda x: x[0] / x[1], 6),
  '||': (2, lambda x: x[0] or x[1], 2),
  '&&': (2, lambda x: x[0] and x[1], 3),
  '==': (2, lambda x: x[0] == x[1], 4),
  '!=': (2, lambda x: x[0] <> x[1], 4),
  '>': (2, lambda x: x[0] > x[1], 4),
  '<': (2, lambda x: x[0] < x[1], 4),
  '>=': (2, lambda x: x[0] >= x[1], 4),
  '<=': (2, lambda x: x[0] <= x[1], 4),
  '!': (2, lambda x: not x[0], 5)
}

# Three simple functions to consume the mapping dictionary
def isOperator(symbol):
  return symbol in mapping

def getArity(operator):
  return mapping[operator][0]

def evaluate(operator, args):
  return mapping[operator][1](args)
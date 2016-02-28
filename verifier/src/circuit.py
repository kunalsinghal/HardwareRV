# Circuit class emulates circuit of one property
# in FPGA. The assumptions here are that the description
# of input property is in postfix notation. We can easily support
# infix notation by writing a convertor later.;

class Circuit:
  def __init__(self, constraint):
    # state stores the values of various variables
    self.state = {}
    # constraint saves the property
    self.constraint = constraint.strip().split()

  # update the value of a certain variable
  def update(self, key, value):
    self.state[key] = value

  # gets value of a variable / integer / boolean
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
    # mapping contains description of every supported variable
    # FORMAT FOR DESCRIPTIONS:
    # (arity, Eval: lis -> value)
    # where Eval is the evaluation function
    # TODO: make a separate class for operators
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

    # Three simple functions to consume the mapping dictionary
    def isOperator(symbol):
      return symbol in mapping

    def getArity(operator):
      return mapping[operator][0]

    def evaluate(operator, args):
      return mapping[operator][1](args)

    stack = []

    # This is the standard postfix evaluation loop
    for symbol in self.constraint:
      if isOperator(symbol):
        arity = getArity(symbol)
        # Illegal property allways evaluates to False,
        # perhaps this should be catched during compilation
        if arity > len(stack):
          return False

        stack = stack[:-arity] + [ evaluate(symbol, stack[-arity:]) ]
      else:
        val = self.value(symbol)
        if val is not None:
          stack.append(val)
        # Incorrect time to verify, all variables are not set,
        # thus returns False
        else:
          return False

    if len(stack) == 1 and stack[0] == True:
      return True
    # Illegal property allways evaluates to False,
    else:
      return False


if __name__ == '__main__':
  c = Circuit('1 x <')
  c.update('x', 2)
  print c.verify()
  c.update('x', 0)
  print c.verify()

# mapping contains description of every supported variable
# FORMAT FOR DESCRIPTIONS:
# (arity, Eval: lis -> value)
# where Eval is the evaluation function
# TODO: make a separate class for operators
mapping = {
  '+': (2, lambda x: x[0] + x[1], 5),
  '-': (2, lambda x: x[0] - x[1], 5),
  '*': (2, lambda x: x[0] * x[1], 6),
  '/': (2, lambda x: x[0] / x[1], 6),
  '||': (2, lambda x: x[0] or x[1], 2),
  '&&': (2, lambda x: x[0] and x[1], 3),
  '>': (2, lambda x: x[0] > x[1], 4),
  '<': (2, lambda x: x[0] < x[1], 4),
  '>=': (2, lambda x: x[0] >= x[1], 4),
  '<=': (2, lambda x: x[0] <= x[1], 4),
  '!': (2, lambda x: not x[0], 5)
}

# Circuit class emulates circuit of one property
# in FPGA. The assumptions here are that the description
# of input property is in postfix notation. We can easily support
# infix notation by writing a convertor later.;

class Circuit:
  def infix_to_postfix(self, infixexpr):
    def getPref(operator):
      if operator == '(':
        return 1
      return mapping[operator][2]

    opStack = []
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
      if token == '(':
        opStack.append(token)

      elif token == ')':
        topToken = opStack.pop()
        while topToken != '(':
          postfixList.append(topToken)
          topToken = opStack.pop()

      elif token in mapping:
        while len(opStack) <> 0 and (getPerf(opStack[-1]) >= getPerf(token)):
          postfixList.append(opStack.pop())
        opStack.append(token)
      else:
        postfixList.append(token)

    while len(opStack) <> 0:
        postfixList.append(opStack.pop())
    return postfixList


  def __init__(self, constraint):
    # state stores the values of various variables
    self.state = {}

    # constraint saves the property
    self.infix = constraint.strip()
    self.constraint = self.infix_to_postfix(self.infix)

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
  c = Circuit('1 < x')
  print c.infix
  print c.constraint
  c.update('x', 2)
  print c.verify()
  c.update('x', 0)
  print c.verify()

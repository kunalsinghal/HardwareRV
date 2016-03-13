from jinja2 import Environment, PackageLoader
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

# Circuit class emulates circuit of one property/constraint
# in FPGA.

class Circuit:
  def __init__(self, constraint, updates={}, critical_pc=0):
    # state stores the values of various variables
    self.state = {}

    # constraint saves the property
    self.infix = constraint.strip()
    self.constraint = self.infix_to_postfix(self.infix)

    self.updates = updates
    self.critical_pc = critical_pc
    variables = updates.values()
    self.var_index = {variables[i]: str(i) for i in xrange(len(variables))}

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

  def print_object(self):
    print 'Printing object', self
    print self.infix
    print self.updates
    print self.critical_pc
    print self.state
    print self.var_index
    print '===================='

  def get_hdl(self, name):
    def hdl(symbol):
      if isOperator(symbol):
        return symbol
      try:
        ret = hex(int(symbol))[2:]
        ret = '0' * (8 - len(ret)) + ret
        return 'x"' + ret + '"'
      except:
        return 'temp_var(' + self.var_index[symbol] + ')'

    env = Environment(loader=PackageLoader('src', 'templates'))
    circuit_hdl_template = env.get_template('circuit_hdl_template')
    update_variable_template = env.get_template('update_variable_template')
    check_template = env.get_template('check_template')

    circuit_logic = ''
    for key in self.updates:
      circuit_logic += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    condition = ' '.join(map(hdl, self.infix.split()))
    circuit_logic += check_template.render(pc=self.critical_pc, condition=condition)
    return circuit_hdl_template.render(name=name, circuit_logic=circuit_logic)

if __name__ == '__main__':
  c = Circuit('1 < x')
  print c.infix
  print c.constraint
  c.update('x', 2)
  print c.verify()
  c.update('x', 0)
  print c.verify()

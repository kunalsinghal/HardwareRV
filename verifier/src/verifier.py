from jinja2 import Environment, PackageLoader
from operators import isOperator

class Verifier(object):
  def __init__(self, constraint, name):
    self.constraint = constraint.strip()
    self.name = name

  # must overwrite
  def get_hdl(self):
    pass

class PropositionalVerifier(Verifier):
  def __init__(self, constraint, name, updates={}, enables=[], disables=[]):
    super(PropositionalVerifier, self).__init__(constraint, name)
    self.updates = updates
    variables = list(set(updates.values()))
    self.var_index = {variables[i]: str(i) for i in xrange(len(variables))}
    self.enables = enables
    self.disables = disables

  def get_hdl(self):
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
    enable_template = env.get_template('enable_template')
    update_variable_template = env.get_template('update_variable_template')
    check_template = env.get_template('check_template')

    circuit_logic = ''

    if len(self.enables) > 0:
      condition = ' || '.join([
        ('instr_data = x"%s"' % program_counter) for program_counter in self.enables
      ])

      circuit_logic += enable_template.render(
        condition=condition, value='1'
      )

    if len(self.disables) > 0:
      condition = ' || '.join([
        ('instr_data = x"%s"' % program_counter) for program_counter in self.enables
      ])

      circuit_logic += enable_template.render(
        condition=condition, value='0'
      )

    for key in self.updates:
      circuit_logic += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    for key in self.updates:
      circuit_logic += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    condition = ' '.join(map(hdl, self.constraint.split()))
    circuit_logic += check_template.render(condition=condition)
    return circuit_hdl_template.render(name=self.name, circuit_logic=circuit_logic)


if __name__ == '__main__':
  x = PropositionalVerifier('a', 'b')
  print x.constraint, x.name
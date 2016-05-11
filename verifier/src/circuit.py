from jinja2 import Environment, PackageLoader
import operators
from ltl_to_ba import ltl_to_ba
import tokenizer

class Circuit(object):
  def __init__(self, constraint, name):
    self.constraint = constraint.strip()
    self.name = name

  # must overwrite
  def get_hdl(self):
    pass

  def symbol_to_hdl(self, symbol):
    def sanitize(x):
      if x == '==':
        return '='
      elif x == '&&':
        return 'AND'
      elif x == '||':
        return 'OR'
      elif x == '!':
        return 'NOT'
      else:
        return x

    if operators.isOperator(symbol) or symbol in ['(', ')']:
      return sanitize(symbol)
    elif symbol == 'true':
      return "'1'"
    elif symbol == 'false':
      return "'0'"
    try:
      ret = hex(int(symbol))[2:]
      ret = '0' * (8 - len(ret)) + ret
      return 'x"' + ret + '"'
    except:
      return 'temp_var(' + self.var_index[symbol] + ')'

class PropositionalCircuit(Circuit):
  def __init__(self, constraint, name, updates={}, enables=[], disables=[]):
    super(PropositionalCircuit, self).__init__(constraint, name)
    self.updates = updates
    variables = list(set(updates.values()))
    self.var_index = {variables[i]: str(i) for i in xrange(len(variables))}
    self.enables = enables
    self.disables = disables

  def get_hdl(self):
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
        ('instr_data = x"%s"' % program_counter) for program_counter in self.disables
      ])

      circuit_logic += enable_template.render(
        condition=condition, value='0'
      )

    for key in self.updates:
      circuit_logic += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    condition = ' '.join(map(self.symbol_to_hdl, tokenizer.get_tokens(self.constraint)))
    circuit_logic += check_template.render(condition=condition)
    return circuit_hdl_template.render(name=self.name, circuit_logic=circuit_logic)


class LTLCircuit(Circuit):
  def __init__(self, constraint, name, updates={}, enables=[], disables=[], resets=[]):
    super(LTLCircuit, self).__init__(constraint, name)
    self.updates = updates
    variables = list(set(updates.values()))
    self.var_index = {variables[i]: str(i) for i in xrange(len(variables))}
    self.enables = enables
    self.disables = disables
    self.resets = resets
    self.automaton = ltl_to_ba(constraint)

  def get_automaton(self):
    def automaton_to_hdl(transitions):
      def transition_to_hdl(transition):
        condition, source = transition
        condition = ' '.join(map(self.symbol_to_hdl, tokenizer.get_tokens(condition)))
        return '(rq(%d) AND (%s))' % (source, condition)
      return '(%s)' % (' OR '.join(map(transition_to_hdl, transitions)))

    automaton = self.automaton
    automaton = [automaton[i] for i in xrange(len(automaton))]

    shift_logic = ' & '.join(map(automaton_to_hdl, automaton))
    return 'r <= %s' % shift_logic

  def get_hdl(self):
    env = Environment(loader=PackageLoader('src', 'templates'))
    ltl_circuit_hdl_template = env.get_template('ltl_circuit_hdl_template')
    enable_template = env.get_template('enable_template')
    reset_template = env.get_template('reset_template')
    update_variable_template = env.get_template('update_variable_template')

    zero_value = '"%s"' % ('0' * len(self.automaton))
    initial_value = '"1%s"' % ('0' * (len(self.automaton)-1))

    enables = ''
    if len(self.enables) > 0:
      condition = ' || '.join([
        ('instr_data = x"%s"' % program_counter) for program_counter in self.enables
      ])
      enables += enable_template.render(
        condition=condition, value='1'
      )

    if len(self.disables) > 0:
      condition = ' || '.join([
        ('instr_data = x"%s"' % program_counter) for program_counter in self.disables
      ])
      enables += enable_template.render(
        condition=condition, value='0'
      )

    resets = ''
    if len(self.resets) > 0:
      condition = ' || '.join([
        ('instr_data = x"%s"' % program_counter) for program_counter in self.resets
      ])
      resets += reset_template.render(
        condition=condition, initial_value=initial_value
      )

    updates = ''
    for key in self.updates:
      updates += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    return ltl_circuit_hdl_template.render(
      name=self.name,
      enables=enables,
      updates=updates,
      resets=resets,
      automaton=self.get_automaton(),
      automaton_sz=len(self.automaton)-1,
      zero_value=zero_value,
      initial_value=initial_value
    )


if __name__ == '__main__':
  x = LTLCircuit('aa U b', 'prop1', {'1': 'aa', '21': 'b', '44': 'aa', '45': 'b'}, [22, 46], [33], [55, 78])
  print x.get_hdl()
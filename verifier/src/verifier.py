from jinja2 import Environment, PackageLoader
import operators
from ltl_to_ba import ltl_to_ba
import tokenizer

class Verifier(object):
  def __init__(self, constraint, name):
    self.constraint = constraint.strip()
    self.name = name

  # must overwrite
  def get_hdl(self):
    pass

  def symbol_to_hdl(self, symbol):
    if operators.isOperator(symbol) or symbol in ['(', ')']:
      return symbol
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

class PropositionalVerifier(Verifier):
  def __init__(self, constraint, name, updates={}, enables=[], disables=[]):
    super(PropositionalVerifier, self).__init__(constraint, name)
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


class LTLVerifier(Verifier):
  def __init__(self, constraint, name, updates={}, enables=[], disables=[]):
    super(LTLVerifier, self).__init__(constraint, name)
    self.updates = updates
    variables = list(set(updates.values()))
    self.var_index = {variables[i]: str(i) for i in xrange(len(variables))}
    self.enables = enables
    self.disables = disables
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
    update_variable_template = env.get_template('update_variable_template')

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

    updates = ''
    for key in self.updates:
      updates += update_variable_template.render(
        pc=key, var_id=self.var_index[self.updates[key]]
      )

    return ltl_circuit_hdl_template.render(
      name=self.name,
      enables=enables,
      updates=updates,
      automaton=self.get_automaton(),
      automaton_sz=len(self.automaton)-1
    )


if __name__ == '__main__':
  x = LTLVerifier('a U b', 'prop1', {'1': 'a', '21': 'b', '44': 'a', '45': 'b'}, [22, 46], [33])
  print x.get_hdl()
import sys
from jinja2 import Environment, PackageLoader
from circuit import PropositionalCircuit, LTLCircuit

class Monitor(object):
  def __init__(self, meta):
    with open(meta, 'r') as meta:
      lines = filter(None, map(lambda x: x.strip(), meta.readlines()))

    circuits = []
    idx = 0
    constraint = None
    enables = []
    disables = []
    updates = {}
    resets = []

    while idx < len(lines):
      parts = lines[idx].split()
      if parts[0] in ['propositional:', 'ltl:']:
        if constraint: # deal with the previous constraint
          if constraint[0] == 'propositional':
            circuits.append(PropositionalCircuit(
              constraint[1],
              'circuit_%d' % len(circuits),
              updates,
              enables,
              disables))
          else:
            pass
        # Overwrite new constraint
        constraint = (parts[0][:-1] , ' '.join(parts[1:]))
        disables = []
        enables = []
        updates = {}
        resets = []

      elif parts[0] == 'enable:':
        enables.append(parts[1])
      elif parts[0] == 'disable:':
        disables.append(parts[1])
      elif parts[0] == 'reset:':
        resets.append(parts[1])
      elif parts[0] == 'update:':
        updates[parts[1]] = parts[2]
      else:
        raise Exception('Incorrect meta file')
      idx += 1

    if constraint: # final constraint
      if constraint[0] == 'propositional':
        circuits.append(PropositionalCircuit(
          constraint[1],
          'circuit_%d' % len(circuits),
          updates,
          enables,
          disables))
      else:
        pass

    self.circuits = circuits
    self.meta = meta

  def get_wrapper_hdl(self):
    env = Environment(loader=PackageLoader('src', 'templates'))
    wrapper_component_template = env.get_template('wrapper_component_template')
    circuit_component_template = env.get_template('circuit_component_template')
    portmapping_template = env.get_template('portmapping_template')


    components = ''
    portmappings = ''
    for i in xrange(len(self.circuits)):
      components += circuit_component_template.render(
        name=self.circuits[i].name
      )
      portmappings += portmapping_template.render(
        label='I%d' % i,
        name=self.circuits[i].name,
        index=i
      )

    combined_result = ' OR '.join(map(
      lambda i: ('assert_out_temp(%d)' % i),
      xrange(len(self.circuits))
    ))

    return wrapper_component_template.render(
      components=components,
      portmappings=portmappings,
      combined_result=combined_result
    )

  def get_circuits_hdl(self):
    return [(circuit.name, circuit.get_hdl()) for circuit in self.circuits]
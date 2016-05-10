import sys
from verifier import PropositionalCircuit, LTLCircuit

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

  def __str__(self):
    return  '\n\n------------------------------\n\n'.join(
      [self.circuits[i].get_hdl() for i in xrange(len(self.circuits))]
    )

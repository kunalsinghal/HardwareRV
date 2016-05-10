import sys
from verifier import PropositionalCircuit, LTLCircuit


try:
  TEST_BASE = sys.argv[1].strip('/')
  # strip extra '/' from the end of the string if any
except:
  print 'Please provide path of test directory as first argument'
  sys.exit()


with open(TEST_BASE + '/meta', 'r') as meta:
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

print constraint
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

for i in xrange(len(circuits)):
  print circuits[i].get_hdl()
  print '-----------------------------------'
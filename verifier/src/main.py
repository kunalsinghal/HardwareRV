import sys
from verifier import PropositionalVerifier

try:
  TEST_BASE = sys.argv[1].strip('/')
  # strip extra '/' from the end of the string if any
except:
  print 'Please provide path of test directory as first argument'
  sys.exit()


with open(TEST_BASE + '/meta', 'r') as meta:
  lines = map(lambda x: x.strip(), meta.readlines())

circuits = []

idx = 2 # line number of first propoerty in meta file

while idx < len(lines):
  propoerty = lines[idx].strip()
  idx += 1
  critical_pc = lines[idx].strip()
  idx += 1
  updates = {}
  while idx < len(lines) and lines[idx].strip() != '':
    pc, variable = lines[idx].split()
    updates[pc] = variable
    idx += 1

  circuits.append(PropositionalVerifier(propoerty, 'circuit_%d' % len(circuits), updates, [critical_pc, critical_pc], [critical_pc, critical_pc]))

for i in xrange(len(circuits)):
  print circuits[i].get_hdl()

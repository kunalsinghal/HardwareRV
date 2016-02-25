import sys
from circuit import Circuit

try:
  TEST_BASE = sys.argv[1].strip('/')
  # strip extra '/' from the end of the string if any
except:
  print 'Please provide path of test directory as first argument'
  sys.exit()


meta = open(TEST_BASE + '/meta', 'r')
lines = map(lambda x: x.strip(), meta.readlines())

idx = 0
for line in lines:
  if line == 'Properties':
    propertyIdx = idx + 2
  elif line == 'Update Tuples':
    tupleIdx = idx + 2
  idx += 1

meta.close()


circuits = []
pc_to_circuits = {}

idx = propertyIdx

while lines[idx] != 'Update Tuples':
  circuits.append(Circuit(lines[idx]))

  for pc in map(int, lines[idx+1].split()):
    try:
      pc_to_circuits[pc].append(len(circuits)-1)
    except:
      pc_to_circuits[pc] = [len(circuits)-1]

  idx += 3

print circuits
print pc_to_circuits

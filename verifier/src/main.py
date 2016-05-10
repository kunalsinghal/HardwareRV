import sys
from monitor import Monitor

try:
  TEST_BASE = sys.argv[1].strip('/')
  # strip extra '/' from the end of the string if any
except:
  print 'Please provide path of test directory as first argument'
  sys.exit()

monitor = Monitor(TEST_BASE + '/meta')

with open(TEST_BASE + '/assertion.vhdl', 'w') as assertion:
  assertion.write(monitor.get_wrapper_hdl())

circuits = monitor.get_circuits_hdl()

for circuit in circuits:
  with open('%s/%s.vhdl' % (TEST_BASE, circuit[0]), 'w') as circuit_file:
    circuit_file.write(circuit[1])
import sys
from monitor import Monitor

try:
  TEST_BASE = sys.argv[1].strip('/')
  # strip extra '/' from the end of the string if any
except:
  print 'Please provide path of test directory as first argument'
  sys.exit()

monitor = Monitor(TEST_BASE + '/meta')
print monitor

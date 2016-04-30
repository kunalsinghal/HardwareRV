import subprocess
import re

def parse_ba(ba_string):
	lines = filter(None, map(str.strip, ba_string.split('\n')))
	states = []
	state_id = {}

	# mapping states to numbers
	for line in lines:
		if line[-1] == ':':
			state_id[line[:-1]] = len(states)
			states.append(line[:-1])

	transition = dict(map(lambda x: [state_id[x], []], states))

	for line in lines[1:]:
		if line[:-1] in states:
			source = state_id[line[:-1]]
		elif line[:2] == '::':
			matches = re.search(r':: (.+?) -> goto (.+)', line)
			transition[source].append((matches.group(1), state_id[matches.group(2).strip()]))
		elif line == 'skip':
			transition[source].append(('true', source))
	print transition
	print state_id


def ltl_to_ba_string(ltl_formula):
	return subprocess.check_output(['ltl3ba', '-f', '"' + ltl_formula + '"'])

if __name__ == '__main__':
	ba_string = ltl_to_ba_string('a -> F b')
	parse_ba(ba_string)
from StringIO import StringIO
import tokenize

def get_tokens(string):
	def sanitize(s):
		return s.replace('||', 'or').replace('&&', 'and')
	def desanitize(s):
		if s == 'and':
			return '&&'
		elif s == 'or':
			return '||'
		else:
			return s

	tokens = tokenize.generate_tokens(StringIO(sanitize(string)).readline)
	tokens = map(lambda x: desanitize(x[1]), tokens)
	return filter(None, tokens)

if __name__ == '__main__':
	print get_tokens('(!a) || (a && b)')


import sys
import os
import csv


class ParseError(Exception):
	pass


def parse(s, chars, transform):
	out = ''
	block = ''
	mode = 'normal'
	for c in s:
		if mode == 'normal':
			if c == chars[0]:
				mode = 'maybe block'
			else:
				out += c
		elif mode == 'maybe block':
			if c == chars[0]:
				mode = 'block'
			else:
				out += chars[0]
				out += c
				mode = 'normal'
		elif mode == 'block':
			if c == chars[1]:
				mode = 'maybe endblock'
			else:
				block += c
		elif 'maybe endblock':
			if c == chars[1]:
				out += transform(block.strip())
				block = ''
				mode = 'normal'
			else:
				block += chars[1]
				block += c
				mode = 'normal'
	if mode == 'maybe block':
		out += chars[0]
	elif mode == 'maybe endblock':
		out += chars[1]
	elif mode != 'normal':
		raise ParseError(s)
	return out


def apply_bold(block):
	def transform(s):
		return '<text:span text:style-name="Bold">%s</text:span>' % s
	return parse(block, '**', transform)


def get_translation(path):
	with open(path) as fh:
		rows = csv.reader(fh)
		translation = {row[0].strip(): apply_bold(row[1].strip()) for row in rows}

	translation['de'] = os.path.splitext(os.path.basename(path))[0]

	if translation['de'] in ['ar', 'fa']:
		translation.update({
			'lr': 'rl',
			'page-start-margin': 'page-end-margin',
			'5217*': '5386*',
			'5386*': '5217*',
			'left': 'right',
			'start': 'end',
			'none': 'translate(128,0) scale(-1,1)',
		})
	else:
		translation.update({
			'lr': 'lr',
			'page-start-margin': 'page-start-margin',
			'5217*': '5217*',
			'5386*': '5386*',
			'left': 'left',
			'start': 'start',
			'none': 'none',
		})

	return translation


if __name__ == '__main__':
	translation = get_translation(sys.argv[2])

	with open(sys.argv[1]) as fh:
		for lineno, line in enumerate(fh):
			try:
				print(parse(line.rstrip(), '{}', lambda s: translation[s]))
			except ParseError:
				raise ParseError('ParseError in line %i' % lineno)

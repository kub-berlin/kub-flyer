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
		return f'<strong>{s}</strong>'
	return parse(block, '**', transform)


def get_translation(path):
	with open(path) as fh:
		rows = csv.reader(fh)
		translation = {row[0].strip(): row[1].strip() for row in rows}

	translation['de'] = os.path.splitext(os.path.basename(path))[0]

	if translation['de'] in ['ar', 'fa']:
		translation.update({
			'ltr': 'rtl',
			'start': 'right',
			'end': 'left',
			'font': '"Noto Naskh Arabic", "Noto Sans"',
		})
	else:
		translation.update({
			'ltr': 'ltr',
			'start': 'left',
			'end': 'right',
			'font': '"Noto Sans"',
		})

	if translation['de'] == 'fr':
		translation['extra-css'] = '.box { font-size: 8pt; }'
	else:
		translation['extra-css'] = ''

	return translation


if __name__ == '__main__':
	translation = get_translation(sys.argv[2])

	def translate(s):
		return apply_bold(translation.get(s) or s)

	with open(sys.argv[1]) as fh:
		for lineno, line in enumerate(fh):
			try:
				print(parse(line.rstrip(), '{}', translate))
			except ParseError:
				raise ParseError('ParseError in line %i' % lineno)

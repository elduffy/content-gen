#!/usr/bin/python
from sys import stderr

def readFromTable(table, srcFile):
	reader = open(srcFile,'r')
	lineCnt = 0
	for line in reader.readlines():
		lineCnt += 1
		toks = line.split(',')
		if len(toks) != table.columnCount() or len(toks) == 0:
			stderr.write('Error reading \'{0}\' on line {1}\n'.format(srcFile, lineCnt))
			continue
		row = TableRow()
		for tok in toks:
			sep = tok.find(':')
			if sep < 0:
				row.addColumn(tok)
			else:
				text = tok[:sep]
				url = tok[sep+1:]
				url = url.replace('"','')
				row.addColumn(HREF(text, url))
		table.addRow(row)
	

if __name__ == '__main__':
	exit(0)

gradTable = Table(None, 'Code', 'Title', 'Professor')
readFromTable(gradTable, 'misc/grad_courses.src')

ugcsTable = Table(None, 'Code', 'Title', 'Professor')
readFromTable(ugcsTable, 'misc/ugcs_courses.src')

ugmathTable = Table(None, 'Code', 'Title', 'Professor')
readFromTable(ugmathTable, 'misc/ugmath_courses.src')



gen.addNodes([
SectionStart('bordered'),
AStart(name='grad_cs'),
Header('Graduate Computer Science (UIUC).', 3),
AEnd(),

gradTable,

AStart(name='ug_cs'),
Header('Undergraduate Computer Science (UTD).', 3),
AEnd(),

ugcsTable,

AStart(name='ug_math'),
Header('Undergraduate Mathematics (UTD).', 3),
AEnd(),

ugmathTable,

SectionEnd()
])

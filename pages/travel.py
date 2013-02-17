#/usr/bin/python
# -*- coding: UTF-8 -*-
from sys import exit

if __name__ == '__main__':
	exit(0)

PHOTO_DIR = '../photos/'

def generatePhotoTable():
	result = Table()
	global PHOTO_DIR
	COLS = 2
	photos = [
	('montmartre.jpg', 'Montmartre, Paris, France'),	('geneva.jpg', 'Geneva, Switzerland'),
	('bern.jpg', 'Bern, Switzerland'),			('interlaken.jpg', 'Interlaken, Switzerland'),
	('eiger.jpg', 'Eiger from Grindelwald, Switzerland'),	('zurich.jpg', 'Z&#xFCrich, Switzerland'),
	('rapperswil.jpg', 'Rapperswil, Switzerland'),		('zug.jpg', 'Der Zugerberg, Switzerland'),
	('phoenix_park.jpg', 'Phoenix Park, Dublin, Ireland'),	('bath.jpg', 'Bath, UK'),
	('windermere.jpg', 'Lake Windermere, UK'),		('cambridge.jpg', 'Cambridge, UK')
	]
	
	curRow = TableRow()
	colCount = 0
	for (img,desc) in photos:
		colCount += 1
		img = PHOTO_DIR + str(img)
		col = DivStartEnd(NodeList(Img(img, 'gallery'), CenterStartEnd(desc)), 'gallery')
		curRow.addColumn(col)
		
		if colCount % COLS == 0:
			result.addRow(curRow)
			curRow = TableRow()
	return result

countries = ['United States', 'Mexico', 'France', 'Switzerland', 'United Kingdom', 'Ireland', 'Canada']
countries.sort()

photos = generatePhotoTable()

gen.addNodes([
SectionStart('bordered'),
PStartEnd('''I travel as often as I am able. Historically, most of my adventuring has
been throughout the United States but in recent years I've had the opportunity
to explore other countries. Here is my (hopefully) ever-expanding list of
countries visited.'''),
UList('ast', *countries),
Header('Select Photos',3),
CenterStartEnd(photos),
SectionEnd()
])

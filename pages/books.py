#/usr/bin/python
# -*- coding: UTF-8 -*-

if __name__ == '__main__':
	exit(0)

## Books Section
books = PageSection('Books', 'bordered', printHeader=False)
table = Table('bordered', 'Title', 'Author', 'ISBN-13')
table.addRow(TableRow('bordered','A Confederacy of Dunces', 'John Kennedy Toole',
	HREF('978-0802130204', 'http://www.amazon.com/dp/0802130208')))
table.addRow(TableRow('bordered','Applied Cryptography', 'Bruce Schneier',
	HREF('978-0471117094', 'http://www.amazon.com/dp/0471117099')))
table.addRow(TableRow('bordered','Effective Java', 'Joshua Bloch',
	HREF('978-0321356680', 'http://www.amazon.com/dp/0321356683')))
table.addRow(TableRow('bordered','Ender\'s Game', 'Orson Scott Card',
	HREF('978-0812550702', 'http://www.amazon.com/dp/0812550706')))
table.addRow(TableRow('bordered','G&#246;del, Escher, Bach: An Eternal Golden Braid', 'Douglas R. Hofstadter',
	HREF('978-0465026562', 'http://www.amazon.com/dp/0465026567')))
table.addRow(TableRow('bordered','Infinite Jest', 'David Foster Wallace',
	HREF('978-0316066525', 'http://www.amazon.com/dp/0316066524')))
table.addRow(TableRow('bordered','Psychopath Test, The', 'Jon Ronson',
	HREF('978-1594485756', 'http://www.amazon.com/dp/1594485755')))

books.addNode(CenterStartEnd(table))
gen.addNodes([

PStartEnd('These are some books I highly recommend. They run the gamut from the fictional to the technical, but each is well worth the read.'),
books

])

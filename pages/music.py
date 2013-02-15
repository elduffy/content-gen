#/usr/bin/python


if __name__ == '__main__':
	exit(0)

table = Table('bordered', 'Title', 'Composer', 'Type', 'File')
list1 = NodeList(HREF('MP3','../music/recordings/buckets_of_rain.mp3'),
	HREF('WAV','../music/recordings/buckets_of_rain.wav'))
table.addRow(TableRow('bordered', 'Buckets of Rain', 'Bob Dylan', 'Instrumental/Exerpt', list1))

gen.addNodes([
SectionStart('bordered'),
PStart(),
'''
I have been a musician for well over a decade now and I consider music
to be an integral part of my life and my identity. I was an Arkansas all-state
clarinetist for three consecutive years and I am a competent pianist.
Nowadays my passion is for the guitar, of which I own three including a steel-string acoustic,
a Les Paul electric, and a classical.  In addition to performing, I also enjoy musical
composition.  This page will serve as a grounds for publishing my thoughts, compositions,
recordings, and any musical miscellanea that I wish to share with others.
''',
PEnd(),
Header("Recordings.",3),
table,

SectionEnd()
])

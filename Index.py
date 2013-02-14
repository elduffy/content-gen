#!/usr/bin/python
from sys import argv, exit, stdout
import os.path
import datetime, date, time, timedelta
import ContentGen as cg

#if not __name__ == '__main__':
#	exit(0)

OUT = stdout
GENDM = False

if len(argv) == 2:
	if os.path.exists(argv[1]):
		mtime = time.ctime(os.path.getmtime(argv[1]))
		
	try:
		OUT = open(argv[1],'rw')
	except IOError,ioe:
		stderr.write("Couldn't open {0} for r/w access.".format(argv[1]))
		exit(1)
	

IMG_ME_SRC = 'photos/me.jpg'
NAME = 'Eric L Duffy'

personal = cg.PageSection('Personal', 'bordered')
personal.startPara()
personal.addText('My name is Eric Duffy. I am a researcher and student at the ')
personal.addHREF('University of Illinois at Urbana-Champaign', 'http://www.illinois.edu/')
personal.addText('. I work in the ')
personal.addHREF('Illinois Security Lab', 'http://seclab.illinois.edu/')
personal.addText(' under ')
personal.addHREF('Dr. Carl Gunter', 'http://cgunter.web.cs.illinois.edu/')
personal.addText('. My research interests are mostly related to computer and network security, but also\
 include all things regarding computation and mathematics. I enjoy ')
personal.addHREF('playing music', 'pages/music.htm')
personal.addText(',')
personal.addHREF('traveling', 'pages/travel.htm')
personal.addText(', working on various ')
personal.addHREF('projects', 'pages/projects.htm')
personal.addText(' and spending time outdoors.')
personal.endPara()

gen = cg.ContentGenerator(stdout)
gen.addNodes([
cg.DocStart(),
cg.PageTitle(),
cg.LinkCSS(),
cg.BodyStart(),
cg.Img(IMG_ME_SRC, 'floatright'),
cg.Header(NAME, 1),

personal,


cg.BodyEnd(),
cg.DocEnd()
])

gen.generateHTML()

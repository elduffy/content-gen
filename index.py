#!/usr/bin/python
from sys import argv, exit, stdout
import os.path
import ContentGen as cg

if __name__ == '__main__':
	exit(0)

IMG_ME_SRC = 'photos/me.jpg'
NAME = 'Eric L Duffy'

personal = cg.PageSection('Personal', 'bordered')
personal.startPara()
personal.addNodes([
'My name is Eric Duffy. I am a researcher and student at the ',
cg.HREF('University of Illinois at Urbana-Champaign', 'http://www.illinois.edu/'),
'. I work in the ',
cg.HREF('Illinois Security Lab', 'http://seclab.illinois.edu/'),
' under ',
cg.HREF('Dr. Carl Gunter', 'http://cgunter.web.cs.illinois.edu/'),
'. My research interests are mostly related to computer and network security, but also\
 include all things regarding computation and mathematics. I enjoy ',
cg.ScriptRef('playing music', 'pages/music.py'),
',',
cg.ScriptRef('traveling', 'pages/travel.py'),
', working on various ',
cg.ScriptRef('projects', 'pages/projects.py'),
' and spending time outdoors.'
])
personal.endPara()

gen.addNodes([
cg.Img(IMG_ME_SRC, 'floatright'),
personal,

])


#!/usr/bin/python
from sys import argv, exit, stdout
import os.path
import ContentGen as cg

if __name__ == '__main__':
	exit(0)

IMG_ME_SRC = 'photos/me.jpg'

## Personal Info Section
personal = PageSection('Personal', 'bordered')
personal.startPara()
personal.addNodes([
'My name is Eric Duffy. I am a researcher and student at the ',
HREF('University of Illinois at Urbana-Champaign', 'http://www.illinois.edu/'),
'. I work in the ',
HREF('Illinois Security Lab', 'http://seclab.illinois.edu/'),
' under ',
HREF('Dr. Carl Gunter', 'http://cgunter.web.cs.illinois.edu/'),	
'. My research interests are mostly related to computer and network security, but also\
 include all things regarding computation and mathematics. I enjoy ',
ScriptRef('playing music', 'pages/music.py'),
', ',
ScriptRef('traveling', 'pages/travel.py'),
', working on various ',
ScriptRef('projects', 'pages/projects.py'),
' and spending time outdoors.'
])
personal.endPara()

## Occupation History Section
occup = PageSection('Occupational History', 'bordered')
# UIUC
occup.addNodes([
PStart(),
BoldStart(),
HREF('The University of Illinois at Urbana-Champaign', 'http://www.illinois.edu'),
BoldEnd(),
' - Research Assistant & Teaching Assistant (2011-Present). ',
HREF('Urbana, Illinois.', 'http://maps.google.com/maps?ll=40.102039,-88.229927&z=14'),
PEnd(),
PStart(cls='n'),
'I study under Dr. Carl Gunter in the Illinois Security Lab.  My current research relates to healthcare IT security, vulnerability research and general system security.  I am an investigator on the ',
HREF('SHARPS', 'http://sharps.org'),
' project. I also helped teach Numerical Analysis (CS 450) in Fall 2011.',
PEnd()
])

# Raytheon-SI
occup.addNodes([
PStart(),
BoldStart(),
HREF('Raytheon-SI Government Solutions', 'http://www.raytheon.com'),
BoldEnd(),
' - Graduate Vulnerability Research Intern (Summer 2012). ',
HREF('Baltimore-Washington, Maryland.', 'http://maps.google.com/maps?ll=39.114287,-76.777902&z=10'),
PEnd(),
PStart(cls='n'),
'Vulnerability research using modern tools and methods including fuzzing, static analysis, dynamic analysis, virtualization, debugging and much, much more.',
PEnd()
])

# Cerner
occup.addNodes([
PStart(),
BoldStart(),
HREF('Cerner Corporation', 'http://www.cerner.com'),
BoldEnd(),
' - Software Engineer (2010-2011). ',
HREF('Kansas City, Missouri.', 'http://maps.google.com/maps?ll=39.100226,-94.581694&z=14'),
PEnd(),
PStart(cls='n'),
'Providing support for Cerner Millennium including memory dump analysis, network analysis, developing debugging tools, and working closely with clients.',
PEnd()
])

# UTD
occup.addNodes([
PStart(),
BoldStart(),
HREF('The University of Texas at Dallas', 'http://www.utdallas.edu'),
BoldEnd(),
'- Help Desk, CS Tutor, Computer Lab, etc (2006-2010). ',
HREF('Richardson, Texas.', 'http://maps.google.com/maps?ll=32.986492,-96.749137&z=15'),
PEnd(),
PStart(cls='n'),
'A plethora of responsibilities such as Windows/*nix administration, client support, fundraising, and anything else that pays the bills.',
PEnd()
])

## Educational History Section
educa = PageSection('Educational History', 'bordered')
educa.addNodes([
PStart(),
BoldStart(),
HREF('The University of Illinois at Urbana-Champaign', 'http://www.illinois.edu'),
' - M.S., Computer Science (2013). (',
ScriptRef('Courses', 'pages/courses.py', 'grad_cs'),
') ',
BoldEnd(),
PEnd()
])






## insert image above the header(s)
idx = gen.findType(BodyStart)
gen.insertNode(idx + 1, Img(IMG_ME_SRC, 'floatright'))
gen.addNode(personal)
gen.addNode(Break())
gen.addNode(occup)
gen.addNode(Break())
gen.addNode(educa)

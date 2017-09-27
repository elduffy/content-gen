#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sys import argv, exit, stdout

if __name__ == '__main__':
	exit(0)

IMG_ME_SRC = 'photos/me.jpg'

## Personal Info Section
personal = PageSection('Personal', 'bordered')
personal.addNodes([
PStartEnd(NodeList(
'My name is Eric Duffy. I am a software engineer living in '
' Austin, TX. I enjoy ',
ScriptRef('playing music', 'pages/music.py'),
', ',
ScriptRef('traveling', 'pages/travel.py'),
', working on various ',
ScriptRef('projects', 'pages/projects.py'),
', and spending time outdoors.'))
])


## Occupation History Section
occup = PageSection('Occupational History', 'bordered')
montrealLocation = 'https://maps.google.com/maps?ll=45.520301,-73.619492&z=11'
# Google
occup.addNodes([
PStartEnd(NodeList(
BoldStartEnd(HREF('Google', 'https://google.com')),
' - Software Developer, Security (2015 - 2017). ',
HREF('Montréal, Québec, Canada.', montrealLocation),
PStartEnd(NodeList('I worked on Google\'s security infrastructure in order to make the web a safer place.',
' I wrote software for an automated system that scans the world\'s web pages for malicious content.'), cls='n')
))
])

# GWAVA
occup.addNodes([
PStartEnd(NodeList(
BoldStartEnd(HREF('GWAVA, Inc.', 'http://gwava.com')), 
' - Software Engineer (2013 - 2015). ',
HREF('Montréal, Québec, Canada.', montrealLocation),
PStartEnd(NodeList(
'I lead a small but talented team developing and maintaining GWAVA\'s Retain archiving product.',
' We developed software in Java and Scala using enterprise JVM technologies such as Apache Tomcat, Spring, and Hibernate.',
), cls='n')
))
])

# UIUC
occup.addNodes([
PStartEnd(NodeList(
BoldStartEnd(HREF('The University of Illinois at Urbana-Champaign', 'http://www.illinois.edu')),
' - Research Assistant & Teaching Assistant (2011-2013). ',
HREF('Urbana, Illinois, USA.', 'https://maps.google.com/maps?ll=40.102039,-88.229927&z=14'),
PEnd(),
PStart(cls='n'),
'I studied under ',
HREF('Dr. Carl Gunter','http://cgunter.web.cs.illinois.edu/'),
' in the ',
HREF('Illinois Security Lab', 'http://seclab.illinois.edu/'),
'.  My research was related to healthcare IT security, vulnerability research and general system security.  I was an investigator on the ',
HREF('SHARPS', 'http://sharps.org'),
' project. See our publication in ',
HREF('HealthTech 2013', 'http://0b4af6cdc2f0c5998459-c0245c5c937c5dedcca3f1764ecc9b2f.r43.cf2.rackcdn.com/12455-healthtech13-duffy.pdf'),
' and my ',
HREF("master's thesis",'https://www.ideals.illinois.edu/handle/2142/45545'),
'.'))
])

# Raytheon-SI
occup.addNodes([
PStart(),
BoldStartEnd(HREF('Raytheon-SI Government Solutions', 'http://www.raytheon.com')),
' - Graduate Vulnerability Research Intern (Summer 2012). ',
HREF('Baltimore-Washington, Maryland, USA.', 'https://maps.google.com/maps?ll=39.114287,-76.777902&z=10'),
PEnd(),
PStartEnd('Vulnerability research using modern tools and methods including fuzzing, static analysis, dynamic analysis, virtualization, debugging and much, much more.', cls='n')
])

# Cerner
occup.addNodes([
PStart(),
BoldStartEnd(HREF('Cerner Corporation', 'http://www.cerner.com')),
' - Software Engineer (2010-2011). ',
HREF('Kansas City, Missouri, USA.', 'https://maps.google.com/maps?ll=39.100226,-94.581694&z=14'),
PEnd(),
PStartEnd('Providing support for Cerner Millennium including memory dump analysis, network analysis, developing debugging tools, and working closely with clients.', cls='n')
])

# UTD
occup.addNodes([
PStart(),
BoldStartEnd(HREF('The University of Texas at Dallas', 'http://www.utdallas.edu')),
' - Help Desk, CS Tutor, Computer Lab, etc (2006-2010). ',
HREF('Richardson, Texas, USA.', 'https://maps.google.com/maps?ll=32.986492,-96.749137&z=15'),
PEnd(),
PStartEnd('A plethora of responsibilities such as Windows/*nix administration, client support, fundraising, and anything else that pays the bills.',cls='n')
])

## Educational History Section
# UIUC
educa = PageSection('Educational History', 'bordered')
educa.addNodes([
PStart(),
BoldStartEnd(HREF('The University of Illinois at Urbana-Champaign', 'http://www.illinois.edu')),
' - M.S., Computer Science (2013). (',
ScriptRef('Courses', 'pages/courses.py', 'grad_cs'),
') ',
PEnd()
])

# UTD CS
educa.addNodes([
PStart(),
BoldStartEnd(HREF('The University of Texas at Dallas', 'http://www.utdallas.edu')),
' - B.S., Computer Science (2010). (',
ScriptRef('Courses', 'pages/courses.py', 'ug_cs'),
') ',
PEnd()
])

accol = UList('ast')
accol.addNodes([
'National Science Foundation Computer Science and Mathematics Scholarship',
'Academic Distinction Scholarship',
'Ericsson Scholarship',
"Dean's List",
'Honors Graduate'
])

# UTD Math
educa.addNodes([
PStart(),
BoldStart(),
HREF('The University of Texas at Dallas', 'http://www.utdallas.edu'),
BoldEnd(),
' - B.S., Mathematics (2010). (',
ScriptRef('Courses', 'pages/courses.py', 'ug_math'),
') ',
PEnd(),
PStartEnd(accol, cls='n'),
])

## Contact Section
contact = PageSection('Contact', 'bordered')

contactList = UList('ast')
contactList.addNodes([
NodeList('Email: ', Img('imgs/email_16.png')),
HREF('LinkedIn','http://www.linkedin.com/pub/eric-duffy/40/56a/5a3')
])

contact.addNodes([ PStart(), contactList, PEnd() ])

## insert image above the header(s)
idx = gen.findType(BodyStart)
gen.insertNode(idx + 1, Img(IMG_ME_SRC, 'floatright'))
gen.addNode(personal)
gen.addNode(Break())
gen.addNode(occup)
gen.addNode(Break())
gen.addNode(educa)
gen.addNode(Break())
gen.addNode(contact)
gen.addNode(Break())

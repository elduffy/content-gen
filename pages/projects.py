#/usr/bin/python
# -*- coding: UTF-8 -*-
if __name__ == '__main__':
	exit(0)

class Project(ContentNode):
	def __init__(self, name, year, desc, *skillList):
		self.name = name
		self.year = year
		if not isinstance(desc, ContentNode):
			desc = ContentString(desc)
		self.desc = desc
		self.skillList = NodeList(*sorted(skillList, key=lambda x:str(x)))
	def generateHTML(self):
		nodes = [
		Header('{0} ({1}).'.format(self.name, self.year), 3),
		PStartEnd(self.desc),
		Header('Related Skills:',4),
		UList('ast', *self.skillList) ]
		result = ''
		for node in nodes:
			result += node.generateHTML()
		return result
	def canHoldChildren(self):
		return True
	def __iter__(self):
		lst = []
		if self.desc.canHoldChildren():
			lst.extend(self.desc)
		else:
			lst.append(self.desc)
		if self.skillList != None:
			lst.extend(self.skillList)
		return iter(lst)

## define the projects in a list
projects = NodeList(

Project('Research Database', 2012,
'''I am currently the <i>de facto</i> database administrator for my research group. I have
designed and implemented a normalized MySQL schema to hold our research dataset as well
as a series of python scripts for importing and exporting data as well as using Enthought
for statistical analysis.''',
'SQL (MySql)', 'Python', 'Enthought Python Distribution (including Scipy & Numpy)'),

Project('JavaScript Fuzzer', 2012,
'''I developed a JavaScript fuzzer designed to break JavaScript parsers/runtimes using a few
thousand lines of C++. It is designed to produce semantically correct code so that the
runtime can be fuzzed, rather than just the parser.''',
'C++','JavaScript','Compiler Organization & Design','Programming Language Design',
'Fuzzer Design', 'Reverse Engineering', 'Virtualization'),

Project('Workflow Learner', 2012,
NodeList("With the help of two classmates, I developed an application that extracts \
a set of accesses from an audit log (such as in an electronic health record) \
and constructs a workflow model from the unstructured data, &#xE0 la ",
HREF('Agrawal, et. al', 'http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.25.8660'),
'. Feel free to take a look at our ',
HREF('presentation', '../misc/563-dss-slides.pptx'), '.'),
'Java', 'Machine Learning', 'Graphviz', 'Graph Theory'
),

Project('Electronic Health Record Emulator', 2011,
NodeList('''I built an EHR emulator which reads an EHR audit log, extracts workflow structures and
emulates the behavior of the patients and users within the audit logs. The purpose of
this was to have a rich set of data on which to run various classifiers (logistic regression
as well as support vector machine with multiple kernels). I wrote this using a few
thousand lines of C#.
Check out my presentation ''', HREF('here', '../misc/463-presentation.pptx'), '.'),
'C#', 'Machine Learning', 'SQL (Postgres)', 'Database Model Design'
),


Project('COOL Compiler', 2011, NodeList(
'''I wrote a compiler for the Classroom Object Oriented Language (COOL) for 
CS 426 - Compiler Construction. It was written in C and C++ and uses ''',
HREF('Flex', 'http://flex.sourceforge.net/'), ' for lexing, ',
HREF('Bison', 'http://www.gnu.org/software/bison/'), ' for parsing, and ',
HREF('LLVM', 'http://llvm.org'), ''' as a backend. Everything else was
either provided by the instructor as support code or written by myself. I also
wrote an LLVM pass to perform register allocation for MIPS using the Chaitin-Briggs
algorithm with the help of a partner.'''
), 'C/C++', 'Flex', 'Bison', 'LLVM', 'OS Organization', 'Compiler Organization & Design',
'Programming Language Design', 'Graph Theory'),

Project('Oiler Graphing Calculator', 2010, NodeList(
'''I developed a graphing calculator for Windows using C#.NET. It supports
multiple parsers should one wish to use a different syntax and is very 
extensible. It can graph functions f : R -> R, f : R -> R x R, and sets defined
iteratively using complex values, like the ''',
HREF('Mandelbrot Set', 'http://en.wikipedia.org/wiki/Mandelbrot_set'),
'''. It is also capable of symbolic differentiation, numerical integration, and several
other features. I presented it to win 2nd place at the UTD programming competition.'''),
'C#', 'Calculus', 'Numerical analysis', 'Real analysis', 'Set theory', 'Complex variables'),

Project('Webpage Content Generator', 2013,
NodeList('I have developed a Python framework for statically generating the content of this website. See ',
ScriptRef('here', 'webgen.py'), ' for details.'),
'Python', 'Web development'))

## sort by year, descending
projects = NodeList(*sorted(iter(projects), key=lambda x:x.year, reverse=True))

gen.addNodes([
SectionStart('bordered'),
PStartEnd('''I have been working on a number of projects over the years.
I am gradually updating this page with my activity, so keep checking back.
I'll also include screenshots and source code 
once I take the time to resurrect my sunsetted projects.'''),
projects,
SectionEnd()
])

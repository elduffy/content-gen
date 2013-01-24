#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net
import collections as coll

def getKwargList(**kwargs):
	#result = '<' + str(tag)
	result = ''
	for k,v in kwargs.items():
		if v == None:
			continue
		result += ' {0}="{1}"'.format(k,v)
	#if close:
	#	result += ' /'
	#result += '>'	
	return result

###	ContentGenerator contains a list of ContentNode objects and generates the output HTML
class ContentGenerator:
	def __init__(self, writer):
		self.nodes = []
		self.writer = writer
	def addNode(self, node):
		self.nodes.append(node)
	def addNodes(self, nodes):
		self.nodes.extend(nodes)
	def generateHTML(self):
		for node in self.nodes:
			self.writer.write(node.generateHTML())
			self.writer.write('\n')
		return

###	ContentNode is an abstract object which can generate HTML output
class ContentNode(object):
	def __init__(self):
		pass
	
	def generateHTML(self):
		return ''
###	ContentString is a ContentNode subclass wrapping string
class ContentString(ContentNode):
	def __init__(self, string):
		self.string = string
	def generateHTML(self):
		return self.string

#### 	Begin abstract Tag classes
### 	TagEmpty is an empty HTML tag, such as <img ... />
class TagEmpty(ContentNode):
	def __init__(self, tag, cls=None, **kwargs):
		self.tag = tag
		self.kwargs = kwargs
		self.cls = cls
		if 'class' in self.kwargs:
			cls = self.kwargs['class']
			del self.kwargs['class']
	def generateHTML(self):
		kw = coll.OrderedDict(self.kwargs.items())
		if not self.cls == None:
			kw['class'] = self.cls
		return '<' + str(self.tag) + str(getKwargList(**kw)) + ' />'

###	TagStart is an start HTML tag, such as <body>
class TagStart(ContentNode):
	def __init__(self, tag, cls=None, **kwargs):
		self.tag = tag
		self.kwargs = kwargs
		self.cls = cls
		if 'class' in self.kwargs:
			cls = self.kwargs['class']
			del self.kwargs['class']
	def generateHTML(self):
		kw = coll.OrderedDict(self.kwargs.items())
		if not self.cls == None:
			kw['class'] = self.cls
		return '<' + str(self.tag) + str(getKwargList(**kw)) + '>'

###	TagStart is an end HTML tag, such as </body>
class TagEnd(ContentNode):
	def __init__(self, tag):
		self.tag = tag
	def generateHTML(self):
		return '</{0}>'.format(self.tag)

###	TagStartEnd wraps the TagStart and TagEnd into a single class with some text between the tags
class TagStartEnd(ContentNode):
	def __init__(self, tag, content='', cls=None, **kwargs):
		self.ts = TagStart(tag, cls, **kwargs)
		self.te = TagEnd(tag)
		self.content = ContentString(content)
	def generateHTML(self):
		result = str(self.ts.generateHTML())
		result += str(self.content.generateHTML())
		result += str(self.te.generateHTML())
		return result
		
####	End abstract Tag classes
#
####	Begin concrete utility Tag classes
#####	Begin Start/End-Tag extensions
class DocStart(TagStart):
	def __init__(self):
		super(DocStart, self).__init__('html')
	def generateHTML(self):
		return '<!DOCTYPE html>\n' + super(DocStart, self).generateHTML()

class DocEnd(TagEnd):
	def __init__(self):
		super(DocEnd, self).__init__('html')

class BodyStart(TagStart):
	def __init__(self, cls=None):
		super(BodyStart, self).__init__('body', cls)

class BodyEnd(TagEnd):
	def __init__(self):
		super(BodyEnd, self).__init__('body')

class SectionStart(TagStart):
	def __init__(self, cls=None, **kwargs):
		super(SectionStart, self).__init__('section', cls, **kwargs)

class SectionEnd(TagEnd):
	def __init__(self):
		super(SectionEnd, self).__init__('section')

class PageTitle(TagStartEnd):
	def __init__(self, title='eld', cls=None, **kwargs):
		super(PageTitle, self).__init__('title', title, cls, **kwargs)

class Header(TagStartEnd):
	def __init__(self, text='', level=1):
		super(Header, self).__init__('h' + str(level), text)

class AStart(TagStart):
	def __init__(self, cls=None, **kwargs):
		super(AStart, self).__init__('a', cls, **kwargs)
class AEnd(TagEnd):
	def __init__(self):
		super(AEnd, self).__init__('a')

#####	End Start/End-Tag extensions
#
#####	Begin Empty-Tag extensions
		
class Img(TagEmpty):
	def __init__(self, src, cls=None, **kwargs):
		super(Img, self).__init__('img', cls, src=src, **kwargs)

class Link(TagEmpty):
	def __init__(self, rel, type, href, cls=None):
		super(Link, self).__init__('link', cls, rel=rel, type=type, href=href)

class LinkCSS(Link):
	def __init__(self, cssFile='style.css'):
		super(LinkCSS, self).__init__('stylesheet', 'text/css', cssFile)
#####	End Empty-Tag extensions
#
#####	Begin section utilities which are particular to my webpage
class PageSection(ContentNode):
	def __init__(self, title, cls=None, **kwargs):
		self.title = title
		self.secStart = SectionStart(cls, **kwargs)
		self.elems = []

	def addText(self, text):
		self.elems.append(ContentString(text))

	def startPara(self):
		self.elems.append(TagStart('p'))

	def endPara(self):
		self.elems.append(TagEnd('p'))

	def addHREF(self, text, href):
		aStart = AStart(href=href)
		aEnd = AEnd()
		self.elems.append(aStart)
		self.elems.append(ContentString(text))
		self.elems.append(aEnd)

	def generateHTML(self):
		result = ''
		result += self.secStart.generateHTML()+ '\n'
		result += AStart(name=self.title.lower()).generateHTML()
		result += Header(str(self.title) + '.', 3).generateHTML()
		result += AEnd().generateHTML() + '\n'
		
		for elem in self.elems:
			result += elem.generateHTML()
			result += '\n'
		result += SectionEnd().generateHTML()
		
		return result


####	End concrete utility Tag classes

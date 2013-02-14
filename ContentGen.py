#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net
import collections as coll
import sys, os
import time, datetime

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


class ScriptHandler:
	def __init__(self, filename, opts=dict()):
		self.filename = filename.strip()
		self.opts = opts

	@staticmethod
	def forceKey():
		return 'force'

	@staticmethod
	def recurKey():
		return 'recursive'

	@staticmethod
	def checkRelKey():
		return 'check_rel'

	@staticmethod
	def checkAllKey():
		return 'check_all'

	def __forcesWrite(self):
		if self.opts != None and self.forceKey() in self.opts:
			return self.opts[self.forceKey()]
		return False

	def __isRecursive(self):
		if self.opts != None and self.recurKey() in self.opts:
			return self.opts[self.recurKey()]
		return False
	
	def __checksRelativeRefs(self):
		if self.opts != None and self.checkRelKey() in self.opts:
			return self.opts[self.checkRelKey()]
		return False

	def __checksAllRefs(self):
		if self.opts != None and self.checkAllKey() in self.opts:
			return self.opts[self.checkAllKey()]
		return False

	def __getDttmFormatString(self):
		return '%Y-%m-%d %H:%M:%S'

	def __writeSourceModifiedTime(self, writer):
		dttm = self.getSourceModifiedTime()
		if dttm == None:
			return
		datestr = dttm.strftime(self.__getDttmFormatString())
		writer.write('mtime:\t{0}\n'.format(datestr))

	def getReferencedScripts(self, gen):
		## Loop over structure to find them
		result = set()
		for node in gen:
			if isinstance(node, ScriptRef):
				result.add(node.getScriptRef())
			if isinstance(node, PageSection):
				result |= self.getReferencedScripts(node)
		return result
		

	def shouldRun(self):
		if self.__forcesWrite():
			return True
		## looks at the input file (source) modified time
		## then looks at the stored modified time, if any
		## if the difference is greater >= 1 seconds, regenerate
		modifiedTime = self.getSourceModifiedTime()
		storedTime = self.getStoredModifiedTime()
		#print("{0},\t{1}".format(modifiedTime,storedTime))
		if modifiedTime == None:
			return False
		if storedTime == None:
			return True
		secDiff = abs((modifiedTime - storedTime).total_seconds())
		return secDiff >= 1

	def getSourceModifiedTime(self):
		try:
			return datetime.datetime.fromtimestamp(os.path.getmtime(self.filename))
		except IOError, ioe:
			return None

	def getStoreName(self):
		## if input is e.g. 'Index.py', return '.wg_Index'
		extIdx = self.filename.rfind('.py')
		if extIdx == len(self.filename) - len('.py'):
			result = self.filename[:extIdx]
		else:
			result = self.filename
		result = '.wg_' + result.replace('.', '_')
		return result

	@staticmethod
	def getHtmlFileName(script):
		## replace '.py' with '.htm' or append '.htm'
		extIdx = script.rfind('.py')
		if extIdx == len(script) - len('.py'):
			result = script[:extIdx] + '.htm'
		else:
			result = script + '.htm'
		return result
		

	def getHtmlName(self):
		return ScriptHandler.getHtmlFileName(self.filename)

	def getHtmlPageHeader(self):
		fname = os.path.basename(self.filename)
		extIdx = fname.rfind('.py')
		if extIdx > 0:
			fname = fname[:extIdx]
		firstChar = fname[0].upper()
		fname = '- ' + str(firstChar) + str(fname[1:]) + '.'
		return fname

	def writeToStore(self):
		writer = None
		try:
			writer = open(self.getStoreName(), 'w')
			self.__writeSourceModifiedTime(writer)
			#TODO: update as necessary
		except IOError:
			return
		finally:
			if writer != None:
				writer.close()
		return
			
	
	def getStoredModifiedTime(self):
		reader = None
		try:
			reader = open(self.getStoreName(), 'r')
			prefix = 'mtime:\t'
			for line in reader.readlines():
				line = line.strip()
				idx = line.find(prefix)
				if idx < 0:
					continue
				remaining = line[idx+len(prefix):]
				dttm = datetime.datetime.strptime(remaining, self.__getDttmFormatString())
				return dttm
		except IOError:
			return None
		except ValueError, ve:
			print(ve)
			return None
		finally:
			if reader != None:
				reader.close()

	def run(self):
		sys.stderr.write("Processing \'{0}\'\n".format(self.filename))
		result = set()
		if not self.shouldRun():
			sys.stderr.write('\'{0}\' already current.\n'.format(self.getHtmlName()))
			return set()
		try:
			writer = open(self.getHtmlName(), 'w')
			gen = ContentGenerator(writer)
			result.add(os.path.abspath(self.filename))
		except IOError, ioe:
			sys.stderr.write(str(ioe) + '\n')
			return set()
		if gen == None:
			return set()
		
		## set default elements in the generator
		NAME = 'Eric L Duffy'
		gen.addNodes([DocStart(), PageTitle(), LinkCSS(), BodyStart(), Header(NAME, 1), Header(self.getHtmlPageHeader(),1) ])
		execfile(self.filename, globals(), locals())
		gen.addNodes([BodyEnd(), DocEnd()])
		gen.generateHTML()
		gen.close()
		
		self.writeToStore()
		
		if self.__isRecursive():
			scripts = self.getReferencedScripts(gen)
			
			for script in scripts:
				absScript = os.path.abspath(script)
				if absScript in result:
					continue
				sh = ScriptHandler(script, self.opts)
				processed = sh.run()
				result |= processed
		return result


###	ContentGenerator contains a list of ContentNode objects and generates the output HTML
class ContentGenerator:
	def __init__(self, writer):
		self.nodes = []
		self.writer = writer
	def __iter__(self):
		return iter(self.nodes)
	def addNode(self, node):
		self.nodes.append(node)
	def addNodes(self, nodes):
		self.nodes.extend(nodes)
	def generateHTML(self):
		for node in self.nodes:
			self.writer.write(node.generateHTML())
			self.writer.write('\n')
		return
	def close(self):
		if self.writer != None:
			self.writer.close()

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

###	DateString is a ContentString subclass generating text of a datetime (current UTC datetime by default)
class DateString(ContentString):
	def __init__(self, dttm=datetime.datetime.utcnow(), format='%A %d %B, %Y'):
		super(DateString, self).__init__(dttm.strftime(format))

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

class HREF(TagStartEnd):
	def __init__(self, text, href):
		super(HREF, self).__init__('a', text, href=href)
		self.href = href
	def getHRef(self):
		return self.href

class ScriptRef(HREF):
	def __init__(self, text, script):
		super(ScriptRef, self).__init__(text, ScriptHandler.getHtmlFileName(script))
		self.script = script
	def getScriptRef(self):
		return self.script
	


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

	def __iter__(self):
		return iter(self.elems)

	def addNode(self, node):
		if isinstance(node, ContentNode):
			self.elems.append(node)
		else:
			self.addText(str(node))

	def addNodes(self, nodes):
		## don't extend, so we can add non-subclasses of ContentNode such as strings
		for node in nodes:
			self.addNode(node)

	def addText(self, text):
		self.elems.append(ContentString(text))

	def startPara(self):
		self.elems.append(TagStart('p'))

	def endPara(self):
		self.elems.append(TagEnd('p'))

	def addHREF(self, text, href):
		self.elems.append(HREF(text, href))

	def addScriptRef(self, text, script):
		self.elems.append(ScriptRef(text, os.path.abspath(script)))

	def generateHTML(self):
		result = ''
		result += self.secStart.generateHTML()+ '\n'
		secName = self.title.lower().replace(' ', '_')
		result += AStart(name=secName).generateHTML()
		result += Header(str(self.title) + '.', 3).generateHTML()
		result += AEnd().generateHTML() + '\n'
		
		for elem in self.elems:
			result += elem.generateHTML()
			#result += '\n'
		result += SectionEnd().generateHTML()
		
		return result


####	End concrete utility Tag classes

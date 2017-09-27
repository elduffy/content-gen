#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net
import collections as coll
import sys, os
import time, datetime
import re
import urllib

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

def textToHTML(text):
	result = NodeList()
	for line in text.split('\n'):
		result.addNode(line)
		result.addNode(Break())
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
	
	@staticmethod
	def silentKey():
		return 'silent'

	@staticmethod
	def isUrl(path):
		reg = ScriptHandler.urlRegex()
		return reg.match(path) != None

	@staticmethod
	def urlRegex():
		return re.compile(
			r'^(?:http|ftp)s?://'
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
			r'localhost|'
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
			r'(?::\d+)?'
			r'(?:/?|[/?]\S+)$', re.IGNORECASE) ## from django
	
	@staticmethod	
	def __stripPath(filename):
		idx = filename.rfind('/')
		if idx < 0:
			return filename
		return filename[idx+1:]
		

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

	def __isSilent(self):
		if self.opts != None and self.silentKey() in self.opts:
			return self.opts[self.silentKey()]
		return False

	def __getDttmFormatString(self):
		return '%Y-%m-%d %H:%M:%S'

	def __writeSourceModifiedTime(self, writer):
		dttm = self.getSourceModifiedTime()
		if dttm == None:
			return
		datestr = dttm.strftime(self.__getDttmFormatString())
		writer.write('mtime:\t{0}\n'.format(datestr))

	def __checkAndReportLocal(self, path):
		olddir = os.path.abspath('.')
		filedir = os.path.dirname(self.filename)
		if len(filedir) == 0:
			filedir = '.'
		os.chdir(filedir)
		abspath = os.path.abspath(path)
		os.chdir(olddir)

		if not os.path.exists(abspath):
			self.issueReport('Unable to locate resource: \'{0}\' referenced in \'{1}\''.format(path, self.filename))
		return

	def __checkAndReportExternal(self, url):
		try:
			res = urllib.urlopen(url)
		except IOError:
			self.issueReport('Unable to access url \'{0}\' referenced in \'{1}\''.format(url, self.filename))
			return

		
	
	def __cssPath(self):
		direc = os.path.relpath(self.filename)
		result = ''
		depth = len(direc.split('/'))
		for i in xrange(1,depth):
			result += '../'
		return result + 'style.css'

	def issueReport(self, message):
		if self.__isSilent():
			return
		sys.stderr.write('Report: ' + str(message) + '\n')

	def getReferencedScripts(self, gen):
		## Loop over structure to find them
		result = set()
		for node in gen:
			if isinstance(node, ScriptRef):
				result.add(node.getScriptRef())
			#if isinstance(node, PageSection) or isinstance(node, NodeList) or isinstance(node, UList):
			if node.canHoldChildren():
				result |= self.getReferencedScripts(node)
		return result
	
	def getReferencedResources(self, gen):
		result = set()
		for node in gen:
			if isinstance(node, HREF) and not isinstance(node, ScriptRef):
				result.add(node.getHRef())
			if isinstance(node, Img):
				result.add(node.getSource())
			if isinstance(node, Link):
				result.add(node.getHRef())
			if isinstance(node, PageSection):
				result |= self.getReferencedResources(node)
		return result

	def shouldRun(self):
		if self.__forcesWrite():
			return True
		## looks at the input file (source) modified time
		## then looks at the stored modified time, if any
		## if the difference is greater >= 1 seconds, regenerate
		modifiedTime = self.getSourceModifiedTime()
		storedTime = self.getStoredModifiedTime()
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
		fname = os.path.basename(self.filename)
		extIdx = fname.rfind('.py')
		if extIdx == len(fname) - len('.py'):
			result = fname[:extIdx]
		else:
			result = fname
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
			fname = os.path.relpath(os.path.dirname(os.path.abspath(self.filename)) + '/' + self.getStoreName())
			writer = open(fname, 'w')
			self.__writeSourceModifiedTime(writer)
			#TODO: update as necessary
		except IOError, ioe:
			self.issueReport('Failed to write to store: {0}'.format(ioe))
			return
		finally:
			if writer != None:
				writer.close()
		return
	
	def getRelativePath(self, rootPath):
		olddir = os.path.abspath('.')
		absPath = os.path.abspath(rootPath)
		filedir = os.path.dirname(self.filename)
		if len(filedir) == 0:
			filedir = '.'
		os.chdir(filedir)
		rPath = os.path.relpath(absPath)
		os.chdir(olddir)
		return rPath
	
	def getStoredModifiedTime(self):
		reader = None
		try:
			fname = os.path.relpath(os.path.dirname(os.path.abspath(self.filename)) + '/' + self.getStoreName())
			reader = open(fname, 'r')
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
			return None
		finally:
			if reader != None:
				reader.close()

	def run(self, seen=set()):
		## returns (processedSet, modifiedSet)
		self.issueReport("Processing \'{0}\'".format(self.filename))
		pResult = set()
		mResult = set()
		if not self.shouldRun():
			self.issueReport('\'{0}\' already current.'.format(self.getHtmlName()))
			gen = ContentGenerator(None)
			pResult.add(os.path.abspath(self.filename))
			execfile(self.filename, globals(), locals()) ## updates gen
		else:
			try:
				writer = open(self.getHtmlName(), 'w')
				gen = ContentGenerator(writer)
				pResult.add(os.path.abspath(self.filename))
				mResult.add(os.path.abspath(self.filename))
			except IOError, ioe:
				self.issueReport('Failed to process {0}: {1}'.format(self.filename, ioe))
				return (set(), set())
			if gen == None:
				return (set(), set())
		
			## set default elements in the generator
			NAME = 'Eric L Duffy'
			gen.addNodes([DocStart(), PageTitle(), LinkCSS(self.__cssPath()), BodyStart(), Header(NAME, 1), Header(self.getHtmlPageHeader(),2) ])
			execfile(self.filename, globals(), locals())
			gen.addNodes([HomeLink(), Break(), Break(), ModifiedDateString(),
                            BodyEnd(), DocEnd()])
			gen.generateHTML()
			gen.close()
			self.writeToStore()
		
		if self.__isRecursive():
			scripts = self.getReferencedScripts(gen)
			for script in scripts:
				olddir = os.path.abspath('.')
				filedir = os.path.dirname(self.filename)
				if len(filedir) == 0:
					filedir = '.'
				os.chdir(filedir)
				absScript = os.path.abspath(script)
				os.chdir(olddir)
				#absScript = os.path.abspath(script)
				if absScript in pResult:
					continue
				if not os.path.exists(absScript):
					print(absScript)
					self.issueReport('Script \'{0}\' referenced in \'{1}\' does not exist'.format(script, self.filename))
					continue
				if absScript in seen:
					continue
				#sh = ScriptHandler(script, self.opts)
				sh = ScriptHandler(absScript, self.opts)
				seen.add(absScript)
				(processed, modified) = sh.run(seen)
				pResult |= processed
				mResult |= modified
		
		if self.__checksRelativeRefs() or self.__checksAllRefs():
			refs = self.getReferencedResources(gen)
			for ref in refs:
				if not ScriptHandler.isUrl(ref):
					## local resource
					self.__checkAndReportLocal(ref)
				else:
					## external resource
					if self.__checksAllRefs():
						## check the link
						self.__checkAndReportExternal(ref)
		
		return (pResult, mResult)


###	ContentGenerator contains a list of ContentNode objects and generates the output HTML
class ContentGenerator:
	def __init__(self, writer):
		self.nodes = []
		self.writer = writer
	def __iter__(self):
		return iter(self.nodes)
	def addNode(self, node):
		if not isinstance(node, ContentNode):
			self.nodes.append(ContentString(str(node)))
		else:
			self.nodes.append(node)
	def insertNode(self, idx, node):
		if not isinstance(node, ContentNode):
			self.nodes.insert(idx, ContentString(str(node)))
		else:
			self.nodes.insert(idx, node)
	def findType(self, typ):
		i = 0
		for node in self.nodes:
			if isinstance(node, typ):
				return i
			i += 1
		return -1
	def addNodes(self, nodes):
		for node in nodes:
			self.addNode(node)
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
	
	def canHoldChildren(self):
		return False

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
		self.cls = cls
		if isinstance(content, ContentNode):
			self.content = content
		elif content == None:
			self.content = ContentString('')
		else:
			self.content = ContentString(content)
	def __iter__(self):
		if self.content == None:
			return iter([])
		elif self.content.canHoldChildren():
			return iter(self.content)
		else:
			return iter([self.content])
	def canHoldChildren(self):
		if self.content == None:
			return False
		if not isinstance(self.content, ContentNode):
			return False
		return True
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
		return '<!DOCTYPE html>\n<meta charset="utf-8">\n' + super(DocStart, self).generateHTML()

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
class AStartEnd(TagStartEnd):
	def __init__(self, content, cls=None, **kwargs):
		super(AStartEnd, self).__init__('a', content, cls, **kwargs)

class CenterStart(TagStart):
	def __init__(self, **kwargs):
		super(CenterStart, self).__init__('center', None, **kwargs)
class CenterEnd(TagEnd):
	def __init__(self):
		super(CenterEnd, self).__init__('center')
class CenterStartEnd(TagStartEnd):
	def __init__(self, content, **kwargs):
		super(CenterStartEnd, self).__init__('center', content, None, **kwargs)

class PStart(TagStart):
	def __init__(self, cls=None, **kwargs):
		super(PStart, self).__init__('p', cls, **kwargs)
class PEnd(TagEnd):
	def __init__(self):
		super(PEnd, self).__init__('p')
class PStartEnd(TagStartEnd):
	def __init__(self, content, cls=None, **kwargs):
		super(PStartEnd, self).__init__('p', content, cls, **kwargs)
	

class HREF(TagStartEnd):
	def __init__(self, text, href):
		super(HREF, self).__init__('a', text, href=href)
		self.href = href
	def canHoldChildren(self):
		return False	
	def getHRef(self):
		return self.href

class ScriptRef(HREF):
	def __init__(self, text, script, section=''):
		super(ScriptRef, self).__init__(text, ScriptHandler.getHtmlFileName(script) + (('#' + section) if len(section) > 0 else '' ))
		self.script = script
		self.section = section
	def getScriptRef(self):
		return self.script
	def hasSection(self):
		return len(section) > 0
	
class Break(TagStart):
	def __init__(self):
		super(Break, self).__init__('br')

class BoldStart(TagStart):
	def __init__(self):
		super(BoldStart, self).__init__('b')
class BoldEnd(TagEnd):
	def __init__(self):
		super(BoldEnd, self).__init__('b')
class BoldStartEnd(TagStartEnd):
	def __init__(self, content):
		super(BoldStartEnd, self).__init__('b', content)

class SupStartEnd(TagStartEnd):
	def __init__(self, content):
		super(SupStartEnd, self).__init__('sup', content)

class UList(TagStartEnd):
	def __init__(self, cls=None, *nodes):
		super(UList, self).__init__('ul', NodeList(), cls)
		self.addNodes(nodes)
	def __iter__(self):
		return iter(self.content)
	def canHoldChildren(self):
		return True
	def addNode(self, node):
		item = TagStartEnd('li', node, self.cls)
		self.content.addNode(item)
	def addNodes(self, nodes):
		for node in nodes:
			self.addNode(node)
class NodeList(ContentNode):
	def __init__(self, *items):
		super(NodeList, self).__init__()
		self.nodes = []
		self.addNodes(items)
	def addNode(self, node):
		if node == None:
			return
		if not isinstance(node, ContentNode):
			self.nodes.append(ContentString(str(node)))
		else:
			self.nodes.append(node)
	def addNodes(self, nodes):
		for node in nodes:
			self.addNode(node)

	def nodeAt(self, idx):
		return self.nodes[idx]

	def __iter__(self):
		return iter(self.nodes)

	def __len__(self):
		return len(self.nodes)

	def canHoldChildren(self):
		return True
	
	def generateHTML(self):
		result = ''
		for node in self.nodes:
			if node == None:
				continue
			result += str(node.generateHTML())
		return result

class Table(TagStartEnd):
	def __init__(self, cls=None, *headers):
		super(Table, self).__init__('table', NodeList(), cls)

		if headers == None or len(headers) == 0:
			return
		headerRow = TableRow(cls)
		for header in headers:
			if not isinstance(header, ContentNode):
				header = ContentString(str(header))
			hdr = TagStartEnd('th', header, cls)
			headerRow.addNode(hdr)
		self.addRow(headerRow)

	def __iter__(self):
		return iter(self.content)
	def canHoldChildren(self):
		return True
	def columnCount(self):
		if self.content == None:
			return 0
		if len(self.content) == 0:
			return 0
		return len(self.content.nodeAt(0))
	def addRow(self, node):
		if not isinstance(node, TableRow):
			self.content.addNode(TableRow(self.cls, node))
		else:
			self.content.addNode(node)

class TableRow(NodeList):
	def __init__(self, cls=None, *columns):
		super(TableRow, self).__init__()
		self.cls = cls
		for col in columns:
			self.addColumn(col)
		
	def addColumn(self, node):
		if not isinstance(node, ContentNode):
			node = ContentString(node)
		super(TableRow, self).addNode(TagStartEnd('td', node, self.cls))
	def generateHTML(self):
		result = '<tr>' + super(TableRow, self).generateHTML() + '</tr>'
		return result

#####	End Start/End-Tag extensions
#
#####	Begin Empty-Tag extensions
		
class Img(TagEmpty):
	def __init__(self, src, cls=None, **kwargs):
		super(Img, self).__init__('img', cls, src=src, **kwargs)
		self.src = src
	def getSource(self):
		return self.src

class DivStartEnd(TagStartEnd):
	def __init__(self, content, cls=None):
		super(DivStartEnd, self).__init__('div', content, cls)

class Link(TagEmpty):
	def __init__(self, rel, type, href, cls=None):
		super(Link, self).__init__('link', cls, rel=rel, type=type, href=href)
		self.href = href
	def getHRef(self):
		return self.href

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
		self.sectionName = self.title.lower().replace(' ', '_')
		
		if 'printHeader' in kwargs and kwargs['printHeader'] == False:
			self.printHeader = False
		else:
			self.printHeader = True

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

	def canHoldChildren(self):
		return True

	def getSectionName(self):
		return self.sectionName

	def setSectionName(self, name):
		self.sectionName = name

	def generateHTML(self):
		result = ''
		result += self.secStart.generateHTML()+ '\n'
		secName = self.getSectionName()
		result += AStart(name=secName).generateHTML()
		if self.printHeader:
			result += Header(str(self.title) + '.', 3).generateHTML()
		result += AEnd().generateHTML() + '\n'
		
		for elem in self.elems:
			result += elem.generateHTML()
			#result += '\n'
		result += SectionEnd().generateHTML()
		
		return result

class HomeLink(NodeList):
	def __init__(self):
		super(HomeLink, self).__init__(Break(), HREF('Home','http://eduff.net'), Break())

class ModifiedDateString(DateString):
	def __init__(self):
		super(ModifiedDateString, self).__init__()
		self.string = 'Modified ' + self.string
		

####	End concrete utility Tag classes

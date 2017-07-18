#/usr/bin/python
# -*- coding: UTF-8 -*-
if __name__ == '__main__':
	exit(0)

def reportTable():
	result = Table('bordered', 'Report', 'Meaning')
	
	info = 	[
		('Processing &lt;script&gt;',
			'''Processing has begun on &lt;script&gt;, but output has not
			necessarily been generated.'''),
		('&lt;script&gt; already current',
			'''The version of &lt;script&gt; recognized in .wg_&lt;script&gt; is the
			same as that supplied and the -f flag was not enabled.'''),
		('Failed to process &lt;script&gt;: &lt;error&gt;', '''An I/O error is preventing 
			the script from being processed.'''),
		('Script &lt;script1&gt; referenced in &lt;script0&gt; does not exist',
			'''&lt;script0&gt; has a ScriptRef() on &lt;script1&gt; but
			&lt;script1&gt; has not yet been created and cannot be executed.'''),
		('Unable to locate resource: &lt;resource&gt; referenced in &lt;script&gt;',
			'''&lt;script&gt; has a reference to &lt;resource&gt;, defined in HREF,
			Link, Img, etc which cannot be located in the file system.'''),
		('Unable to access url &lt;url&gt; referenced in &lt;script&gt;',
			'Same as above, but for URLs.'),
		('Failed to write to store: &lt;error&gt;','Could not write to wg_&lt;script&gt;')
		]
	
	for (report, meaning) in info:
		result.addRow(TableRow('bordered', report, textToHTML(meaning)))
	return result

GITSITE = 'https://github.com/elduffy/content-gen'

overview = PageSection('Overview', 'bordered')
overview.startPara()
overview.addNodes([
HREF('WebGen.py', GITSITE),
''' is the technology I use to generate the content on this site. It is a set of Python scripts 
and modules which statically generate the HTML to be displayed. It also checks the validity of 
references to resources, reduces formatting inconsistencies, allows for greater flexibility, and generally
eases the burden of maintaining this site. Plus, it's just more fun than writing HTML by hand.'''
])
overview.endPara()
overview.startPara()
overview.addNodes([
'You will notice that each HTML page on this site contains a ',
SourceLink('webgen.py'),
''' link at the bottom which directs you to a Python script. This script is called by 
WebGen.py (not to be confused with this page's source, webgen.py) and all elements of the
page are inserted into the "gen" object, which is maintained by WebGen.py. WebGen.py then 
calls the generateHTML() method which outputs the HTML from the structure defined in the script.
WebGen.py also maintains a record of the modified date/time of the source script so that whenever
the website is processed in a batch fashion, we don't need to extraneously regenerate the content.
'''
])
overview.endPara()
overview.startPara()
overview.addNodes([
'WebGen.py, along with the source for this site, is available on ', HREF('github', GITSITE), '.'
])
overview.endPara()

usage = PageSection('Usage', 'bordered')
usage.startPara()
usage.addNodes([
'The WebGen.py help menu can be invoked as follows:', Break(), Break(),

textToHTML('''./WebGen.py -h
Usage: WebGen.py [options] [script0 [script1 [...]]]

Options:
  -h, --help         show this help message and exit
  -f, --force        Force overwrite of existing HTML file(s)
  -r, --recursive    Recurse through referenced files
  -l, --check-local  Check relative references in source files when able
  -c, --check-all    Check all references in source files when able
  -s, --silent       Prevent normal execution output'''),
])
usage.endPara()
usage.startPara()
usage.addNodes([
'''The -f switch forces overwrite even when the version store (named .wg_&lt;scriptname&gt;)
indicates that the generated HTML is syncronized with the source. The -r switch tells WebGen.py
to iterate recursively through the scripts that are referenced using the ScriptRef() object. 
The -l switch verifies the existence of 
local resources that are referenced with Img(), HREF(), Link(), etc but it
does not check external references, which can be enabled by the -c flag. The -s flag gags output,
which is discussed below'''
])
usage.endPara()

output = PageSection('Output', 'bordered')
output.startPara()
output.addNodes([
'''WebGen.py generates some helpful information when the -s flag is not enabled. The output labeled
"Report" is printed to stderr while everything else goes to stdout. The following table summarizes the 
reports.''',
CenterStart(),
reportTable(),
CenterEnd()
])
output.endPara()
output.startPara()
output.addNodes([
'''Once execution has ended, a summary is displayed giving the number of files processed and those modified
(including created).'''
])
output.endPara()


gen.addNodes([
overview, Break(), usage, Break(), output
])

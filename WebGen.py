#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net

from sys import exit, stderr
from optparse import OptionParser
import os
from ContentGen import ScriptHandler

if not __name__ == '__main__':
	exit(0)

optParser = OptionParser(usage='usage: %prog [options] [script0 [script1 [...]]')
optParser.add_option('-f', '--force', action='store_true', default=False, dest=ScriptHandler.forceKey(), help='Force overwrite of existing HTML file(s)')
optParser.add_option('-r', '--recursive', action='store_true', default=False, dest=ScriptHandler.recurKey(), help='Recurse through referenced files')
optParser.add_option('-l', '--check-local', action='store_true', default=False, dest=ScriptHandler.checkRelKey(), help='Check relative references in source files when able')
optParser.add_option('-c', '--check-all', action='store_true', default=False, dest=ScriptHandler.checkAllKey(), help='Check all references in source files when able')
optParser.add_option('-s', '--silent', action='store_true', default=False, dest=ScriptHandler.silentKey(), help='Prevent normal execution output')

(opts, args) = optParser.parse_args()
if len(args) == 0:
	print('Must pass a python script as argument.\n{0}'.format(optParser.get_usage()))
	exit(0)

optDict = vars(opts)
silent = optDict[ScriptHandler.silentKey()]
filesProcessed = set()
filesModified = set()
for fname in args:
	fname = os.path.abspath(fname)
	try:
		sh = ScriptHandler(fname, optDict)
		(processed, modified) = sh.run()
		filesProcessed |= processed
		filesModified |= modified
	except IOError, ioe:
		stderr.write('Could not process file \'{0}\': {1}\n'.format(fname, ioe))

numProcessed = len(filesProcessed)
numModified = len(filesModified)
if numProcessed > 0 and not silent:
	reportStr = '\nComplete! Processed {0} file{1}, modifying {2}: '.format(numProcessed, 's' if numProcessed > 1 else '', numModified)
	for script in filesProcessed:
		reportStr += "\n'{0}'".format(script)
		if script in filesModified:
			reportStr += ' (mod)'
	print(reportStr)

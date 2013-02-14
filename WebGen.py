#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net

from sys import exit, stderr
from optparse import OptionParser
import os
import ContentGen as cg

def get_usage():
	return

if not __name__ == '__main__':
	exit(0)

optParser = OptionParser(usage='usage: %prog [options] filename')
optParser.add_option('-f', '--force', action='store_true', default=False, dest=cg.ScriptHandler.forceKey(), help='Force overwrite of existing HTML file(s)')
optParser.add_option('-r', '--recursive', action='store_true', default=False, dest=cg.ScriptHandler.recurKey(), help='Recurse through referenced files')
optParser.add_option('-l', action='store_true', default=False, dest=cg.ScriptHandler.checkRelKey(), help='Check relative references in source files when able')
optParser.add_option('-c', action='store_true', default=False, dest=cg.ScriptHandler.checkAllKey(), help='Check all references in source files when able')

(opts, args) = optParser.parse_args()
if len(args) != 1:
	print('Must pass a python script as argument.\n{0}'.format(optParser.get_usage()))
	exit(0)

for fname in args:
	try:
		sh = cg.ScriptHandler(fname, vars(opts))
		processed = sh.run()
		if len(processed) > 0:
			reportStr = 'Processed the following files: '
			for script in processed:
				reportStr += "\n'{0}'".format(script)
			print(reportStr)
		
	except IOError, ioe:
		stderr.write('Could not process file \'{0}\': {1}\n'.format(fname, ioe))

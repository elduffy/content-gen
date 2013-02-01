#!/usr/bin/python
## Author: Eric L Duffy
## Website: eduff.net

from sys import exit, stderr
from optparse import OptionParser
from ContentGen import PyLoader

def get_usage():
	return

if not __name__ == '__main__':
	exit(0)

optParser = OptionParser(usage='usage: %prog [options] filename')
optParser.add_option('-f', '--force', action='store_true', default=False, dest='force', help='Force overwrite of existing HTML file(s)')
optParser.add_option('-r', '--recursive', action='store_true', default=False, dest='recursive', help='Recurse through referenced files')

(opts, args) = optParser.parse_args()
if len(args) != 1:
	print('Must pass a python file as argument.\n{0}'.format(optParser.get_usage()))


pl = PyLoader(args[0])

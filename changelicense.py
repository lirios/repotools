#!/usr/bin/env python
#
# This file is part of Liri.
#
# Copyright (C) 2019 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:MIT$
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# $END_LICENSE$
#

srclicense = dstlicense = ""
srctext = dsttext = ""

def read_license(filename):
	import re
	text = license = ""
	ignore = True

	f = open(filename, "r")
	for line in f.readlines():
		# Read from the BEGIN_LICENSE line included
		m = re.search(r'\$BEGIN_LICENSE:(.+)\$$', line)
		if m:
			ignore = False
			license = m.group(1)

		# Save the line when we are actually reading a license line
		if not ignore:
			text += line

		# Stop reading when we hit the END_LICENSE line
		m = re.search(r'\$END_LICENSE\$$', line)
		if m:
			break
	f.close()

	return (license, text)

def search(root, d):
	for pattern in options.glob.split(";"):
		g = os.path.join(root, d, pattern)
		for f in glob.glob(g):
			if f[:-len(pattern)] != pattern:
				massage(f)

def massage(filename):
	# Read the original text
	f = open(filename, "r")
	code = f.read()
	f.close()

	# Perform the substitution
	code = code.replace(srctext, dsttext)

	# Write the code
	f = open(filename, "w")
	f.write(code)
	f.close()

if __name__ == "__main__":
	import sys, os, glob
	from optparse import OptionParser

	parser = OptionParser(usage="usage: %prog [options] PATH .. PATHN")
	parser.add_option("-s", "--source-license", dest="source_license",
		help="read source license text from FILE", metavar="FILE")
	parser.add_option("-d", "--dest-license", dest="dest_license",
		help="read destination license text from FILE", metavar="FILE")
	parser.add_option("-g", "--glob", dest="glob",
		help="source code files glob, default: %default", default="*.cpp;*.h")

	(options, args) = parser.parse_args()

	# Source and destination license files are mandatory
	if not options.source_license or not options.dest_license:
		parser.print_help()
		sys.exit(1)

	# Also the argument
	if not args:
		parser.print_help()
		sys.exit(1)

	# Read the license files
	(srclicense, srctext) = read_license(options.source_license)
	(dstlicense, dsttext) = read_license(options.dest_license)

	# Can't continue if we haven't read the licenses correctly
	if not srclicense or not srctext:
		print >> sys.stderr, "Couldn't read the source license!"
		sys.exit(1)
	if not dstlicense or not dsttext:
		print >> sys.stderr, "Couldn't read the destination license!"
		sys.exit(1)

	# Walk through all the directories passed as argument and replace
	# the original license text with the new one
	for path in args:
		for root, dirs, files in os.walk(path):
			search(root, "")
			for d in dirs:
				search(root, d)

#!/usr/bin/env python
#
# This file is part of Liri.
#
# Copyright (C) 2012-2015 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:BSD$
#
# You may use this file under the terms of the BSD license as follows:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Liri project nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Pier Luigi Fiorini BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

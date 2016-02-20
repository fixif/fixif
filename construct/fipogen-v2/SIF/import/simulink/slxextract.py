#!/usr/bin/python
"""
slxextract modules
 Extract 'blockdiagram.xml' file
 from Matlab SLX compressed file
 Note : SLX file (OPC) is a zip file with some specification 
"""

import zipfile
import sys
import os.path

	

# Function to check archive validity
def isarchivevalid(zfilename):
	if  zipfile.is_zipfile(zfilename):
		return True
	else:
		return False



# Function to extract the block diag from slx file
def slxextract(slxfile):
	zfile = zipfile.ZipFile(slxfile)
	for ffname in zfile.namelist():
		(dir, selfile) = os.path.split(ffname)
		if selfile == 'blockdiagram.xml':
			#zfile.extract(fname)
			fd = open(selfile, 'w')
			fd.write(zfile.read(ffname))
			fd.close()
			zfile.close()
			return True

	zfile.close()
	return False


# stand alone extraction script
# -->  extract blockdiag from slx file given in cmdline
if __name__ == "__main__":

	# Get archive file
	if len(sys.argv) < 2:
		print "specify the SLX file"
		sys.exit()
	else:
		zfilename = sys.argv[1]
	print zfilename


	# Check archive validity
	if isarchivevalid(zfilename):
		print "archive OK"
	else:
		print "bad archive"
		sys.exit()

	# Extract blockdiagram.xml file in a slx file
	state = slxextract(zfilename)
	if state:
		print "blockdiagram extracted in blockdiagram.xml"
	else:
		print "blockdiagram not found"


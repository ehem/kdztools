#!/usr/bin/env python

"""
Copyright (C) 2016 Elliott Mitchell <ehem+android@m5p.com>
Copyright (C) 2013 IOMonster (thecubed on XDA)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import zlib
import os
import sys
import argparse
from struct import *
from collections import OrderedDict

class DZFileTools:
	"""
	LGE Compressed DZ File tools
	"""

	# Setup variables
	partitions = []
	outdir = "dzextracted"

	dz_header = b"\x32\x96\x18\x74"
	dz_sub_header = b"\x30\x12\x95\x78"
	dz_sub_len = 512

	# Format string dict
	#   itemName is the new dict key for the data to be stored under
	#   formatString is the Python formatstring for struct.unpack()
	#   collapse is boolean that controls whether extra \x00 's should be stripped
	# Example:
	#   ('itemName', ('formatString', collapse))
	dz_sub_dict = OrderedDict([
	  ('header',   ('4s',   False)),
	  ('type',     ('32s',  True)),
	  ('name',     ('64s',  True)),
	  ('unknown0', ('I',    False)),
	  ('length',   ('I',    False)),
	  ('md5',      ('16s',  False)),
	  ('unknown1', ('I',    False)),
	  ('unknown2', ('I',    False)),
	  ('unknown3', ('I',    False)),
	  ('pad',      ('376s', True)),
	])

	# Generate the formatstring for struct.unpack()
	dz_formatstring = " ".join([x[0] for x in dz_sub_dict.values()])

	# Generate list of items that can be collapsed (truncated)
	dz_collapsibles = [n for n, (y, p) in dz_sub_dict.items() if p]


	def readDZHeader(self):
		"""
		Reads the DZ header, and returns a single dz_item
		in the form as defined by self.dz_sub_dict
		"""

		# Read a whole DZ header
		buf = self.infile.read(self.dz_sub_len)

		# "Make the item"
		# Create a new dict using the keys from the format string
		# and the format string itself
		# and apply the format to the buffer
		dz_item = dict(
			zip(
				self.dz_sub_dict.keys(),
				unpack(self.dz_formatstring,buf)
			)
		)

		# Add an "offset" key to the dict
		# self allows us to remember where in the file the compressed data exists
		dz_item['offset'] = self.infile.tell()

		# Collapse (truncate) each key's value if it's listed as collapsible
		for key in self.dz_collapsibles:
			dz_item[key] = dz_item[key].rstrip(b'\x00')
			if b'\x00' in dz_item[key]:
				print("[!] Error: extraneous data found IN "+key)
				sys.exit(1)

		# Verify DZ sub-header
		if dz_item['header'] != self.dz_sub_header:
			print("[!] Bad DZ sub header!")
			sys.exit(1)

		return dz_item


	def getPartitions(self):
		"""
		Returns the list of partitions from a DZ file containing multiple segments
		"""
		while True:

			# Read each segment's header
			dz_sub = self.readDZHeader()

			# Append it to our list
			self.partitions.append(dz_sub)

			# Would seeking the file to the end of the compressed data
			# bring us to the end of the file, or beyond it?
			if int(self.infile.tell()) + int(dz_sub['length']) >= int(self.dz_length):
				break

			# Seek to next DZ header
			self.infile.seek(dz_sub['length'],1)

		# Make partition list
		return [(x['name'],x['length']) for x in self.partitions]


	def extractPartition(self,index):
		"""
		Extracts a partition from a compressed DZ file using ZLIB.
		self function could be particularly memory-intensive when used
		with large segments, as the entire compressed segment is loaded
		into RAM and decompressed.

		A better way to do self would be to chunk the zlib compressed
		data and decompress it with zlib.decompressor() and a while
		loop.

		I'm lazy though, and y'all have fast computers, so self is good
		enough.
		"""

		currentPartition = self.partitions[index]

		# Seek to the beginning of the compressed data in the specified partition
		self.infile.seek(currentPartition['offset'])

		# Ensure that the output directory exists
		if not os.path.exists(self.outdir):
			os.makedirs(self.outdir)

		# Open the new file for writing
		outfile = open(os.path.join(self.outdir,currentPartition['name'].decode("utf8")), 'wb')

		# Read the whole compressed segment into RAM
		zdata = self.infile.read(currentPartition['length'])

		# Decompress the data, and write it to disk
		outfile.write(zlib.decompress(zdata))

		# Close the file
		outfile.close()

	def parseArgs(self):
		# Parse arguments
		parser = argparse.ArgumentParser(description='LG Compressed DZ File Extractor by IOMonster')
		parser.add_argument('-f', '--file', help='DZ File to read', action='store', required=True, dest='dzfile')
		group = parser.add_mutually_exclusive_group(required=True)
		group.add_argument('-l', '--list', help='List partitions', action='store_true', dest='listOnly')
		group.add_argument('-x', '--extract', help='Extract all partitions', action='store_true', dest='extractAll')
		group.add_argument('-s', '--single', help='Single Extract by ID', action='store', dest='extractID', type=int)
		parser.add_argument('-o', '--out', help='Output directory', action='store', dest='outdir')

		return parser.parse_args()

	def openFile(self, dzfile):
		# Open the file
		self.infile = open(dzfile, "rb")

		# Get length of whole file
		self.infile.seek(0, os.SEEK_END)
		self.dz_length = self.infile.tell()
		self.infile.seek(0)

		# Verify DZ header
		verify_header = self.infile.read(4)
		if verify_header != self.dz_header:
			print("[!] Error: Unsupported DZ file format.")
			print("[ ] Expected: %s ,\n\tbut received %s ." % (" ".join(hex(n) for n in self.dz_header), " ".join(hex(n) for n in verify_header)))
			sys.exit(1)

		# Skip to end of DZ header
		self.infile.seek(512)

	def cmdListPartitions(self):
		print("[+] DZ Partition List\n=========================================")
		for part in enumerate(self.partList):
			print("%2d : %s (%d bytes)" % (part[0], part[1][0].decode("utf8"), part[1][1]))

	def cmdExtractSingle(self, partID):
		print("[+] Extracting single partition!\n")
		print("[+] Extracting " + str(self.partList[partID][0]) + " to " + os.path.join(self.outdir,self.partList[partID][0]))
		self.extractPartition(partID)

	def cmdExtractAll(self):
		print("[+] Extracting all partitions!\n")
		for part in enumerate(self.partList):
			print("[+] Extracting " + part[1][0].decode("utf8") + " to " + os.path.join(self.outdir,part[1][0].decode("utf8")))
			self.extractPartition(part[0])

	def main(self):
		args = self.parseArgs()
		self.openFile(args.dzfile)
		self.partList = self.getPartitions()

		if "outdir" in args:
			self.outdir = args.outdir

		if args.listOnly:
			self.cmdListPartitions()

		elif args.extractID and args.extractID >= 0:
			self.cmdExtractSingle(args.extractID)

		elif args.extractAll:
			self.cmdExtractAll()


if __name__ == "__main__":
	dztools = DZFileTools()
	dztools.main()


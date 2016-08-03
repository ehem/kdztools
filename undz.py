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

from __future__ import print_function
import os
import sys
import io
import zlib
import argparse
import hashlib
from binascii import crc32, b2a_hex

# our tools are in "libexec"
sys.path.append(os.path.join(sys.path[0], "libexec"))

import dz
import gpt


class UNDZUtils(object):
	"""
	Common class for unpacking DZ file structures
	"""


	def loadHeader(self, file):
		"""
		Loads a structured header, does common processing and returns
		dictionary with data (buffer stored as "buffer")
		"""

		# Read the header structure
		buffer = file.read(self._dz_length)


		# "Make the item"
		# Create a new dict using the keys from the format string
		# and the format string itself
		# and apply the format to the buffer
		dz_item = self.unpackdict(buffer)


		# Verify DZ area header
		if dz_item == None:
			print("[!] Bad DZ {:s} header!".format(self._dz_area), file=sys.stderr)
			sys.exit(1)


		# some paths want to take a look at the raw data
		dz_item['buffer'] = buffer


		# Collapse (truncate) each key's value if it's listed as collapsible
		for key in self._dz_collapsibles:
			if type(dz_item[key]) is str or type(dz_item[key]) is bytes:
				dz_item[key] = dz_item[key].rstrip(b'\x00')
				if b'\x00' in dz_item[key]:
					print("[!] Error: extraneous data found IN "+key, file=sys.stderr)
					sys.exit(1)
			elif type(dz_item[key]) is int:
				if dz_item[key] != 0:
					print('[!] Error: field "'+key+'" is non-zero ('+b2a_hex(dz_item[key])+')', file=sys.stderr)
					sys.exit(1)
			else:
				print("[!] Error: internal error", file=sys.stderr)
				sys.exit(-1)

		# To my knowledge this is supposed to be blank (for now...)
		if len(dz_item['pad']) != 0:
			print("[!] Error: pad is not empty", file=sys.stderr)
			sys.exit(1)


		return dz_item



class UNDZChunk(dz.DZChunk, UNDZUtils):
	"""
	Representation of an individual file chunk from a LGE DZ file
	"""


	def getChunkName(self):
		"""
		Return the name of our chunk
		"""
		return self.chunkName.decode("utf8")

	def getSliceName(self):
		"""
		Return the name of the slice we're located in
		"""
		return self.sliceName.decode("utf8")

	def getLength(self):
		"""
		Return the length of our chunk (amount of compressed data)
		"""
		return self.dataSize

	def getMessages(self):
		"""
		Return any messages generated while loading us
		"""
		return self.messages

	def getDataOffset(self):
		"""
		Return the offset where our payload should be located
		"""
		return self.dataOffset

	def getTargetStart(self):
		"""
		Return the offset into the target storage medium where we start
		"""
		return self.targetAddr << self.dz.shiftLBA

	def getTargetEnd(self):
		"""
		Return the offset into the target storage medium where we end
		"""
		return (self.targetAddr << self.dz.shiftLBA) + self.targetSize

	def getNext(self):
		"""
		Return offset of next chunk
		"""
		return self.dataOffset + self.dataSize

	def Messages(self, file=sys.stdout):
		"""
		Write our messages to file
		"""
		# Print our messages
		for m in self.messages:
			print(m, file=file)


	def display(self, sliceIdx, selfIdx):
		"""
		Display information about our chunk
		"""
		print("{:2d}/{:2d} : {:s} ({:d} bytes)".format(sliceIdx, selfIdx, self.chunkName.decode("utf8"), self.dataSize))
		self.Messages()
		return ++selfIdx

	def extract(self):
		"""
		Extracts our payload from the compressed DZ file using ZLIB.
		self function could be particularly memory-intensive when used
		with large chunks, as the entire compressed chunk is loaded
		into RAM and decompressed.

		A better way to do self would be to chunk the zlib compressed
		data and decompress it with zlib.decompressor() and a while
		loop.

		I'm lazy though, and y'all have fast computers, so self is good
		enough.
		"""

		# Seek to the beginning of the compressed data in the specified partition
		self.dz.dzfile.seek(self.dataOffset, io.SEEK_SET)

		# Read the whole compressed segment into RAM
		zdata = self.dz.dzfile.read(self.dataSize)

		# Decompress the data
		buf = zlib.decompress(zdata)

		crc = crc32(buf) & 0xFFFFFFFF

		if crc != self.crc32:
			print("[!] Error: CRC32 of data doesn't match header ({:08X} vs {:08X})".format(crc, self.crc32), file=sys.stderr)
			sys.exit(1)

		md5 = hashlib.md5()
		md5.update(buf)

		if md5.digest() != self.md5:
			print("[!] Error: MD5 of data doesn't match header ({:32s} vs {:32s})".format(md5.hexdigest(), b2a_hex(self.md5)), file=sys.stderr)
			sys.exit(1)

		return buf

	def extractChunk(self, file, name):
		"""
		Extract the payload of our chunk into the file with the name

		Extracts our payload from the compressed DZ file using ZLIB.
		self function could be particularly memory-intensive when used
		with large chunks, as the entire compressed chunk is loaded
		into RAM and decompressed.

		A better way to do self would be to chunk the zlib compressed
		data and decompress it with zlib.decompressor() and a while
		loop.

		I'm lazy though, and y'all have fast computers, so self is good
		enough.
		"""

		if name:
			print("[+] Extracting {:s} to {:s}".format(self.chunkName.decode("utf8"), name))

		# Create a hole at the end of the wipe area
		if file:
			current = file.seek(0, io.SEEK_CUR)

#			# Ensure space is allocated to areas to be written
#			for addr in range(self.wipeCount):
#				file.seek(1<<self.dz.shiftLBA, io.SEEK_CUR)
#				file.write(b'\x00')
#			file.seek(current, io.SEEK_SET)
			# Makes the output the correct size, by filling as hole
			file.truncate(current + (self.wipeCount<<self.dz.shiftLBA))

		# Write it to file
		file.write(self.extract())

		# Print our messages
		self.Messages()

	def extractChunkfile(self, file, name):
		"""
		Extract the raw data of our chunk into the file with the name
		"""

		print("[+] Extracting {:s} to {:s}".format(self.chunkName.decode("utf8"), name))

		self.dz.dzfile.seek(self.dataOffset-self._dz_length, io.SEEK_SET)
		buffer = self.dz.dzfile.read(self.dataSize + self._dz_length)
		file.write(buffer)

		# Print our messages
		self.Messages()

	def __init__(self, dz, file):
		"""
		Loads the DZ header in the form as defined by self._dz_chunk_dict
		"""

		super(UNDZChunk, self).__init__()

		# Save a pointer to the UNDZFile
		self.dz = dz

		# Load the header, does common checking
		dz_item = self.loadHeader(file)

		# used for warnings about the chunk
		self.messages = []

		# Record the "offset" where our chunk was declared,
		# allows us to resolve where in the compressed data is
		self.dataOffset = file.tell()

		# Add ourselves to the hashes for checking
		dz.md5Headers.update(dz_item['buffer'])

### experiment, results negative
#		dz.sha1Headers.update(dz_item['buffer'])
#
#		dz.crcHeaders = crc32(dz_item['buffer'], dz.crcHeaders)
#
#		dz.md5HeaderNZ.update(dz_item['buffer'][0:-len(dz_item['pad'])])
#		dz.crcHeaderNZ=crc32(dz_item['buffer'][0:-len(dz_item['pad'])], dz.crcHeaders)
### experiment, results negative


		#
		if dz_item['targetSize']&0x1FF != 0:
			self.messages.append("[?] Warning: uncompressed size is {:d}, not a multiple of 512 (please report!)".format(dz_item['targetSize']))

		# Save off all the important data
		self.sliceName	= dz_item['sliceName']
		self.chunkName	= dz_item['chunkName']
		self.targetAddr = dz_item['targetAddr']
		self.targetSize	= dz_item['targetSize']
		self.dataSize	= dz_item['dataSize']
		self.md5	= dz_item['md5']
		self.wipeCount	= dz_item['wipeCount']
		self.crc32	= dz_item['crc32']

		# This is where in the image we're supposed to go
		targetAddr = int(self.chunkName[len(self.sliceName)+1:-4])

		if targetAddr != self.targetAddr:
			self.messages.append("[!] Uncompressed starting offset differs from chunk name!")



class UNDZSlice(object):
	"""
	Representation of a diskslice from a LGE DZ file
	"""

	def addChunk(self, chunk):
		"""
		Add a chunk to our diskslice
		"""

		offset = chunk.getTargetStart()
		# if it is at the start...
		if offset < self.start:
			print("[!] Warning: Chunk is part of \"{:s}\", but starts in front of slice?!".format(self.name), file=sys.stderr)

		self.chunks.append(chunk)


	def getStart(self):
		"""
		Get the starting offset of our slice
		"""
		return self.start

	def getEnd(self):
		"""
		Get the ending offset of our slice
		"""
		return self.end

	def getLength(self):
		"""
		Get the length of our slice
		"""
		return self.end-self.start

	def display(self, sliceIdx, chunkIdx):
		"""
		Display information on the various chunks in our slice
		Return the last index we used
		"""
		if len(self.chunks) == 0:
			print("{:2d}/?? : {:s} (<empty>)".format(sliceIdx, self.name))
		for chunk in self.chunks:
			chunkIdx+=1
			chunk.display(sliceIdx, chunkIdx)
		return chunkIdx

	def getChunkCount(self):
		"""
		Get the number of chunks in our slice
		"""
		return len(self.chunks)

	def getSliceName(self):
		"""
		Get the name of our slice
		"""
		return self.name

	def extractChunk(self, file, name, idx):
		"""
		Extract a given chunk
		"""
		self.chunks[idx].extractChunk(file, name)

	def extractChunkfile(self, file, name, idx):
		"""
		Extract a given chunk
		"""
		self.chunks[idx].extractChunkfile(file, name)

	def extractSlice(self, file, name):
		"""
		Extract the whole slice to the FileIO file named name
		"""

		start = self.getStart()
		end = self.getEnd()

		for chunk in self.chunks:
			cur = chunk.getTargetStart()
			# Mostly happens for the backup GPT (large pad at start)
			if cur < start:
				# this ensures messages from extraction show up
				chunk.extractChunk(file, name)
				file.seek(0, io.SEEK_SET)
				file.truncate(0)
				# in case the long buffer was reeeally looong

				buf = chunk.extract()
				file.write(buf[cur-start:])
			else:
				file.seek(cur-start, io.SEEK_SET)
				chunk.extractChunk(file, name)

		# it is possible for chunks wipe area to extend beyond slice
		file.truncate(self.getLength())


		# write a params file for saving values used during recreate
		params = io.open(name + ".params", "wt")
		params.write(u'# saved parameters for the file "{:s}"\n'.format(name))
		params.write(u"startLBA={:d}\n".format(start >> self.dz.shiftLBA))
		params.write(u"startAddr={:d}\n".format(start))
		params.write(u"endLBA={:d}\n".format(end >> self.dz.shiftLBA))
		params.write(u"endAddr={:d}\n".format(end))
		params.write(u"# this value may be crucial for success and dangerous to modify\n")

		if len(self.chunks) > 0:
			last = self.chunks[-1]
			params.write(u"lastWipe={:d}\n".format((last.getTargetStart() >> self.dz.shiftLBA) + last.wipeCount))
			params.write(u"# the block size is important (though not too likely to change in near future\n")
			params.write(u"blockSize={:d}\n".format(1<<self.dz.shiftLBA))
			params.write(u"blockShift={:d}\n".format(self.dz.shiftLBA))
		else:
			params.write(u"phantom=1\n")
			params.write(u"# this is a phantom slice, no writes are done\n")
			params.write(u"# (though it could be getting wiped)\n")

		params.close()

	def __init__(self, dz, name, start=0x7FFFFFFFFFFFFFFF, end=0):
		"""
		Initialize the instance of UNDZSlice class
		"""

		super(UNDZSlice, self).__init__()

		self.name = name
		self.chunks = []
		self.messages = set()
		self.start = start
		self.end = end

		# Save a pointer to the UNDZFile
		self.dz = dz



class UNDZFile(dz.DZFile, UNDZUtils):
	"""
	Representation of the data parsed from a LGE DZ file
	"""


	def open(self, name):
		"""
		What do you expect? Open file and check the header
		"""

		# Open the file
		self.dzfile = io.FileIO(name, "rb")

		# Get length of whole file
		self.length = self.dzfile.seek(0, io.SEEK_END)
		self.dzfile.seek(0, io.SEEK_SET)


		# Load the header, does common checking
		dz_file = self.loadHeader(self.dzfile)

		# Save the full header for rebuilding the file later
		self.header = dz_file['buffer']

		# Appears to be version numbers for the format
		if dz_file['formatMajor'] > 2:
			print("[!] Error: DZ format version too high! (please report)", file=sys.stderr)
			sys.exit(1)
		elif dz_file['formatMinor'] > 1:
			print("[!] Warning: DZ format more recent than previous versions, output unreliable", file=sys.stderr)


		self.chunkCount = dz_file['chunkCount']

		# save this for creating modified files later
		# (ro.lge.factoryversion)
		self.ro_lge_factoryversion = dz_file['version']

		self.formatMajor = dz_file['formatMajor']
		self.formatMinor = dz_file['formatMinor']

		# currently only "user" has been seen in wild
		self.build_type = dz_file['build_type']

		# save this for consistency checking
		self.md5 = dz_file['md5']

		# save these for later analysis
		self.unknown0 = dz_file['unknown0']
		self.unknown1 = dz_file['unknown1']
		self.unknown2 = dz_file['unknown2']
		self.unknown3 = dz_file['unknown3']


	def loadChunks(self):
		"""
		Loads the headers of the chunks to prepare for listing|extract
		"""

		# are the chunks out of order in regards to image order?
		disorder = False
		last = -1

		while True:

			# Read each segment's header
			chunk = UNDZChunk(self, self.dzfile)
			self.chunks.append(chunk)

			# check ordering
			if last > chunk.getTargetStart():
				disorder = True
			last = chunk.getTargetStart()

			# Would seeking the file to the end of the compressed
			# data bring us to the end of the file, or beyond it?
			next = chunk.getNext()
			if next >= int(self.length):
				break

			# Seek to next DZ header
			self.dzfile.seek(next, io.SEEK_SET)

		# If I'm perverse enough to think of this...
		if disorder:
			print("[ ] Warning: Found out of order chunks (please report)", file=sys.stderr)
			self.chunks.sort(key=lambda c: c.getTargetStart())

		try:
			emptycount = 0
			g = gpt.GPT(self.chunks[0].extract())

			self.shiftLBA = g.shiftLBA

			next = g.dataStartLBA
			slice = UNDZSlice(self, self.chunks[0].getSliceName(), 0, next<<g.shiftLBA)
			self.slices.append(slice)
			self.sliceIdx[self.chunks[0].getSliceName()] = slice

			for slice in g.slices:
				if next != slice.startLBA<<g.shiftLBA:
					new = UNDZSlice(self, "_unallocated_" + str(emptycount), next<<g.shiftLBA, (slice.startLBA-1)<<g.shiftLBA)
					self.slices.append(new)
					emptycount += 1
				next = (slice.endLBA+1)<<g.shiftLBA
				new = UNDZSlice(self, slice.name, slice.startLBA<<g.shiftLBA, next)
				self.slices.append(new)
				self.sliceIdx[slice.name] = new

			if next != (g.dataEndLBA+1)<<g.shiftLBA:
				new = UNDZSlice(self, "_unallocated_" + str(emptycount), next, g.dataEndLBA<<g.shiftLBA)
				self.slices.append(new)
				emptycount += 1
				next = (g.dataEndLBA+1)<<g.shiftLBA

			slice = UNDZSlice(self, self.chunks[-1].getSliceName(), g.dataEndLBA<<g.shiftLBA, (g.altLBA+1)<<g.shiftLBA)
			self.slices.append(slice)
			self.sliceIdx[self.chunks[-1].getSliceName()] = slice

		except NoGPT:
			pass

		for chunk in self.chunks:
			self.addChunk(chunk)

	def checkValues(self):
		"""
		Check values for consistency with suspected use
		"""

		# This does look like a count of chunks
		if len(self.chunks) != self.chunkCount:
			print("[!] Error: chunks in header differs from chunks found (please report)", file=sys.stderr)
			sys.exit(-1)

		# Checking this field for what is expected
		md5Headers = self.md5Headers.digest()

		if md5Headers != self.md5:
			print("[!] Error: MD5 of chunk headers doesn't match header ({:32s} vs {:32s})".format(self.md5Headers.hexdigest(), b2a_hex(self.md5)), file=sys.stderr)
			sys.exit(-1)


		# these are speculative, disabled for others
		return 0
		# Other speculation
		md5HeaderNZ = self.md5HeaderNZ.digest()

		if md5HeaderNZ == self.unknown2:
			self.messages.add("[ ] unknown2 is consistent with MD5 of non-zero header areas")
		else:
			self.messages.add("[ ] MD5 of non-zero header areas not found ({:32s})".format(self.md5HeaderNZ.hexdigest()))


		self.crcHeaders = self.crcHeaders & 0xFFFFFFFF
		if self.crcHeaders == self.unknown0:
			self.messages.add("[ ] unknown0 is consistent with CRC32 of headers")
		elif self.crcHeaders == self.unknown1:
			self.messages.add("[ ] unknown1 is consistent with CRC32 of headers")
		elif self.crcHeaders == self.unknown4:
			self.messages.add("[ ] unknown4 is consistent with CRC32 of headers")
		else:
			self.messages.add("[ ] No CRC32 of headers found ({:08X})".format(self.crcHeaders))


		self.crcHeaderNZ = self.crcHeaderNZ & 0xFFFFFFFF
		if self.crcHeaderNZ == self.unknown0:
			self.messages.add("[ ] unknown0 is consistent with CRC32 of non-zero header areas")
		elif self.crcHeaderNZ == self.unknown1:
			self.messages.add("[ ] unknown1 is consistent with CRC32 of non-zero header areas")
		elif self.crcHeaderNZ == self.unknown4:
			self.messages.add("[ ] unknown4 is consistent with CRC32 of non-zero header areas")
		else:
			self.messages.add("[ ] No CRC32 of non-zero header areas found ({:08X})".format(self.crcHeaders))


		if self.unknown0 == 256:
			self.messages.add("[ ] unknown 0 is 256 like always (half blocksize?)")


	def addChunk(self, chunk):
		"""
		Adds a chunk to some slice, potentially creating a new slice
		"""

		name = chunk.getSliceName()

		# Get the needed slice
		if name in self.sliceIdx:
			slice = self.sliceIdx[name]
		else:
# FIXME: what if chunks out of order?
			slice = UNDZSlice(self, name)
			self.slices.append(slice)
			self.sliceIdx[name] = slice

		# Add it
		slice.addChunk(chunk)

	def display(self):
		"""
		Display information on the various chunks that were found
		"""
		chunkIdx = 0
		sliceIdx = 0
		for slice in self.slices:
			sliceIdx+=1
			chunkIdx = slice.display(sliceIdx, chunkIdx)

		for m in self.messages:
			print(m)

	def getChunkCount(self):
		"""
		Return the number of chunks in the whole file
		"""
		return len(self.chunks)

	def getSliceCount(self):
		"""
		Return the number of slices we've got
		"""
		return len(self.slices)

	def getChunkName(self, idx):
		"""
		Return the name of the given chunk index
		"""
		return self.chunks[idx].getChunkName()

	def getSliceName(self, idx):
		"""
		Return the name of the given slice index
		"""
		return self.slices[idx].getSliceName()

	def extractChunk(self, file, name, idx, slice=None):
		"""
		Extract a given chunk
		"""
		if slice:
			self.slices[slice].extractChunk(file, name, idx)
		else:
			self.chunks[idx].extractChunk(file, name)

	def extractChunkfile(self, file, name, idx, slice=None):
		"""
		Extract a given chunkfile
		"""
		if slice:
			self.slices[slice].extractChunkfile(file, name, idx)
		else:
			self.chunks[idx].extractChunkfile(file, name)

	def extractSlice(self, file, name, idx):
		"""
		Extract the whole slice to the FileIO file named name
		"""
		return self.slices[idx].extractSlice(file, name)

	def extractImage(self, file, name):
		"""
		Extract the whole file to an image file named name
		"""

		# the slice extraction has gotten preoccupied with slices
		for chunk in self.chunks:
			file.seek(chunk.getTargetStart(), io.SEEK_SET)
			chunk.extractChunk(file, name)


	def saveHeader(self):
		"""
		Dump the header from the original file into the output dir
		"""
		file = io.FileIO(".header", "wb")
		file.write(self.header)
		file.close()

	def __init__(self, name):
		"""
		Constructing this class opens the file and loads map of chunks
		"""

		super(UNDZFile, self).__init__()

		self.slices = []
		self.sliceIdx = {}

		self.chunks = []

		self.messages = set()

		# Hash of the headers for consistency checking
		self.md5Headers = hashlib.new("md5")

		# A reasonable default
		# FIXME: need to do somehow do this better
		self.shiftLBA = 9

		# Hashes candidates for data in header area, all the chunk
		# headers, all the payload data, or everything
#		self.sha1Headers = hashlib.new("sha1")
#		self.crcHeaders = crc32(b"")
#		self.md5HeaderNZ = hashlib.md5()
#		self.crcHeaderNZ = crc32(b"")
#		self.md5Payload = hashlib.md5()
#		self.crcPayload = crc32(b"")
#		self.md5Image = hashlib.md5()
#		self.crcImage = crc32(b"")
#		self.md5All = hashlib.md5()
#		self.crcAll = crc32(b"")
#		# try crc32 ?

		self.open(name)
		self.loadChunks()
		self.checkValues()




class DZFileTools:
	"""
	LGE Compressed DZ File tools
	"""

	# Setup variables
	outdir = "dzextracted"

	def parseArgs(self):
		# Parse arguments
		parser = argparse.ArgumentParser(description='LG Compressed DZ File Extractor originally by IOMonster')
		parser.add_argument('-f', '--file', help='DZ File to read', action='store', required=True, dest='dzfile')
		group = parser.add_mutually_exclusive_group(required=True)
		group.add_argument('-l', '--list', help='list slices/partitions', action='store_true', dest='listOnly')
		group.add_argument('-x', '--extract', help='extract chunk-file(s) for reconstruction (all by default)', action='store_true', dest='extractChunkfile')
		group.add_argument('-c', '--chunk', help='extract data chunk(s) (all by default)', action='store_true', dest='extractChunk')
		group.add_argument('-s', '--single', help='extract diskslice(s) (partition(s)) (all by default)', action='store_true', dest='extractSlice')
		group.add_argument('-i', '--image', help='extract all slices/partitions as a disk image', action='store_true', dest='extractImage')
		parser.add_argument('-d', '--dir', '-o', '--out', help='output location', action='store', dest='outdir')
		parser.add_argument('-b', '--blocksize', help='blocksize used on the device', action='store', dest='blocksize')

		return parser.parse_known_args()

	def cmdListPartitions(self):
		print("[+] DZ Partition List\n=========================================")
		self.dz_file.display()

	def cmdExtractChunk(self, files):
		if len(files) == 0:
			print("[+] Extracting all chunks!\n")
			files = range(1, self.dz_file.getChunkCount()+1)
		elif len(files) == 1:
			print("[+] Extracting single chunk!\n")
		else:
			print("[+] Extracting {:d} chunks!\n".format(len(files)))

		for idx in files:
			try:
				idx = int(idx)
			except ValueError:
				print('[!] Bad value "{:s}" (must be number)'.format(idx), file=sys.stderr)
				sys.exit(1)
			if idx <= 0 or idx > self.dz_file.getChunkCount():
				print("[!] Cannot extract out of range chunk {:d} (min=1 max={:d})".format(idx, len(self.dz_file.getChunkCount())), file=sys.stderr)
				sys.exit(1)
			name = self.dz_file.getChunkName(idx-1)
			file = io.FileIO(name, "wb")
			self.dz_file.extractChunk(file, name, idx-1)
			file.close()

	def cmdExtractChunkfile(self, files):
		if len(files) == 0:
			print("[+] Extracting all chunkfiles!\n")
			files = range(1, self.dz_file.getChunkCount()+1)
		elif len(files) == 1:
			print("[+] Extracting single chunkfile!\n")
		else:
			print("[+] Extracting {:d} chunkfiles!\n".format(len(files)))

		for idx in files:
			try:
				idx = int(idx)
			except ValueError:
				print('[!] Bad value "{:s}" (must be number)'.format(idx), file=sys.stderr)
				sys.exit(1)
			if idx <= 0 or idx > self.dz_file.getChunkCount():
				print("[!] Cannot extract out of range chunkfile {:d} (min=1 max={:d})".format(idx, len(self.dz_file.getChunkCount())), file=sys.stderr)
				sys.exit(1)
			name = self.dz_file.getChunkName(idx-1) + ".chunk"
			file = io.FileIO(name, "wb")
			self.dz_file.extractChunkfile(file, name, idx-1)
			file.close()

	def cmdExtractSlice(self, files):
		if len(files) == 0:
			print("[+] Extracting all slices^Wpartitions\n")
			files = range(1, self.dz_file.getSliceCount()+1)
		elif len(files) == 1:
			print("[+] Extracting single slice^Wpartition!\n")
		else:
			print("[+] Extracting {:d} slices^Wpartitions!\n".format(len(files)))

		for idx in files:
			try:
				idx = int(idx)
			except ValueError:
				print('[!] Bad value "{:s}" (must be number)'.format(idx), file=sys.stderr)
				sys.exit(1)
			if idx <= 0 or idx > self.dz_file.getSliceCount():
				print("[!] Cannot extract out of range slice {:d} (min=1 max={:d})".format(idx, self.dz_file.getSliceCount()), file=sys.stderr)
				sys.exit(1)
			slice = self.dz_file.slices[idx-1]
			name = slice.getSliceName() + ".image"
			file = io.FileIO(name, "wb")
			self.dz_file.extractSlice(file, name, idx-1)
			file.close()

	def cmdExtractImage(self, files):
		if len(files) > 0:
			print("[!] Cannot specify specific portions to extract when outputting image", file=sys.stderr)
			sys.exit(1)
		name = "image.img"
		file = io.FileIO(name, "wb")
		self.dz_file.extractImage(file, name)
		file.close()

	def main(self):
		args = self.parseArgs()
		cmd = args[0]
		files = args[1]

		if cmd.outdir:
			self.outdir = cmd.outdir

		if cmd.blocksize:
			cmd.blocksize = int(cmd.blocksize)
			if cmd.blocksize & (cmd.blocksize-1):
				print("[!] Error: Specified block size is not a power of 2", file=sys.stderr)
				sys.exit(1)
			size = cmd.blocksize
			result = 0
			shift = 32
			while shift > 0:
				if (size>>shift)>0:
					size>>=shift
					result+=shift
				shift>>=1
			self.shiftLBA = result

		self.dz_file = UNDZFile(cmd.dzfile)

		if cmd.listOnly:
			self.cmdListPartitions()
			sys.exit(0)

		# Ensure that the output directory exists
		if not os.path.exists(self.outdir):
			os.makedirs(self.outdir)

		# Change to the output directory
		os.chdir(self.outdir)

		# Extracting slice(s)
		if cmd.extractSlice:
			self.cmdExtractSlice(files)

		# Extracting chunk-files(s)
		elif cmd.extractChunkfile:
			self.cmdExtractChunkfile(files)

		# Extract the whole image
		elif cmd.extractImage:
			self.cmdExtractImage(files)

		# Extracting chunk(s)
		elif cmd.extractChunk:
			self.cmdExtractChunk(files)

		# Save the header for later reconstruction
		self.dz_file.saveHeader()

if __name__ == "__main__":
	dztools = DZFileTools()
	dztools.main()


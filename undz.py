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
from struct import Struct
from collections import OrderedDict
from binascii import crc32, b2a_hex
import gpt


class DZStruct(object):
	"""
	Common class for areas with structure
	"""
# 4 byte header
# 512 byte length
# OrderedDict layout out 512 bytes of stuff



class DZChunk(DZStruct):
	"""
	Representation of an individual file chunk from a LGE DZ file
	"""

	_dz_chunk_header = b"\x30\x12\x95\x78"
	_dz_chunk_len = 512

	# Format string dict
	#   itemName is the new dict key for the data to be stored under
	#   formatString is the Python formatstring for struct.unpack()
	#   collapse is boolean that controls whether extra \x00 's should be stripped
	# Example:
	#   ('itemName', ('formatString', collapse))
	_dz_chunk_dict = OrderedDict([
		('header',	('4s',   False)),	# magic number
		('sliceName',	('32s',  True)),	# name of our slice
		('chunkName',	('64s',  True)),	# name of our chunk
		('targetSize',	('I',    False)),	# bytes of target area
		('dataSize',	('I',    False)),	# amount of compressed
		('md5',		('16s',  False)),	# MD5 of target image
		('targetAddr',	('I',    False)),	# first block to write
		('wipeCount',	('I',    False)),	# blocks to wipe before
		('reserved',	('I',    True)),	# currently always zero
		('crc32',	('I',    False)),	# CRC32 of target image
		('pad',		('372s', True)),	# currently always zero
	])

	# Generate the struct for .unpack()
	_dz_struct = Struct("<" + "".join([x[0] for x in _dz_chunk_dict.values()]))

	# Generate list of items that can be collapsed (truncated)
	_dz_collapsibles = [n for n, (y, p) in _dz_chunk_dict.items() if p]


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
			file.truncate(current + (self.wipeCount<<self.shiftLBA))

		# Write it to file
		file.write(self.extract())

		# Print our messages
		self.Messages()

	def __init__(self, dz, file):
		"""
		Loads the DZ header in the form as defined by self._dz_chunk_dict
		"""

		# Sanity check
		if self._dz_struct.size != self._dz_chunk_len:
			print("[!] Internal error!  Chunk format wrong!", file=sys.stderr)
			sys.exit(-1)

		# Save a pointer to the DZFile
		self.dz = dz

		# Read a whole DZ header
		buf = file.read(self._dz_chunk_len)

		# "Make the item"
		# Create a new dict using the keys from the format string
		# and the format string itself
		# and apply the format to the buffer
		dz_item = dict(zip(
			self._dz_chunk_dict.keys(),
			self._dz_struct.unpack(buf)
		))

		# used for warnings about the chunk
		self.messages = []

		# Record the "offset" where our chunk was declared,
		# allows us to resolve where in the compressed data is
		self.dataOffset = file.tell()

		# Verify DZ sub-header
		if dz_item['header'] != self._dz_chunk_header:
			print("[!] Bad DZ chunk header!", file=sys.stderr)
			sys.exit(1)

		# Add ourselves to the hashes for checking
		dz.md5Headers.update(buf)

### experiment, results negative
		dz.crcHeaders = crc32(buf, dz.crcHeaders)

		dz.md5HeaderNZ.update(buf[0:-len(dz_item['pad'])])
		dz.crcHeaderNZ=crc32(buf[0:-len(dz_item['pad'])], dz.crcHeaders)
### experiment, results negative

		# Collapse (truncate) each key's value if it's listed as collapsible
		for key in self._dz_collapsibles:
			if type(dz_item[key]) is str or type(dz_item[key]) is bytes:
				dz_item[key] = dz_item[key].rstrip(b'\x00')
				if b'\x00' in dz_item[key]:
					print("[!] Error: extraneous data found IN "+key, file=sys.stderr)
					sys.exit(1)
			elif type(dz_item[key]) is int:
				if dz_item[key] != 0:
					print('[!] Error: field "'+key+'" is non-zero ('+hex(dz_item[key])+')', file=sys.stderr)
					sys.exit(1)
			else:
				print("[!] Error: internal error", file=sys.stderr)
				sys.exit(-1)

		# To my knowledge this is supposed to be blank (for now...)
		if len(dz_item['pad']) != 0:
			print("[!] Error: pad is not empty", file=sys.stderr)
			sys.exit(1)

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
		targetAddr = int(self.chunkName[len(self.sliceName)+1:-4]) << self.dz.shiftLBA

		if targetAddr != self.targetAddr<<self.dz.shiftLBA:
			self.messages.append("[!] Uncompressed starting offset differs from chunk name!")



class DZSlice(object):
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

	def extractSlice(self, file, name):
		"""
		Extract the whole slice to the FileIO file named name
		"""

		start = self.getStart()
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

	def __init__(self, dz, name, start=0x7FFFFFFFFFFFFFFF, end=0):
		"""
		Initialize the instance of DZSlice class
		"""
		self.name = name
		self.chunks = []
		self.messages = set()
		self.start = start
		self.end = end

		# Save a pointer to the DZFile
		self.dz = dz



class DZFile(DZStruct):
	"""
	Representation of the data parsed from a LGE DZ file
	"""

	_dz_header = b"\x32\x96\x18\x74"
	_dz_head_len = 512

	# Format string dict
	#   itemName is the new dict key for the data to be stored under
	#   formatString is the Python formatstring for struct.unpack()
	#   collapse is boolean that controls whether extra \x00 's should be stripped
	# Example:
	#   ('itemName', ('formatString', collapse))
	_dz_file_dict = OrderedDict([
		('header',	('4s',   False)),	# magic number
		('formatMajor',	('I',    False)),	# always 2 in LE
		('formatMinor',	('I',    False)),	# always 1 in LE
		('reserved0',	('I',    True)),	# format patchlevel?
		('device',	('32s',  True)),
		('version',	('144s', True)),	# "factoryversion"
		('chunkCount',	('I',    False)),
		('md5',		('16s',  False)),	# MD5 of chunk headers
		('unknown0',	('I',    False)),
		('reserved1',	('I',    True)),	# currently always zero
		('unknown1',	('I',    False)),
		('unknown2',	('16s',  False)),	# MD5 checksum?
		('unknown3',	('48s',  False)),	# Id? windows thing?
		('build_type',	('20s',  True)),	# "user"???
		('unknown4',	('8s',   False)),	# version code?
		('reserved2',	('I',    True)),	# currently always zero
		('reserved3',	('H',    True)),	# padding?
		('oldDateCode',	('10s',	 True)),	# prior firmware date?
		('pad',		('180s', True)),	# currently always zero
	])

	# Generate the struct for .unpack()
	_dz_struct = Struct("<" + "".join([x[0] for x in _dz_file_dict.values()]))

	# Generate list of items that can be collapsed (truncated)
	_dz_collapsibles = [n for n, (y, p) in _dz_file_dict.items() if p]

	def open(self, name):
		"""
		What do you expect? Open file and check the header
		"""

		# Sanity check
		if self._dz_struct.size != self._dz_head_len:
			print("[!] Internal error!  Header format wrong!", file=sys.stderr)
			sys.exit(-1)

		# Open the file
		self.dzfile = io.FileIO(name, "rb")

		# Get length of whole file
		self.length = self.dzfile.seek(0, io.SEEK_END)
		self.dzfile.seek(0, io.SEEK_SET)

		# Save the full header for rebuilding the file later
		self.header = self.dzfile.read(self._dz_head_len)

		# "Make the item"
		# Create a new dict using the keys from the format string
		# and the format string itself
		# and apply the format to the buffer

		dz_file = dict(zip(
			self._dz_file_dict.keys(),
			self._dz_struct.unpack(self.header)
		))

		# Verify DZ header
		verify_header = dz_file['header']
		if verify_header != self._dz_header:
			print("[!] Error: Unsupported DZ file format.", file=sys.stderr)
			print("[ ] Expected: {:s} ,\n\tbut received {:s} .".format(" ".join(hex(n) for n in self._dz_header), " ".join(hex(n) for n in verify_header)), file=sys.stderr)
			sys.exit(1)

		# Appears to be version numbers for the format
		if dz_file['formatMajor'] > 2:
			print("[!] Error: DZ format version too high! (please report)", file=sys.stderr)
			sys.exit(1)
		elif dz_file['formatMinor'] > 1:
			print("[!] Warning: DZ format more recent than previous versions, output unreliable", file=sys.stderr)

		# Collapse (truncate) each key's value if it's listed as collapsible
		for key in self._dz_collapsibles:
			if type(dz_file[key]) is str or type(dz_file[key]) is bytes:
				dz_file[key] = dz_file[key].rstrip(b'\x00')
				if b'\x00' in dz_file[key]:
					print("[!] Error: extraneous data found IN "+key, file=sys.stderr)
					sys.exit(1)
			elif type(dz_file[key]) is int:
				if dz_file[key] != 0:
					print('[!] Error: field "'+key+'" is non-zero ('+hex(dz_file[key])+')', file=sys.stderr)
					sys.exit(1)
			else:
				print("[!] Error: internal error", file=sys.stderr)
				sys.exit(-1)

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
		self.unknown4 = dz_file['unknown4']


	def loadChunks(self):
		"""
		Loads the headers of the chunks to prepare for listing|extract
		"""

		# are the chunks out of order in regards to image order?
		disorder = False
		last = -1

		while True:

			# Read each segment's header
			chunk = DZChunk(self, self.dzfile)
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
			slice = DZSlice(self, self.chunks[0].getSliceName(), 0, next<<g.shiftLBA)
			self.slices.append(slice)
			self.sliceIdx[self.chunks[0].getSliceName()] = slice

			for slice in g.slices:
				if next != slice.startLBA<<g.shiftLBA:
					new = DZSlice(self, "_unallocated_" + str(emptycount), next<<g.shiftLBA, (slice.startLBA-1)<<g.shiftLBA)
					self.slices.append(new)
					emptycount += 1
				next = (slice.endLBA+1)<<g.shiftLBA
				new = DZSlice(self, slice.name, slice.startLBA<<g.shiftLBA, next)
				self.slices.append(new)
				self.sliceIdx[slice.name] = new

			if next != (g.dataEndLBA+1)<<g.shiftLBA:
				new = DZSlice(self, "_unallocated_" + str(emptycount), next, g.dataEndLBA<<g.shiftLBA)
				self.slices.append(new)
				emptycount += 1
				next = (g.dataEndLBA+1)<<g.shiftLBA

			slice = DZSlice(self, self.chunks[-1].getSliceName(), g.dataEndLBA<<g.shiftLBA, (g.altLBA+1)<<g.shiftLBA)
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
			slice = DZSlice(self, name)
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

	def extractSlice(self, file, name, idx):
		"""
		Extract the whole slice to the FileIO file named name
		"""
		return self.slices[idx].extractSlice(file, name)

	def extractImage(self, file, name):
		"""
		Extract the whole file to an image file named name
		"""

		for slice in self.slices:
			file.seek(slice.getStart(), io.SEEK_SET)
			slice.extractSlice(file, name)

	def saveHeader(self, dir):
		"""
		Dump the header from the original file into the output dir
		"""
		name = os.path.join(dir, ".header")
		file = io.FileIO(name, "wb")
		file.write(self.header)

	def __init__(self, name):
		"""
		Constructing this class opens the file and loads map of chunks
		"""

		self.slices = []
		self.sliceIdx = {}

		self.chunks = []

		self.messages = set()

		# Hash of the headers for consistency checking
		self.md5Headers = hashlib.md5()

		# A reasonable default
		# FIXME: need to do somehow do this better
		self.shiftLBA = 9

		# Hashes candidates for data in header area, all the chunk
		# headers, all the payload data, or everything
		self.crcHeaders = crc32(b"")
		self.md5HeaderNZ = hashlib.md5()
		self.crcHeaderNZ = crc32(b"")
		self.md5Payload = hashlib.md5()
		self.crcPayload = crc32(b"")
		self.md5Image = hashlib.md5()
		self.crcImage = crc32(b"")
		self.md5All = hashlib.md5()
		self.crcAll = crc32(b"")
		# try crc32 ?

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
		group.add_argument('-l', '--list', help='List partitions', action='store_true', dest='listOnly')
		group.add_argument('-x', '--extract', help='Extract data chunk(s) (all by default)', action='store_true', dest='extractChunk')
		group.add_argument('-s', '--single', help='Extract diskslice(s) (partition(s)) (all by default)', action='store_true', dest='extractSlice')
		group.add_argument('-i', '--image', help='Extract all partitions as a disk image', action='store_true', dest='extractImage')
		parser.add_argument('-o', '--out', help='Output location', action='store', dest='outdir')
		parser.add_argument('-b', '--blocksize', help='Blocksize used on the device', action='store', dest='blocksize')

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
			name = os.path.join(self.outdir, self.dz_file.getChunkName(idx-1))
			file = io.FileIO(name, "wb")
			self.dz_file.extractChunk(file, name, idx-1)

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
			name = os.path.join(self.outdir, slice.getSliceName() + ".img")
			file = io.FileIO(name, "wb")
			self.dz_file.extractSlice(file, name, idx-1)

	def cmdExtractImage(self, files):
		if len(files) > 0:
			print("[!] Cannot specify specific portions to extract when outputting image", file=sys.stderr)
			sys.exit(1)
		name = os.path.join(self.outdir, "image.img")
		file = io.FileIO(name, "wb")
		self.dz_file.extractImage(file, name)

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

		self.dz_file = DZFile(cmd.dzfile)

		if cmd.listOnly:
			self.cmdListPartitions()
			sys.exit(0)

		# Ensure that the output directory exists
		if not os.path.exists(self.outdir):
			os.makedirs(self.outdir)

		if cmd.extractChunk:
			self.cmdExtractChunk(files)

		elif cmd.extractSlice:
			self.cmdExtractSlice(files)

		elif cmd.extractImage:
			self.cmdExtractImage(files)

		self.dz_file.saveHeader(self.outdir)

if __name__ == "__main__":
	dztools = DZFileTools()
	dztools.main()


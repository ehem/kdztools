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
#import os
import sys
#import io
#import hashlib
from struct import Struct
from collections import OrderedDict


class DZStruct(object):
	"""
	Common class for DZ file structures
	"""

	# Length of the headers in DZ files
	_dz_length = 512

	def __init__(self, classy):
		"""
		Common initializations for all DZ structures
		"""


		# Generate the struct for .unpack()
		try:
			classy._dzstruct

		except AttributeError:
			classy._dz_struct = Struct("<" + "".join([x[0] for x in classy._dz_format_dict.values()]))

			# Sanity check
			if self._dz_struct.size != self._dz_length:
				print("[!] Internal error!  Chunk format wrong!", file=sys.stderr)
				sys.exit(-1)

		# Generate list of items that can be collapsed (truncated)
		try:
			classy._dz_collapsibles

		except AttributeError:
			classy._dz_collapsibles = [n for n, (y, p) in classy._dz_format_dict.items() if p]


	def packdict(self, din):
		"""
		Pack all the fields from the dict into a returned buffer
		"""

		dout = dict()

		# pad any string keys that need padding
		for k in self._dz_format_dict.keys():
			if self._dz_format_dict[k][0][-1] == 's':
				l = int(self._dz_format_dict[k][0][:-1])
				dout[k] = (din[k] if k in din else "").ljust(l, b'\x00')
			else:
				dout[k] = din[k]

		dout['header'] = self._dz_header

		values = [dout[k] for k in self._dz_format_dict.keys()]
		buffer = self._dz_struct.pack(*values)

		return buffer


	def unpackdict(self, buffer):
		"""
		Unpack data in buffer into a returned dictionary, return None
		if magic number/header is absent
		"""

		d = dict(zip(
			self._dz_format_dict.keys(),
			self._dz_struct.unpack(buffer)
		))

		if d['header'] != self._dz_header:
			return None

		return d



class DZChunk(DZStruct):
	"""
	Representation of an individual file chunk from a LGE DZ file
	"""

	_dz_area = "chunk"
	_dz_header = b"\x30\x12\x95\x78"

	# Format string dict
	#   itemName is the new dict key for the data to be stored under
	#   formatString is the Python formatstring for struct.unpack()
	#   collapse is boolean that controls whether extra \x00 's should be stripped
	# Example:
	#   ('itemName', ('formatString', collapse))
	_dz_format_dict = OrderedDict([
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

	def __init__(self):
		"""
		Initializer for DZChunk, gets DZStruct to fill remaining values
		"""
		super(DZChunk, self).__init__(DZChunk)



class DZFile(DZStruct):
	"""
	Representation of the data parsed from a LGE DZ file
	"""

	_dz_area = "file"
	_dz_header = b"\x32\x96\x18\x74"

	# Format string dict
	#   itemName is the new dict key for the data to be stored under
	#   formatString is the Python formatstring for struct.unpack()
	#   collapse is boolean that controls whether extra \x00 's should be stripped
	# Example:
	#   ('itemName', ('formatString', collapse))
	_dz_format_dict = OrderedDict([
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
		('unknown1',	('20s',  False)),	#unknown, need to know!
		('unknown2',	('48s',  False)),	# Id? windows thing?
		('build_type',	('20s',  True)),	# "user"???
		('unknown3',	('8s',   False)),	# version code?
		('reserved2',	('I',    True)),	# currently always zero
		('reserved3',	('H',    True)),	# padding?
		('oldDateCode',	('10s',	 True)),	# prior firmware date?
		('pad',		('180s', True)),	# currently always zero
	])

	def __init__(self):
		"""
		Initializer for DZFile, gets DZStruct to fill remaining values
		"""
		super(DZFile, self).__init__(DZFile)



if __name__ == "__main__":
	print("Sorry, this file is an internal library and doesn't do anything interesting by", file=sys.stderr)
	print("itself.", file=sys.stderr)
	sys.exit(1)


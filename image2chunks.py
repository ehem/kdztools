#!/usr/bin/env python

"""
Copyright (C) 2016 Elliott Mitchell <ehem+android@m5p.com>

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
from binascii import crc32

# our tools are in "libexec"
sys.path.append(os.path.join(sys.path[0], "libexec"))

import dz

# compatibility, Python 3 has SEEK_HOLE/SEEK_DATA, Python 2 does not
SEEK_HOLE = io.SEEK_HOLE if hasattr(io, "SEEK_HOLE") else 4
SEEK_DATA = io.SEEK_DATA if hasattr(io, "SEEK_DATA") else 3

class Image2Chunks(dz.DZChunk):
	"""
	Class for transforming a single file from a raw image into chunk files
	"""

	def openFiles(self, name):
		"""
		Opens the files, provide an error message if one doesn't exist
		"""

		try:
			role = "parameter"
			self.paramsFile = io.open(name + ".params", "rt")
			role = "image"
			self.file = io.FileIO(name, "rb")

		except IOError:
			print("[!] Failed opening {:s} file for {:s}".format(role, name), file=sys.stderr)
			sys.exit(1)




	def loadParams(self, name):
		"""
		Loads the .params file for image, saves off key values
		"""


		params = dict()
		line = self.paramsFile.readline()
		while len(line) > 0:
			line.lstrip()
			line = line.partition("#")[0]
			if len(line) == 0:
				line = self.paramsFile.readline()
				continue
			parts = line.partition("=")
			if len(parts[1]) == 0:
				print("[!] Bad line in {:s}'s parameter file".format(name), file=sys.stderr)
			var = parts[0].rstrip()
			# currently we only have integers in the file
			val = int(parts[2].strip())
			params[var] = val
			line = self.paramsFile.readline()

		self.paramsFile.close()
		del self.paramsFile

		if 'phantom' in params and params['phantom']:
			print("[!] {:s} is a phantom slice, skipping!".format(name))
			return False

		for k in 'blockShift', 'startLBA', 'endLBA', 'lastWipe':
			if k not in params:
				print("Parameter value \"{:s}\" is missing, unable to continue".format(k))
				sys.exit(1)

		self.blockShift	= params['blockShift']
		self.blockSize	= 1 << self.blockShift
		self.startLBA	= params['startLBA']
		self.endLBA	= params['endLBA']
		self.lastWipe	= params['lastWipe']

		return True


	def makeChunksHoles(self, name):
		"""
		Generate one or more .chunks files for the named file
		"""

		os.chdir(os.path.dirname(name))
		name = os.path.basename(name)
		baseName = name.rpartition(".")[0] + "_"
		sliceName = name.rpartition(".")[0].encode("utf8")

		current = 0
		targetAddr = self.startLBA
		eof = self.file.seek(0, io.SEEK_END)
		self.file.seek(0, io.SEEK_SET)

		while current < eof:
			hole = (self.file.seek(current, SEEK_HOLE) + self.blockSize-1) & ~(self.blockSize-1)
			# Python's handling of this condition is suboptimal
			try:
				next = self.file.seek(hole, SEEK_DATA) & ~(self.blockSize-1)
				wipeCount = (next - current) >> self.blockShift
			except IOError:
				next = eof
				wipeCount = self.lastWipe - targetAddr

			md5 = hashlib.md5()
			crc = crc32(b"")
			zobj = zlib.compressobj(1)
			self.file.seek(current, io.SEEK_SET)

			chunkName = baseName + str(targetAddr) + ".bin"
			out = io.FileIO(chunkName + ".chunk", "wb")

			print("[+] Compressing {:s} to {:s} ({:d} empty blocks)".format(name, chunkName, (next - hole) >> self.blockShift))

			chunkName = chunkName.encode("utf8")
			out.seek(self._dz_length, io.SEEK_SET)
			zlen = 0

			for b in range((hole - current) >> self.blockShift):
				buf = self.file.read(self.blockSize)
				md5.update(buf)
				crc = crc32(buf, crc)
				zdata = zobj.compress(buf)
				zlen += len(zdata)
				out.write(zdata)

			zdata = zobj.flush(zlib.Z_FINISH)
			zlen += len(zdata)
			out.write(zdata)
			md5 = md5.digest()


			out.seek(0, io.SEEK_SET)

			values = {
				'sliceName':	sliceName,
				'chunkName':	chunkName,
				'targetSize':	hole - current,
				'reserved':	0,
				'dataSize':	zlen,
				'md5':		md5,
				'targetAddr':	targetAddr,
				'wipeCount':	wipeCount,
				'crc32':	crc & 0xFFFFFFFF,
			}

			header = self.packdict(values)
			out.write(header)
			out.close()

			current = next
			targetAddr = self.startLBA + (current >> self.blockShift)

		print("[+] done\n")


	def makeChunksProbe(self, name):
		"""
		Generate one or more .chunks files for the named file
		"""

		os.chdir(os.path.dirname(name))
		name = os.path.basename(name)
		baseName = name.rpartition(".")[0] + "_"
		sliceName = name.rpartition(".")[0].encode("utf8")

		current = 0
		targetAddr = self.startLBA
		eof = self.file.seek(0, io.SEEK_END)
		self.file.seek(0, io.SEEK_SET)



# emulate characteristics of LG's tool, always find a block at start
		readSize = self.blockSize << 10

		md5 = hashlib.md5()
		crc = crc32(b"")
		zobj = zlib.compressobj(1)
		self.file.seek(current, io.SEEK_SET)

		chunkName = baseName + str(targetAddr) + ".bin"
		out = io.FileIO(chunkName + ".chunk", "wb")

		sys.stdout.write("[+] Compressing {:s} to {:s} ".format(name, chunkName))

		chunkName = chunkName.encode("utf8")
		out.seek(self._dz_length, io.SEEK_SET)
		zlen = 0

		wipeData = readSize
		dataCount = readSize



		buf = self.file.read(readSize)

		while len(buf.lstrip(b'\x00')) == 0 and current < eof:
			md5.update(buf)
			crc = crc32(buf, crc)
			zdata = zobj.compress(buf)
			zlen += len(zdata)
			out.write(zdata)
			wipeData += readSize
			dataCount += readSize
			current += readSize

			buf = self.file.read(readSize)



		while current < eof:




			while len(buf.lstrip(b'\x00')) != 0 and current < eof:
				md5.update(buf)
				crc = crc32(buf, crc)
				zdata = zobj.compress(buf)
				zlen += len(zdata)
				out.write(zdata)
				wipeData += readSize
				dataCount += readSize
				current += readSize

				buf = self.file.read(readSize)

			zdata = zobj.flush(zlib.Z_FINISH)
			zlen += len(zdata)
			out.write(zdata)
			md5 = md5.digest()



			while len(buf.lstrip(b'\x00')) == 0 and current < eof:
				wipeData += readSize
				current += readSize
				buf = self.file.read(readSize)


			print("({:d} empty blocks)".format((wipeData - dataCount) >> self.blockShift))





			out.seek(0, io.SEEK_SET)

			values = {
				'sliceName':	sliceName,
				'chunkName':	chunkName,
				'targetSize':	dataCount,
				'reserved':	0,
				'dataSize':	zlen,
				'md5':		md5,
				'targetAddr':	targetAddr,
				'wipeCount':	wipeData >> self.blockShift,
				'crc32':	crc & 0xFFFFFFFF,
			}

			header = self.packdict(values)
			out.write(header)
			out.close()




			targetAddr = self.startLBA + (current >> self.blockShift)


			if current < eof:


				md5 = hashlib.md5()
				crc = crc32(b"")
				zobj = zlib.compressobj(1)

				chunkName = baseName + str(targetAddr) + ".bin"
				out = io.FileIO(chunkName + ".chunk", "wb")

				sys.stdout.write("[+] Compressing {:s} to {:s} ".format(name, chunkName))

				chunkName = chunkName.encode("utf8")
				out.seek(self._dz_length, io.SEEK_SET)
				zlen = 0

				wipeData = readSize
				dataCount = readSize






		print("[+] done\n")


	def __init__(self, name, hasHoles):
		"""
		Initializer for Image2Chunks class, takes filename as arg
		"""

		super(Image2Chunks, self).__init__()

		self.openFiles(name)

		if self.loadParams(name):

			self.makeChunksHoles(name) if hasHoles else self.makeChunksProbe(name)


if __name__ == "__main__":

	progname = sys.argv[0]
	del sys.argv[0]

	basedir = os.open(".", os.O_DIRECTORY)

	# reasonable default, everyone is copying SEEK_DATA/SEEK_HOLE
	hasHoles = False if os.name == "nt" else True

	for arg in sys.argv:

		if arg[0] == "-":
			if arg == "-s":
				hasHoles = True
			elif arg == "-p":
				hasHoles = False
			elif arg == "-h":
				print("usage: {:s} [-h] [-s | -n] <file(s)>\n".format(progname))
				print("DZ Chunking program by Elliott Mitchell\n")
				print("optional arguments:")
				print("  -h                    show this help message and exit")
				print("  -s                    use SEEK_DATA/SEEK_HOLE (not available on all OSes)")
				print("  -p                    probe for holes (safe)")
				sys.exit(0)

			elif arg[0] == "-":
				print('[!] Unknown option "{:s}"'.format(arg))
				sys.exit(1)

			continue

		Image2Chunks(arg, hasHoles)

		os.fchdir(basedir)


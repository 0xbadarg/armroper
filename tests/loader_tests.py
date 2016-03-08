import unittest
from services.loader import ELF

class TestELF(unittest.TestCase):

	temp_binary = "/bin/ls"

	def loadbin(self):
		with open(self.temp_binary, mode='rb') as file:
			self.binary = file.read()
		file.close()
		self.elf = ELF(self.binary)

	def testGetFormat(self):
		self.loadbin()
		self.assertEqual(self.elf.getFormat(), "ELF")
	
	def testGetArch(self):
		self.loadbin()
		self.assertIsNotNone(self.elf.getArch())

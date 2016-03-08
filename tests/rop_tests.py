import unittest
from services.loader import ELF
from services.rop import Rop

class TestROP(unittest.TestCase):
	
	temp_binary = "/bin/ls"

	def testGetGadgets(self):
		roper = Rop(self.temp_binary)
		roper.run()
		self.assertIsNotNone(roper.gadgets)

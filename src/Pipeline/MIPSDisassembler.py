#Author: Andy O'Connell <aoconnel@bu.edu> <andrewoconnell89@gmail.com>
#
#	--------------------------   R-Format   --------------------------
#	o----------------------------------------------------------------o
#	| opcode  |    rs   |    rt    |   rd   | shift (shamt) |  funct |
#	|---------|---------|----------|--------|---------------|--------|
#	| 6 bits  |  5 bits |	5 bits | 5 bits |     5 bits    | 6 bits |
#	o----------------------------------------------------------------o

#	--------------  I-Format  ----------------
#	o----------------------------------------o
#	| opcode |    rs   |    rt    |  OFFSET  |
#	|--------|---------|----------|----------|
#	| 6 bits |  5 bits |  5 bits  | 16 bits  |
#	o----------------------------------------o

#	==================================   OPCODES   =================================
#	o-------------------------------------------------------------------------------o
#	|  mNEMONIC	|	MEANING					|   TYPE	|	OPCODE	|    FUNCTION	|
#	|===============================================================================|
#	|	add		|	ADD						|	R		|	0x00	|	0x20		|
#	|	sub		|	Subtract				|	R		|	0x00	|	0x22		|
#	|	and		|	Bit AND					|	R		|	0x00	|	0x24		|
#	|	or		|	Bit OR					|	R		|	0x00	|	0x25		|
#	|	slt		|	Set to 1 if Less than	|	R		|	0x00	|	0x2A		|
#	|	lw		|	Load Word				|	I		|	0x23	|	N/A			|
#	|	sw		|	Store Word				|	I		|	0x2B	|	N/A			|
#	|	beq		|	Branch if Equal			|	I		|	0x04	|	N/A			|
#	|	bne		|	Brance if Not Equal		|	I		|	0x05	|	N/A			|
#	o-------------------------------------------------------------------------------o

#	HEX Referance
#	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#	0 1 2 3 4 5 6 7 8 9 A  B  C  D  E  F

class Disassembler(object):
	OPCODE = { 0x23 : 'lw',
        0x20 : 'lb',
		0x2B : 'sw',
        0x28 : 'sb',
		0x04 : 'beq',
		0x05 : 'bne'}

	FUNCT = { 0x20 : 'add',
		0x22 : 'sub',
		0x24 : 'and',
		0x25 : 'or',
		0x2A : 'slt'}

	#Constructor
	def __init__(self):
		self.PC = 0x7A060
		self.PC_Inc = 0x4

		self.formatType = None
		self.instruction = None
		self.opcode = None
		self.rs = None
		self.rt = None
		self.rd = None
		self.offset = None
		self.shamt = None
		self.funct = None

	def load(self,instruction):
		self.instruction = instruction

		#isolate the OPCODE
		# 1111 1100 0000 0000 0000 0000 0000 0000
		#   F    C   0    0    0    0    0    0
		opcode_MASK = 0xfc000000
		#print("OpCode Mask: ","{0:b}".format(opcode_MASK))

		#print("Instruction: ","{0:b}".format(self.instruction))
		self.opcode = self.instruction & opcode_MASK
		#print("Result     : ","{0:b}".format(self.opcode))

		self.opcode = self.opcode >> 26
		#print("Bit Shifted: ","{0:b}".format(self.opcode))

		#R Format
		if self.opcode == 0:
			#We want to designate this object to be of type R
			self.formatType = 'R'

			#RS MASK
			# 0000 0011 1110 0000 0000 0000 0000 0000
			#  0    3    E    0    0    0    0    0
			#Source Register
			rs_MASK = 0x03E00000
			self.rs = self.instruction & rs_MASK
			self.rs = self.rs >> 21

			#RT MASK
			# 0000 0000 0001 1111 0000 0000 0000 0000
			#  0    0    1    F    0    0    0    0
			rt_MASK = 0x001F0000
			self.rt = self.instruction & rt_MASK
			self.rt = self.rt >> 16

			#RD MASK
			# 0000 0000 0000 0000 1111 1000 0000 0000
			#  0    0    0    0    F    8    0    0
			rd_MASK = 0x0000F800
			self.rd = self.instruction & rd_MASK
			self.rd = self.rd >> 11

			#SHAMT MASK
			# 0000 0000 0000 0000 0000 0111 1100 0000
			#  0    0    0    0    0    7    C    0
			shamt_MASK = 0x000007C0
			self.shamt = self.instruction & shamt_MASK
			self.shamt = self.shamt >> 6

			#FUNCT MASK
			# 0000 0000 0000 0000 0000 0000 0011 1111
			#  0    0    0    0    0    0    3    F
			funct_MASK = 0x0000003F
			self.funct = self.instruction & funct_MASK



		#I Format
		elif self.opcode > 0:
			#We want to designate this object to be of type I
			self.formatType = 'I'

			#RS MASK
			# 0000 0011 1110 0000 0000 0000 0000 0000
			#  0    3    E    0    0    0    0    0
			#Source Register
			rs_MASK = 0x03E00000
			self.rs = self.instruction & rs_MASK
			self.rs = self.rs >> 21

			#RT MASK
			# 0000 0000 0001 1111 0000 0000 0000 0000
			#  0    0    1    F    0    0    0    0
			rt_MASK = 0x001F0000
			self.rt = self.instruction & rt_MASK
			self.rt = self.rt >> 16

			#OFFSET MASK
			# 0000 0000 0000 0000 1111 1111 1111 1111
			#  0    0    0    0    F    F    F    F
			offset_MASK = 0x0000FFFF
			self.offset = self.instruction & offset_MASK
			if (Disassembler.OPCODE[self.opcode]) == 'beq' or (Disassembler.OPCODE[self.opcode] == 'bne'):
				self.offset = (self.offset << 2) + 0x4
			if self.offset >= 32768:
				self.offset = self.offset - 65536

		print(self.__str__())
		self.PC += self.PC_Inc


	def __str__(self):
		if self.formatType == 'I':
			#self.debugI()
			if Disassembler.OPCODE[self.opcode] == 'lw':
				return '{0:x}'.format(self.PC) + \
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d}'.format(self.rt) +\
					', {0:d}'.format(self.offset) +\
					'(${0:d}'.format(self.rs) + ')'

			elif Disassembler.OPCODE[self.opcode] == 'lb':
				return '{0:x}'.format(self.PC) + \
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d}'.format(self.rt) +\
					', {0:d}'.format(self.offset) +\
					'(${0:d}'.format(self.rs) + ')'

			elif Disassembler.OPCODE[self.opcode] == 'beq':
				return '{0:x}'.format(self.PC) +\
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d},'.format(self.rs) +\
					' ${0:d},'.format(self.rt) +\
					' address 0x{0:x}'.format(self.offset+self.PC)

			elif Disassembler.OPCODE[self.opcode] == 'bne':
				return '{0:x}'.format(self.PC) +\
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d},'.format(self.rs) +\
					' ${0:d},'.format(self.rt) +\
					' address 0x{0:x}'.format(self.offset+self.PC)

			elif Disassembler.OPCODE[self.opcode] == 'sw':
				return '{0:x}'.format(self.PC) +\
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d}'.format(self.rt) +\
					' {0:d}'.format(self.offset) +\
					'(${0:d}'.format(self.rs) + ')'

			elif Disassembler.OPCODE[self.opcode] == 'sb':
				return '{0:x}'.format(self.PC) +\
					'  ' + Disassembler.OPCODE[self.opcode] +\
					' ${0:d}'.format(self.rt) +\
					' {0:d}'.format(self.offset) +\
					'(${0:d}'.format(self.rs) + ')'

			else:
				return '{0:x}'.format(self.PC) +\
					'  ' + Disassembler.OPCODE[self.opcode]+\
					' ${0:d}'.format(self.rt) +\
					', ${0:d}'.format(self.offset) +\
					'({0:d}'.format(self.rs) + ')'


		elif self.formatType == 'R':
			#self.debugR()
			return '{0:x}'.format(self.PC) +\
				'  ' + Disassembler.FUNCT[self.funct] +\
				' ${0:d},'.format(self.rd) +' '+\
				'${0:d},'.format(self.rs) +' '+\
				'${0:d}'.format(self.rt)

		else:
			return ('Something Went Wrong....', self.instruction)

	#Not used
	def r(self, register):
		print(type(register), register)
		try:
			tmp = Disassembler.REGISTER[register]
			print(tmp)
			return tmp
		except:
			return '{0:d}'.format(register)


	def debugI(self):
		print('\n')
		print('RAW:  {0:b}'.format(self.instruction))
		print('OPC:  {0:b}'.format(self.opcode))
		print('RS:   {0:b}'.format(self.rs))
		print('RT:   {0:b}'.format(self.rt))
		print('OFFS: {0:b}'.format(self.offset))


	def debugR(self):
		print('\n')
		print('RAW:  {0:b}'.format(self.instruction))
		print('OPC:  {0:b}'.format(self.opcode))
		print('RS:   {0:b}'.format(self.rs))
		print('RT:   {0:b}'.format(self.rt))
		print('RD:   {0:b}'.format(self.rd))
		print('SHAMT:{0:b}'.format(self.shamt))
		print('FUNCT:{0:b}'.format(self.funct))

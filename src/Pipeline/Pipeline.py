#Author: Andy O'Connell <aoconnel@bu.edu> <andrewoconnell89@gmail.com>
#
#	--------------------------   R-Format   --------------------------
#	o----------------------------------------------------------------o
#	| opcode  |    rs   |    rt    |   rd   | shift (shamt) |  funct |
#	|---------|---------|----------|--------|---------------|--------|
#	| 6 bits  |  5 bits |	5 bits | 5 bits |     5 bits    | 6 bits |
#	o----------------------------------------------------------------o
#   op op op op op op rs rs rs rs rs rt rt rt rt rt rd rd rd rd rd rd -- -- -- -- -- fc fc fc fc fc
#   31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
#
#	--------------  I-Format  ----------------
#	o----------------------------------------o
#	| opcode |    rs   |    rt    |  OFFSET  |
#	|--------|---------|----------|----------|
#	| 6 bits |  5 bits |  5 bits  | 16 bits  |
#	o----------------------------------------o
#   op op op op op op rs rs rs rs rs rt rt rt rt rt of of of of of of of of of of of of of of of of
#   31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
#
#	==================================   OPCODES   =================================
#	o-------------------------------------------------------------------------------o
#	|  mNEMONIC	|	MEANING					|   TYPE	|	OPCODE	|    FUNCTION	|
#	|===============================================================================|
#	|	add		|	ADD						|	R		|	0x00	|	0x20		|
#   |	sub		|	Subtract				|	R		|	0x00	|	0x22		|
#   |   nop     |   Null operation          |   R       |   0x00    |   0x00        |
#	|	lb		|	Load Byte				|	I		|	0x20	|	N/A			|
#	|	sb		|	Store Byte				|	I		|	0x28	|	N/A			|
#	o-------------------------------------------------------------------------------o
#
#	HEX Referance
#	0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
#	0 1 2 3 4 5 6 7 8 9 A  B  C  D  E  F

from Pipeline.MIPSDisassembler import Disassembler # This is from Project 1

class Pipeline(object):

    def __init__(self, startProgramCount, InstructionCache):
        """Initalizes the 5 Stages of the Pipeline. (IF, ID, EX, MEM, WB)
        """

        #Main Memory, Registers.  Must be initialized
        self.Main_Mem = None
        self.initializeMainMem()
        self.Regs = None
        self.initializeRegs()

        # Instructions to be used.  = {0x7A000 : 0xa1020000,}
        self.InstructionCache = InstructionCache
        self.PC = startProgramCount


        #----------------------------------------------------------------------
        #IF/ID Write
        self.IFID_W_Inst    = 0
        self.IFID_W_IncrPC  = 0

        #IF/ID Read
        self.IFID_R_Inst    = 0
        self.IFID_R_IncrPC  = 0




        #----------------------------------------------------------------------
        #ID/EX Write
        self.IDEX_W_RegDst = 0
        self.IDEX_W_ALUSrc = 0
        self.IDEX_W_ALUOp = 0
        self.IDEX_W_MemRead = 0
        self.IDEX_W_MemWrite = 0
        self.IDEX_W_Branch = 0
        self.IDEX_W_MemToReg = 0
        self.IDEX_W_RegWrite = 0

        self.IDEX_W_IncrPC = 0
        self.IDEX_W_ReadReg1Value = 0
        self.IDEX_W_ReadReg2Value = 0
        self.IDEX_W_SEOffset = 0
        self.IDEX_W_WriteReg_20_16 = 0
        self.IDEX_W_WriteReg_15_11 = 0
        self.IDEX_W_Function = 0

        #ID/EX Read
        self.IDEX_R_RegDst = 0
        self.IDEX_R_ALUSrc = 0
        self.IDEX_R_ALUOp = 0
        self.IDEX_R_MemRead = 0
        self.IDEX_R_MemWrite = 0
        self.IDEX_R_Branch = 0
        self.IDEX_R_MemToReg = 0
        self.IDEX_R_RegWrite = 0

        self.IDEX_R_IncrPC = 0
        self.IDEX_R_ReadReg1Value = 0
        self.IDEX_R_ReadReg2Value = 0
        self.IDEX_R_SEOffset = 0
        self.IDEX_R_WriteReg_20_16 = 0
        self.IDEX_R_WriteReg_15_11 = 0
        self.IDEX_R_Function = 0


        #----------------------------------------------------------------------
        #EX/MEM Write
        self.EXMEM_W_MemRead = 0
        self.EXMEM_W_MemWrite = 0
        self.EXMEM_W_Branch = 0
        self.EXMEM_W_MemToReg = 0
        self.EXMEM_W_RegWrite = 0
        self.EXMEM_W_CalcBTA = 0
        self.EXMEM_W_Zero = 0
        self.EXMEM_W_ALUResult = 0

        self.EXMEM_W_SWValue = 0
        self.EXMEM_W_WriteRegNum = 0

        #EX/MEM Read
        self.EXMEM_R_MemRead = 0
        self.EXMEM_R_MemWrite = 0
        self.EXMEM_R_Branch = 0
        self.EXMEM_R_MemToReg = 0
        self.EXMEM_R_RegWrite = 0
        self.EXMEM_R_CalcBTA = 0
        self.EXMEM_R_Zero = 0
        self.EXMEM_R_ALUResult = 0

        self.EXMEM_R_SWValue = 0
        self.EXMEM_R_WriteRegNum = 0


        #----------------------------------------------------------------------
        #MEM/WB Write
        self.MEMWB_W_MemToReg = 0
        self.MEMWB_W_RegWrite = 0

        self.MEMWB_W_LWDataValue = 0
        self.MEMWB_W_ALUResult = 0
        self.MEMWB_W_WriteRegNum = 0

        #MEM/WB Read
        self.MEMWB_R_MemToReg = 0
        self.MEMWB_R_RegWrite = 0

        self.MEMWB_R_LWDataValue = 0
        self.MEMWB_R_ALUResult = 0
        self.MEMWB_R_WriteRegNum = 0


    def IF_stage(self):
        """You will fetch the next instruction out of the Instruction Cache.
        Put it in the WRITE version of the IF/ID pipeline Register """
        print('\n-------------IF-------------')
        print("GlobalPC: {0:x}".format(self.PC))
        #IF/ID Write
        self.IFID_W_Inst    = self.InstructionCache[self.PC]
        self.IFID_W_IncrPC  = self.PC + 0x4

        self.PC = self.PC + 0x4

        # DEBUG
        print("IFID_W_Inst: {0:x}".format(self.IFID_W_Inst))
        print("IFID_W_IncrPC: {0:x}".format(self.IFID_W_IncrPC))




    def ID_stage(self):
        """Here you'll read an instruction from the READ version of IF/ID
        pipeline register, do the decoding and register fetching and write the
        values to the WRITE version of the ID/EX pipeline register."""
        print('\n-------------ID-------------')
        # Null Operation Condition
        if self.IFID_R_Inst == 0:
            self.IDEX_W_RegDst = 0
            self.IDEX_W_ALUSrc = 0
            self.IDEX_W_ALUOp = 0
            self.IDEX_W_MemRead = 0
            self.IDEX_W_MemWrite = 0
            self.IDEX_W_Branch = 0
            self.IDEX_W_MemToReg = 0
            self.IDEX_W_RegWrite = 0
            self.IDEX_W_IncrPC = 0
            self.IDEX_W_ReadReg1Value = 0
            self.IDEX_W_ReadReg2Value = 0
            self.IDEX_W_SEOffset = 0
            self.IDEX_W_WriteReg_20_16 = 0
            self.IDEX_W_WriteReg_15_11 = 0
            self.IDEX_W_Function = 0
            print("ID_stage: nop")
            return True


        d = Disassembler()
        d.load(self.IFID_R_Inst)
        print("Instruction: {0:x}".format(self.IFID_R_Inst)," ",d)
        print("IFID_R_IncrPC: {0:x}".format(self.IFID_R_IncrPC))

        # Set Control Variables
        if d.formatType == 'R':
            print("R")
            self.IDEX_W_RegDst = 1
            self.IDEX_W_ALUSrc = 0
            self.IDEX_W_ALUOp = 2
            self.IDEX_W_MemRead = 0
            self.IDEX_W_MemWrite = 0
            self.IDEX_W_Branch = 0
            self.IDEX_W_MemToReg = 0
            self.IDEX_W_RegWrite = 1    # End of Control
            self.IDEX_W_ReadReg1Value = self.Regs[d.rs]
            self.IDEX_W_ReadReg2Value = self.Regs[d.rt]
            self.IDEX_W_SEOffset = 'x'
            self.IDEX_W_WriteReg_20_16 = d.rs
            self.IDEX_W_WriteReg_15_11 = d.rt
            self.IDEX_W_Function = d.funct

        elif d.opcode == 0x20: #lb
            self.IDEX_W_RegDst = 0
            self.IDEX_W_ALUSrc = 1
            self.IDEX_W_ALUOp = 0
            self.IDEX_W_MemRead = 1
            self.IDEX_W_MemWrite = 0
            self.IDEX_W_Branch = 0
            self.IDEX_W_MemToReg = 1
            self.IDEX_W_RegWrite = 1    # End of Control
            self.IDEX_W_ReadReg1Value = self.Regs[d.rs]
            self.IDEX_W_ReadReg2Value = self.Regs[d.rt]
            self.IDEX_W_SEOffset = d.offset
            self.IDEX_W_WriteReg_20_16 = d.rs
            self.IDEX_W_WriteReg_15_11 = d.rt
            self.IDEX_W_Function = 'x'
        elif d.opcode == 0x28: #sb
            self.IDEX_W_RegDst = 'x'
            self.IDEX_W_ALUSrc = 1
            self.IDEX_W_ALUOp = 0
            self.IDEX_W_MemRead = 0
            self.IDEX_W_MemWrite = 1
            self.IDEX_W_Branch = 0
            self.IDEX_W_MemToReg = 'x'
            self.IDEX_W_RegWrite = 0    # End of Control
            self.IDEX_W_ReadReg1Value = self.Regs[d.rs]
            self.IDEX_W_ReadReg2Value = self.Regs[d.rt]
            self.IDEX_W_SEOffset = d.offset
            self.IDEX_W_WriteReg_20_16 = d.rs
            self.IDEX_W_WriteReg_15_11 = d.rt
            self.IDEX_W_Function = 'x'

        print("IDEX_W_ReadReg1Value: {0:x}".format(self.IDEX_W_ReadReg1Value))
        print("IDEX_W_ReadReg2Value: {0:x}".format(self.IDEX_W_ReadReg2Value))
        print("IDEX_W_SEOffset ",self.IDEX_W_SEOffset)
        print("IDEX_W_WriteReg_20_16 ",self.IDEX_W_WriteReg_20_16)
        print("IDEX_W_WriteReg_15_11 ",self.IDEX_W_WriteReg_15_11)
        print("IDEX_W_Function ",self.IDEX_W_Function)

    def EX_stage(self):
        """ Here you'll perform the requested instruction on the spicific
        operands you read out of the READ version of the ID/EX pipeline register
        and then write the appropriate values to the WRITE version of the EX/MEM
        pipeline register.  For example, an "add" operation will take the two
        operands out of the ID/EX pipeline register and add them
        together like this:

        EX_MEM_WRITE.ALU_Result = ID_EX_READ.Reg_Val1 + ID_EX_READ.Reg_Val2;
        """
        print('\n-------------EX-------------')
        #EX/MEM Write
        #IDEX_R_
        self.EXMEM_W_MemRead = IDEX_R_MemRead
        self.EXMEM_W_MemWrite = IDEX_R_MemWrite
        self.EXMEM_W_Branch = IDEX_R_Branch
        self.EXMEM_W_MemToReg = IDEX_R_MemToReg
        self.EXMEM_W_RegWrite = IDEX_R_RegWrite
        #self.EXMEM_W_CalcBTA = "????"  # This is for Branches
        self.EXMEM_W_Zero = "????"

        self.EXMEM_W_ALUResult = 0
        self.EXMEM_W_SWValue = 0
        self.EXMEM_W_WriteRegNum = 0

    def MEM_stage(self):
        """If the instruction is a lb, then use the address you calculated in
        the EX stage as an index into your Main Memory array andget the value
        that is there.  Otherwise, just pass information from the READ version
        of the EX_MEM pipeline register to the WRITE version of MEM_WB.
        """
        print('\n-------------MEM-------------')

    def WB_stage(self):
        """Write to the registers based on information you read out of the READ
        version of MEM_WB.
        """
        print('\n-------------WB-------------')

    def Print_out_everything(self):
        pass

    def Copy_write_to_read(self):
        #IF/ID Read
        self.IFID_R_Inst    = self.IFID_W_Inst
        self.IFID_R_IncrPC  = self.IFID_W_IncrPC

        #ID/EX Read
        self.IDEX_R_RegDst = self.IDEX_W_RegDst
        self.IDEX_R_ALUSrc = self.IDEX_W_ALUSrc
        self.IDEX_R_ALUOp = self.IDEX_W_ALUOp
        self.IDEX_R_MemRead = self.IDEX_W_MemRead
        self.IDEX_R_MemWrite = self.IDEX_W_MemWrite
        self.IDEX_R_Branch = self.IDEX_W_Branch
        self.IDEX_R_MemToReg = self.IDEX_W_MemToReg
        self.IDEX_R_RegWrite = self.IDEX_W_RegWrite

        self.IDEX_R_IncrPC = self.IDEX_W_IncrPC
        self.IDEX_R_ReadReg1Value = self.IDEX_W_ReadReg1Value
        self.IDEX_R_ReadReg2Value = self.IDEX_W_ReadReg2Value
        self.IDEX_R_SEOffset = self.IDEX_W_SEOffset
        self.IDEX_R_WriteReg_20_16 = self.IDEX_W_WriteReg_20_16
        self.IDEX_R_WriteReg_15_11 = self.IDEX_W_WriteReg_15_11
        self.IDEX_R_Function = self.IDEX_W_Function


        #EX/MEM Read
        self.EXMEM_R_MemRead = self.EXMEM_W_MemRead
        self.EXMEM_R_MemWrite = self.EXMEM_W_MemWrite
        self.EXMEM_R_Branch = self.EXMEM_W_Branch
        self.EXMEM_R_MemToReg = self.EXMEM_W_MemToReg
        self.EXMEM_R_RegWrite = self.EXMEM_W_RegWrite
        self.EXMEM_R_CalcBTA = self.EXMEM_W_CalcBTA
        self.EXMEM_R_Zero = self.EXMEM_W_Zero
        self.EXMEM_R_ALUResult = self.EXMEM_W_ALUResult

        self.EXMEM_R_SWValue = self.EXMEM_W_SWValue
        self.EXMEM_R_WriteRegNum = self.EXMEM_W_WriteRegNum

        #MEM/WB Read
        self.MEMWB_R_MemToReg = self.MEMWB_W_MemToReg
        self.MEMWB_R_RegWrite = self.MEMWB_W_RegWrite

        self.MEMWB_R_LWDataValue = self.MEMWB_W_LWDataValue
        self.MEMWB_R_ALUResult = self.MEMWB_W_ALUResult
        self.MEMWB_R_WriteRegNum = self.MEMWB_W_WriteRegNum



    def initializeMainMem(self):
        self.Main_Mem = []
        for i in range(1024):
            self.Main_Mem.append( i & 0b000011111111 )

    def initializeRegs(self):
        self.Regs = []
        for i in range(32):
            self.Regs.append( i + 0x100)

        self.Regs[0] = 0 #Special Case for Reg 0

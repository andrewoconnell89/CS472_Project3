class Pipeline(object):

    def __init__(self):
        self.Main_Mem = None
        self.Regs = None

        #Control Variables
        self.RegDst = None
        self.Branch = None
        self.MemRead = None
        self.MemtoReg = None
        self.ALUOp = None
        self.MemWrite = None
        self.ALUSrc = None
        self.RegWrite = None

    def initializeMainMem(self):
        self.Main_Mem = []
        for i in range(1024):
            self.Main_Mem.append( i & 0b000011111111 )

    def initializeRegs(self):
        self.Regs = []
        for i in range(32):
            self.Regs.append( i + 0x100)

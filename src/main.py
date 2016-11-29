from Pipeline.Pipeline import Pipeline


#Starting Program Counter
startPC = 0x7A000

InstructionCache = {0x7A000 : 0xa1020000,
                        0x7A004 : 0x810AFFFC,
                        0x7A008 : 0x00831820,
                        0x7A00c : 0x01263820,
                        0x7A010 : 0x01224820,
                        0x7A004 : 0x81180000,
                        0x7A008 : 0x81510010,
                        0x7A00c : 0x00624022,
                        0x7A020 : 0x00000000,
                        0x7A004 : 0x00000000,
                        0x7A008 : 0x00000000,
                        0x7A00c : 0x00000000}


#Initalize new Pipeline object starting at specified PC
p = Pipeline(startPC, InstructionCache)

p.IF_stage()
p.ID_stage()
p.EX_stage()
p.MEM_stage()
p.WB_stage()
p.Print_out_everything()
p.Copy_write_to_read()

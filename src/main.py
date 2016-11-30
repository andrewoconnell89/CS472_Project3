from Pipeline.Pipeline import Pipeline


#Starting Program Counter
startPC = 0x7A000

InstructionCache = {    0x7A000 : 0xa1020000,
                        0x7A004 : 0x810AFFFC,
                        0x7A008 : 0x00831820,
                        0x7A00C : 0x01263820,
                        0x7A010 : 0x01224820,
                        0x7A014 : 0x81180000,
                        0x7A018 : 0x81510010,
                        0x7A01c : 0x00624022,
                        0x7A020 : 0x00000000,
                        0x7A024 : 0x00000000,
                        0x7A028 : 0x00000000,
                        0x7A02c : 0x00000000}

# 0xa1020000 sb $2 0($8)
# 0x810AFFFC lb $10 -4($8)
# 0x00831820 add $3 $4 $3
# 0x01263820 add $7 $9 $6
# 0x01224820 add $9 $9 $2
# 0x81180000 lb $24 0($8)
# 0x81510010 lb $17 16($10)
# 0x00624022 sub $8 $3 $2




#Initalize new Pipeline object starting at specified PC
p = Pipeline(startPC, InstructionCache)
for i in range(1,13):
    print('\n================ Clock Cycle %s ==============' % i)
    p.IF_stage()
    p.ID_stage()
    p.EX_stage()
    p.MEM_stage()
    p.WB_stage()
    p.Print_out_everything()
    p.Copy_write_to_read()

#test for sb $2 0($8)
print("\n---------UNIT TESTING BELOW-------------------")
print("\nTest1: sb $2 0($8) -- Value should be x102")
print("     Main_Mem[x{0:x}] = x{1:x}".format(0x108, p.Main_Mem[0x108]))
print("\nTest2: lb $10 -4($8) -- Value should be x4")
print("     Regs[{0:d}] = x{1:x}".format(10, p.Regs[10]))
print("\nTest3: add $3 $4 $3 -- Value should be x207")
print("     Regs[3] = x{0:x}".format(p.Regs[3]))
print("\nTest4: add $7 $9 $6 -- Value should be x20F")
print("     Regs[7] = x{0:x}".format(p.Regs[7]))
print("\nTest5: add $9 $9 $2 -- Value should be x20B")
print("     Regs[9] = x{0:x}".format(p.Regs[9]))
print("\nTest6: lb $24 0($8) -- Value should be x102 (due to instruction in 1)")
print("     Regs[24] = x{0:x}".format(p.Regs[24]))
print("\nTest7: lb $17 16($10) -- Value should be x14 ($10=x4+x10 then Main_Mem[x14]=x14  Register 10 was changed in test2)")
print("     Regs[17] = x{0:x}".format(p.Regs[17]))
print("\nTest8: sub $8 $3 $2 -- Value should be x309")
print("     Regs[8] = x{0:x}".format(p.Regs[8]))


#for i in range(len(p.Main_Mem)):
#    print("{0:x} - {0:x}".format(i,p.Main_Mem[i]))

#for i in range(len(p.Regs)):
#    print("{0:x} - {0:x}".format(i,p.Regs[i]))

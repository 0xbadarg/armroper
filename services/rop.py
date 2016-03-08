
from capstone import *
from src.gadgets import *
from services.loader import *
from struct import unpack
from capstone.arm_const import *


class GType:
    GT_Move_Reg = 1     # mov r0, r2
    GT_Arithm_Const = 2 # add r1, #1
    GT_Arithm_Reg = 3   # add r1, r1, r2
    GT_Load_Mem = 4     # ldr r0, [r2, #4]
    GT_Store_Mem = 5    # str r3, [r0, #8]
    GT_Load_Const = 6   # pop {r0, r4, lr}
    GT_Syscall = 7      # svc 0x0
    GT_Jump = 8         # blx, bx
    GT_Inv = 9          # other insn


class Rop:
    def __init__(self, path):
        self.gadgets = []
        self.typeDict = {
            GType.GT_Move_Reg : [],
            GType.GT_Arithm_Const : [],
            GType.GT_Arithm_Reg : [],
            GType.GT_Load_Mem : [],
            GType.GT_Store_Mem : [],
            GType.GT_Load_Const: [],
            GType.GT_Syscall : [],
            GType.GT_Jump : [],
            GType.GT_Inv : [],
            }

        self.__binary = None
        with open(path, mode='rb') as file:
            self.__binary = file.read()
        file.close()
        self.elf = ELF(self.__binary)
        
    def run(self, depth = 5, mode = "arm"):
        sections = self.elf.getExecSections()
        g = Gadget(self.elf, depth, mode)
        for s in sections:
            self.gadgets.append(g.getROPGadgets(s))

        #self.output()
        self.classifyGadgets()
        #self.print_gadget_class()


    def print_gadget_class(self):

        for i in self.typeDict.keys():
            if i == GType.GT_Inv:
                continue

            print("type: %d" %(i))
            for j in self.typeDict[i]:
                print(j["gadget"],)
                print(self.regs_rw(j))


    def GadgetType(self, node):
        # syscall type
        if "svc" in node["gadget"]:
            return GType.GT_Syscall

        for opcode in node["insn"]:
            if opcode.mnemonic == "svc":
                return GType.GT_Syscall
            elif opcode.mnemonic == "pop":
                return GType.GT_Load_Const        #print array
        #print len(array)
            elif opcode.mnemonic == "ldr":
                return GType.GT_Load_Mem
            elif opcode.mnemonic == "str":
                return GType.GT_Store_Mem
            elif opcode.mnemonic == "mov":
                if opcode.op_count(ARM_OP_REG) == 2:
                    return GType.GT_Move_Reg
                else:
                    return GType.GT_Inv
            elif opcode.mnemonic == "add":
                #print "op == add"
                #print opcode.op_str
                reg_num = opcode.op_count(ARM_OP_REG)
                imm_num = opcode.op_count(ARM_OP_IMM)
                if reg_num >= 3:
                    return GType.GT_Arithm_Reg
                elif (reg_num == 2 or reg_num == 1) and imm_num == 1:
                    return GType.GT_Arithm_Const
            elif opcode.mnemonic == "blx" or opcode.mnemonic == "bx":
                return GType.GT_Jump
            else:
                return GType.GT_Inv

    def classifyGadgets(self):
        for i in self.gadgets:
            for j in i:
                Gtype = self.GadgetType(j)
                self.typeDict[Gtype].append(j)

    def output(self):
        for i in self.gadgets:
            for j in i:
                print(" [+] Gadget found! 0x%x : %s [+]" %(j["vaddr"], j["gadget"]))

    def printBytes(self, array):
        index = 0
        ret = []
        step = 4

        while index < len(array):
            if (len(array) - index) >= 4:
                step = 4
                ret += [unpack("<I", array[index:index + step])]
            elif (len(array) - index) >= 2:
                step = 2
                ret += [unpack("<H", array[index:index + step])]
            else:
                step = 1
                ret += [unpack("<B", array[index:index + step])]
            index += step

        for i in ret:
            print("0x%x" %(i),)
        print("")

    def regs_rw(self, node):
        ret = {"read": [],
                "write": []
                }
        
        for ins in node["insn"]:
            regs = ins.op_str.replace(' ','').split(',')
            if ins.mnemonic == "mov":
                if len(regs) == 2:
                    if not regs[1] in ret:
                        ret["read"].append(regs[1])
                    if not regs[0] in ret:
                        ret["write"].append(regs[0])

            elif ins.mnemonic == "add":
                ret["write"].append(regs[0])
                ret["read"].append(regs[1])
                if len(regs) == 3:
                    ret["read"].append(regs[2])
            elif ins.mnemonic == "ldr":
                ret["write"].append(regs[0])
                ret["read"].append(regs[1])
            elif ins.mnemonic == "str":
                ret["write"].append(regs[1])
                ret["read"].append(regs[0])
            elif ins.mnemonic == "pop":
                for r in regs:
                    r = r.replace('{', '')
                    r = r.replace('}', '')
                    ret["write"].append(r)
            elif ins.mnemonic == "blx" or ins.mnemonic == "bx":
                ret["read"].append(regs[0])
            elif ins.mnemonic == "orr":
                ret["write"].append(regs[0])
                ret["read"].append(regs[1])
                ret["read"].append(regs[2])
        return ret



import re
from capstone import *
import sys

gadget_arm = [
    [b"[\x30-\x3f]\xff\x2f\xe1", 4, 4], # blx, arm mode
    [b"[\x10-\x1f]\xff\x2f\xe1", 4, 4], # bx, arm mode
    [b"[\x00-\xff]\x80\xbd\xe8", 4, 4], # pop {,pc}, arm mode
    [b"[\x00-\xff]\x00\x00\xef", 4, 4], # swi, arm mode
]
gadget_thumb = [
    [b"[\x80-\xf8]\x47", 2, 2],         # blx, thumb mode
    [b"[\x00-\x78]\x47", 2, 2],         # bx, thumb mode
    [b"[\x00-\xff]\xbd", 2, 2],         # pop {,pc}, thumb mode
    [b"[\x00-\xff]\xdf", 2, 2],         # swi, thumb mode
]


class Gadget:
    def __init__(self, binary, depth, mode):
        self.__binary = binary
        self.__depth = depth
        self.__mode = mode


    def getROPGadgets(self, section):
        arch = self.__binary.getArch()
        archMode = self.__binary.getArchMode()
        gadgets = []
        if arch == CS_ARCH_X86:
            gadgets = [
                [b"\xc3", 1, 1], # ret
                [b"\xc2[\x00-\xff]{2}", 3, 1], # ret <imm>
            ]
        elif arch == CS_ARCH_ARM:
            if self.__mode == "arm":
                gadgets.extend(gadget_arm)
                gadgets.extend(gadget_thumb)

            elif self.__mode == "thumb":
                gadgets.extend(gadget_thumb)
            else:
                print("Error: Bad arm mode")
                sys.exit(-1)
            archMode = CS_MODE_ARM

        return self.findGadgets(section, gadgets, arch, archMode)

    def findGadgets(self, section, gadgets, arch, archMode):
        OP = 0
        SIZE = 1
        ALIGN = 2

        ret = []

        md = Cs(arch, archMode)
        md.detail = True
        md.syntax = CS_OPT_SYNTAX_ATT
        for gad in gadgets:
            allPos = [ m.start() for m in re.finditer(gad[OP], section["opcodes"])]
            for pos in allPos:
                for i in range(self.__depth):
                    if (section["vaddr"] + pos - (i * gad[ALIGN])) % gad[ALIGN] == 0: # align right
                        asms = md.disasm(section["opcodes"][pos - (i * gad[ALIGN]):pos + gad[SIZE]], section["vaddr"] + pos)
                        gadget = ""
                        insns = []
                        for asm in asms:
                            insns.append(asm)
                            gadget += (asm.mnemonic + " " + asm.op_str + " ; ").replace("  ", " ")
                        if len(gadget) > 0:
                            ret += [ {"vaddr": section["vaddr"] + pos - (i * gad[ALIGN]),
                                      "gadget": gadget,
                                      "codes": section["opcodes"][pos - (i * gad[ALIGN]): pos + gad[SIZE]],
                                      "insn": insns} ]

        return ret

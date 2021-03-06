from idc import *
from idautils import *
from deobfuscator import Deobfuscator
import utils

class RegPush(Deobfuscator):

    def __init__(self):
        super(RegPush, self).__init__()
        self.name = "register_push"
        self.type = "register push function"
        self.comment = "Does a register push according to the previous argument"
        self.op_map = op_reg = {
                '4Fh':'eax',
                '50h':'ecx',
                '51h':'edx',
                '52h':'ebx',
                '54h':'ebp',
                '55h':'esi',
                '56h':'edi'
                }

    def can_deobfuscate(self, address):
        return utils.get_instr_bytes(address) in ["837c24044f"]

    def label_caller(self, function_address, caller_address):
        push_address = PrevHead(caller_address)
        operand = self.get_operand(push_address)
        if operand not in self.op_map:
            print '[!] Unable to deobfuscate register push at 0x%x' % (push_address)
            return
        register = self.op_map[operand]
        comment1 = "(irrelevant) argument for register push"
        MakeComm(push_address, comment1)
        if not GetCommentEx(caller_address, 0):
            comment2 = "push %s" % (register)
            MakeComm(caller_address, comment2)

    def get_operand(self, address):
        return GetOpnd(address, 0)

import sys
from libs.expr import Expr
from libs.handle import Handle


class Ev:

    def __init__(self):
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', '->']
        self.keyWord = ['while', 'if', 'end']
        self.typeWord = ['int', 'str', 'float', 'bool']
        self.stdFunc = ['print']
        self.varActing = ['\"']
        self.matchMap = {}
        self.vars = {}
        self.handle = Handle(self.vars, self.matchMap, self.typeWord)

    def ev(self, scp, namespace=None):
        lines = [x for x in scp.split("\n") if x.strip() != ""]
        # 匹配关键字与end的行数
        self.ev_match(lines)
        pgCounter = 0
        while pgCounter < len(lines):
            tag = lines[pgCounter].split(maxsplit=1)[0]
            if tag in self.keyWord:
                pgCounter = self.handle.keyword(pgCounter, lines, namespace)
            elif tag in self.stdFunc:
                pgCounter = self.handle.stdfunc(pgCounter, lines, namespace)
            else:
                pgCounter = self.handle.assign(pgCounter, lines, namespace)



    def ev_match(self, lines):
        tempStack = []
        for i, line in enumerate(lines):
            tag = line.split(maxsplit=1)[0]
            if tag in self.keyWord:
                if tag == 'end':
                    startIdx = tempStack.pop()
                    self.matchMap[startIdx] = i
                    self.matchMap[i] = startIdx
                else:
                    tempStack.append(i)

    @staticmethod
    def ev_detect_varacting(_str : str):
        if _str.startswith('"') and _str.endswith('"'):
            return _str[1:-1]
        return ""

Ev().ev(open(sys.argv[1]).read())
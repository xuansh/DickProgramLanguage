import sys
from libs.Handle.handle import Handle


class Ev:

    def __init__(self):
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', '->']
        self.keyWord = ['while', 'if', 'end']
        self.typeWord = ['int', 'str', 'float', 'bool']
        self.stdFunc = ['print']
        self.varActing = ['\"']
        self.lines = []
        self.matchMap = {}
        self.vars = {}
        self.handle = Handle(self.vars, self.matchMap, self.typeWord, self.lines)

    def ev(self, scp, namespace=None):
        raw_lines = scp.split('\n')

        for line in raw_lines:
            stripped = line.strip()
            if not stripped:                # 空行
                continue
            if stripped.startswith('#'):     # 整行注释
                continue

            if '#' in stripped:              # 行内注释
                line = line.split('#', 1)[0]

            if line.strip():
                self.lines.append(line.rstrip())

        # 匹配关键字与end的行数
        self.ev_match(self.lines)
        pgCounter = 0
        while pgCounter < len(self.lines):
            tag = self.lines[pgCounter].split(maxsplit=1)[0]
            if tag in self.keyWord:
                pgCounter = self.handle.keyword(pgCounter, self.lines, namespace)
            elif tag in self.stdFunc:
                pgCounter = self.handle.stdfunc(pgCounter, self.lines, namespace)
            else:
                pgCounter = self.handle.assign(pgCounter, self.lines, namespace)


        # print "the result is " c -> toChar +

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

    def ev_getLineText(self, pgCounter : int):
        return lines[pgCounter]

    @staticmethod
    def ev_detect_varacting(_str : str):
        if _str.startswith('"') and _str.endswith('"'):
            return _str[1:-1]
        return ""

Ev().ev(open(sys.argv[1]).read())
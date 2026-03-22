import sys

class Ev:

    def __init__(self):
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']
        self.keyWord = ['while', 'if', 'end']
        self.stdFunc = ['print']
        self.varActing = ['\"']
        self.matchMap = {}
        self.vars = {}

    def ev(self, scp, namespace=None):
        lines = [x for x in scp.split("\n") if x.strip() != ""]
        # 匹配关键字与end的行数
        self.ev_match(lines)
        pgCounter = 0
        while pgCounter < len(lines):
            tag = lines[pgCounter].split(maxsplit=1)[0]
            if tag in self.keyWord:
                pgCounter = self.hd_keyword(pgCounter, lines, namespace)
            elif tag in self.stdFunc:
                pgCounter = self.hd_stdfunc(pgCounter, lines, namespace)
            else:
                pgCounter = self.hd_assign(pgCounter, lines, namespace)

    def hd_keyword(self, pgCounter, lines, namespace) -> int:
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'while' | 'if':
                if self.ev_expr(lines[pgCounter].split(maxsplit=1)[1]) == 1:
                    pgCounter += 1
                else:
                    pgCounter = self.matchMap[pgCounter]
                    pgCounter += 1
            case 'end':
                matchKeyWord = lines[self.matchMap[pgCounter]].split(maxsplit=1)[0]
                if matchKeyWord == 'while':
                    pgCounter = self.matchMap[pgCounter]
                elif matchKeyWord == 'if':
                    pgCounter += 1
            case _: ...
        return pgCounter

    def hd_assign(self, pgCounter, lines, namespace) -> int:
        (name, _, expr) = lines[pgCounter].split(maxsplit=2)
        self.vars[name] = self.ev_expr(expr)
        pgCounter += 1
        return pgCounter

    def hd_stdfunc(self, pgCounter, lines, namespace):
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'print':
                text = self.ev_expr(lines[pgCounter].split(maxsplit=1)[1])
                print(text)
                pgCounter += 1
            case _: ...
        return pgCounter

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

    def ev_expr(self, line):
        stack = []
        if self.ev_detect_varacting(self, line) != "":
            return self.ev_detect_varacting(self, line)

        tokens = line.split()
        for token in tokens:
            if token.isdigit():         stack.append(int(token))
            elif token in self.vars:    stack.append(self.vars[token])
            elif token in self.operator:
                rht = stack.pop()
                lft = stack.pop()
                if token == '+' :       stack.append(lft + rht)
                elif token == '-' :     stack.append(lft - rht)
                elif token == '*' :     stack.append(lft * rht)
                elif token == '/' :     pass # stack.append(rht / lft) 除法的处理较复杂 暂不考虑
                elif token == '>':
                    if lft > rht:       stack.append(1)
                    else:               stack.append(0)
                elif token == '<':
                    if lft < rht:       stack.append(1)
                    else:               stack.append(0)
                elif token == '>=':
                    if lft >= rht:      stack.append(1)
                    else:               stack.append(0)
                elif token == '<=':
                    if lft <= rht:      stack.append(1)
                    else:               stack.append(0)
                elif token == '==':
                    if lft == rht:      stack.append(1)
                    else:               stack.append(0)
                elif token == '!=':
                    if lft != rht:      stack.append(1)
                    else:               stack.append(0)

        return stack[0]

    @staticmethod
    def ev_detect_varacting(self, _str : str):
        if _str.startswith('"') and _str.endswith('"'):
            return _str[1:-1]
        return ""

Ev().ev(open(sys.argv[1]).read())
from libs.expr import Expr


class Handle:
    def __init__(self, var_dict, match_map_dict, typeword_dict):
        self.vars = var_dict
        self.matchMap = match_map_dict
        self.typeWord = typeword_dict
        self.expr = Expr(self.vars)

    def keyword(self, pgCounter, lines, namespace) -> int:
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'while' | 'if':
                if self.expr.eval(lines[pgCounter].split(maxsplit=1)[1]) == 1:
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

    def assign(self, pgCounter, lines, namespace) -> int:
        (name, colon, expr) = lines[pgCounter].split(maxsplit=2) # i : int = 1
        if colon == ':':
            (type, _, expr) = expr.split(maxsplit = 2)
            if type in self.typeWord:
                self.vars[name] : type = self.expr.eval(expr)
        elif colon == '=' :
            self.vars[name] = self.expr.eval(expr)
        else:
            ... # 这里写报错
        pgCounter += 1
        return pgCounter
        # self.vars[name] = self.expr.eval(expr)
        # pgCounter += 1
        # return pgCounter

    def stdfunc(self, pgCounter, lines, namespace):
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'print': # print i
                text = self.expr.eval(lines[pgCounter].split(maxsplit=1)[1])
                print(text)
                pgCounter += 1
            case _: ...
        return pgCounter
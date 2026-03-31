from libs.Handle.Expr.expr import Expr
import error as er

class Handle:
    def __init__(self, var_dict, match_map_dict, typeword_dict, lines_dict):
        self.vars = var_dict
        self.matchMap = match_map_dict
        self.typeWord = typeword_dict
        self.lines = lines_dict
        self.expr = Expr(self.vars, self.lines)

    def keyword(self, pgCounter, lines, namespace) -> int:
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'while' | 'if':
                if self.expr.eval(lines[pgCounter].split(maxsplit=1)[1], pgCounter) == 1:
                    pgCounter += 1
                else:
                    pgCounter = self.matchMap[pgCounter]
                    pgCounter += 1
            case 'for': ...

            case 'end':
                matchKeyWord = lines[self.matchMap[pgCounter]].split(maxsplit=1)[0]
                if matchKeyWord == 'while':
                    pgCounter = self.matchMap[pgCounter]
                elif matchKeyWord == 'if':
                    pgCounter += 1
            case _: ...
            # 报错 whdwhduiwhdiuwuh
        return pgCounter

    def assign(self, pgCounter, lines, namespace) -> int:
        if len(lines[pgCounter].split(maxsplit=2)) != 1:
            (name, colon, expr) = lines[pgCounter].split(maxsplit=2)
            if colon == ':':
                (type, _, expr) = expr.split(maxsplit = 2)
                if type in self.typeWord:
                    self.vars[name] : type = self.expr.eval(expr, pgCounter)
            elif colon == '=' :
                self.vars[name] = self.expr.eval(expr, pgCounter)
            else:
                stc = self.lines[pgCounter]
                er.errException(2, f"Expected ':' or '=', but found '{colon}'", pgCounter, stc)
        else:
            stc = self.lines[pgCounter]
            er.errException(2, f"Expected ':' or '=', but found none", pgCounter, stc)
        pgCounter += 1
        return pgCounter

    def stdfunc(self, pgCounter, lines, namespace):
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'print': # print i
                printStr = lines[pgCounter].split(maxsplit=1)[1]
                text = self.expr.eval(printStr, pgCounter)
                print(text)
                pgCounter += 1
            case _: ...
        return pgCounter
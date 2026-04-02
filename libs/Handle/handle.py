import re

from libs.Handle.Expr.expr import Expr
import error as er
from pathlib import Path

class Handle:
    def __init__(self, var_dict, match_map_dict, typeword_dict, lines_dict, libmap_dict):
        self.vars = var_dict
        self.matchMap = match_map_dict
        self.typeWord = typeword_dict
        self.lines = lines_dict
        self.libMap = libmap_dict
        self.quoteLib = {}
        self.expr = Expr(self.vars, self.lines, self.quoteLib, self.libMap)

    def keyword(self, pgCounter, lines, _namespace) -> int:
        match lines[pgCounter].split(maxsplit=1)[0]:

            case 'import': #import SQL as sql
                pure_lib = lines[pgCounter].split(maxsplit=1)[1] # pure_lib = SQL as sql
                if len(pure_lib.split()) == 3: # 当import后的字符 符合 xxx xx xxx 格式时
                    (lib, AS, lib_name) = pure_lib.split(maxsplit=2) # SQL as sql
                    if AS != 'as': # 在此基础上 检测是否符合 xxx as xxx 的格式
                        er.errException(2, f"Expect 'as' but found '{AS}'", pgCounter, lines[pgCounter])
                        # 报错 语法错误
                else:
                    lib = lib_name = pure_lib
                match lib:
                    case 'SQL':
                        lib_path = Path(__file__).parent / 'Expr' / 'SQL' / '__init__.py'
                    case 'System':
                        lib_path = Path(__file__).parent / 'Expr' / 'System' / '__init__.py'
                    case _:
                        er.errException(5, f"No module named '{lib}'", pgCounter, lines[pgCounter])
                        # 报错 找不到该库
                if lib_path.is_file():
                     self.quoteLib[lib_name] = lib
                pgCounter += 1

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

    def assign(self, pgCounter, lines, _namespace) -> int:
        stc = lines[pgCounter].strip()

        # 先处理 "name : type = expr"
        type_match = re.match(r'^([^:\s]+)\s*:\s*([^=\s]+)\s*=\s*(.+)', stc)
        if type_match:
            name, var_type, expr = type_match.groups()
            if var_type in self.typeWord:
                self.vars[name] = self.expr.eval(expr, pgCounter)
                pgCounter += 1
                return pgCounter

        # 再处理 "name = expr"（expr 内允许出现 ->）
        if '=' in stc:
            name, expr = stc.split('=', 1)
            name = name.strip()
            expr = expr.strip()
            if name and expr:
                self.vars[name] = self.expr.eval(expr, pgCounter)
                pgCounter += 1
                return pgCounter

        # 最后处理独立表达式 "expr -> 操作"
        if '->' in stc:
            left, right = stc.rsplit('->', 1)
            left = left.strip()
            right = right.strip()
            if left and right:
                self.expr.eval(stc, pgCounter)
                pgCounter += 1
                return pgCounter

        er.errException(2, "Expected ':', '=' or '->', but found invalid statement", pgCounter, lines[pgCounter])
        pgCounter += 1
        return pgCounter

    def stdfunc(self, pgCounter, lines, _namespace):
        match lines[pgCounter].split(maxsplit=1)[0]:
            case 'print': # print i
                printStr = lines[pgCounter].split(maxsplit=1)[1]
                text = self.expr.eval(printStr, pgCounter)
                print(text)
                pgCounter += 1
            case _: ...
        return pgCounter
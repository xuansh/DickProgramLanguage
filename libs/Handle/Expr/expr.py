import shlex

import error as er
# 先修复sql.py后再导入，此处先调整调用逻辑


class Expr:
    def __init__(self, var_dict, lines_dict, quote_lib_dict, libmap_dict):
        self.vars = var_dict
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']
        self.lines = lines_dict
        self.quote_word = quote_lib_dict
        self.libMap = libmap_dict

    def eval(self, line, pgCounter):
        stack = []
        tokens = shlex.split(line)
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit():
                stack.append(int(token))
            elif token in self.vars:
                stack.append(self.vars[token])
            elif token in self.operator:
                # 修复：栈长度校验（原逻辑用or错误）
                if len(stack) < 2:
                    stc = self.lines[pgCounter]
                    er.errException(2, f"invalid syntax: insufficient operands", pgCounter, stc)
                    break

                rht = stack.pop()
                lft = stack.pop()
                if token == '+':
                    if isinstance(lft, str) or isinstance(rht, str):
                        stack.append(str(lft) + str(rht))
                    else:
                        stack.append(lft + rht)
                elif token == '-':
                    stack.append(lft - rht)
                elif token == '*':
                    stack.append(lft * rht)
                elif token == '/':
                    if rht == 0:
                        er.errException(1, "division by zero", pgCounter, self.lines[pgCounter])
                    stack.append(lft / rht)
                elif token == '>':
                    stack.append(1 if lft > rht else 0)
                elif token == '<':
                    stack.append(1 if lft < rht else 0)
                elif token == '>=':
                    stack.append(1 if lft >= rht else 0)
                elif token == '<=':
                    stack.append(1 if lft <= rht else 0)
                elif token == '==':
                    stack.append(1 if lft == rht else 0)
                elif token == '!=':
                    stack.append(1 if lft != rht else 0)
            elif token == '->':
                # 检查是否有后续操作符
                if i + 1 >= len(tokens):
                    er.errException(2, "missing operation after ->", pgCounter, self.lines[pgCounter])
                    break

                operatingMethod = tokens[i + 1]
                if '.' in operatingMethod:
                    # 拆分库和方法（仅拆分一次，避免多小数点问题）
                    lib, lib_op = operatingMethod.split('.', 1)
                    if self.quote_word[lib] in self.libMap:
                        import importlib
                        module_path = self.libMap[self.quote_word[lib]]
                        module = importlib.import_module(module_path)
                        setattr(self, self.quote_word[lib], module)
                        if not stack:
                            er.errException(2, f"no value for {self.quote_word[lib]} operation", pgCounter, self.lines[pgCounter])
                        stc = stack.pop()
                        res = module.Lib_find(self, stc, lib_op, pgCounter)
                        stack.append(res)
                    i += 1
                # 后面这两个operatingMethod或许也需要封装成模块或者库
                elif operatingMethod == 'toChar':
                    if not stack:
                        er.errException(2, "no value for toChar", pgCounter, self.lines[pgCounter])
                    _str = stack.pop()
                    stack.append(str(_str))
                    i += 1
                elif operatingMethod == 'toOrder':
                    if not stack or len(str(stack[-1])) != 1:
                        stc = self.lines[pgCounter]
                        er.errException(1, f"toOrder expected a single char", pgCounter, stc)
                    _char = stack.pop()
                    stack.append(ord(_char))
                    i += 1
                else:
                    er.errException(3, f"unknown operation {operatingMethod}", pgCounter, self.lines[pgCounter])
            elif token.lower() == 'true':
                stack.append(1)
            elif token.lower() == 'false':
                stack.append(0)
            elif any([
                token in line,
                f'"{token}"' in line
            ]):
                stack.append(token)
            else:
                stc = self.lines[pgCounter]
                er.errException(3, f"name '{token}' is not defined", pgCounter, stc)
            i += 1

        if len(stack) != 1:
            er.errException(2, "invalid expression (multiple values)", pgCounter, self.lines[pgCounter])
        return stack[0]
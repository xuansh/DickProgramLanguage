import shlex
import error as er

class Expr:
    def __init__(self,var_dict,lines_dict):
        self.vars = var_dict
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']
        self.lines = lines_dict


    def eval(self, line, pgCounter):
        stack = []
        tokens = shlex.split(line)
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit():         stack.append(int(token))
            elif token in self.vars:    stack.append(self.vars[token])
            elif token in self.operator:

                if (stack[-1] or stack[-2]) is None:
                    stc = self.lines[pgCounter]
                    er.errException(2, f"invalid syntax", pgCounter, stc)
                    break

                rht = stack.pop()
                lft = stack.pop()
                if token == '+' :
                    if isinstance(lft, str) or isinstance(rht, str):
                                        stack.append(str(lft) + str(rht))
                    else:
                                        stack.append(lft + rht)
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
            elif token == '->':
                operatingMethod = tokens[i + 1]
                if operatingMethod == 'toChar':
                    _str = stack.pop()
                    stack.append(str(_str))
                    i += 1
                elif operatingMethod == 'toOrder':
                    if len(stack[-1]) == 1:
                                        _char = stack.pop()
                                        stack.append(ord(_char))
                    else :
                        stc = self.lines[pgCounter]
                        er.errException(1, f"toOrder expected a single char, but got '{len(stack[-1])}'", pgCounter, stc)
                        # 报错 TypeError : variable contains length chars, but toOrder expected a char
            elif token.lower() == 'true':
                                        stack.append(1)
            elif token.lower() == 'false' :
                                        stack.append(0)
            elif f'"{token}"' in line:
                                        stack.append(token)
            # 任何既不带双引号的 又是未知变量 直接报错
            else:
                stc = self.lines[pgCounter]
                er.errException(3, f"name {token} is not defined", pgCounter, stc)
            i += 1
        return stack[0]


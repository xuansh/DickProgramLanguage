class Expr:
    def __init__(self,var_dict):
        self.vars = var_dict
        self.operator = ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']


    def detect_varacting(self,_str : str):
        if _str.startswith('"') and _str.endswith('"'):
            return _str[1:-1]
        return ""

    def eval(self, line):
        stack = []
        if self.detect_varacting(line) != "":
            return self.detect_varacting(line)

        tokens = line.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.isdigit():         stack.append(int(token))
            elif self.detect_varacting(token) != "":
                                        stack.append(self.detect_varacting(token))
            elif self.detect_varacting(line) != "":
                                        stack.append(token)
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
            elif token == '->':
                operatingMethod = tokens[i + 1]
                if operatingMethod == 'toChar':
                    _str = stack.pop()
                    stack.append(str(_str))
                    i += 1
                if operatingMethod == 'toOrder':
                    if len(stack[-1]) == 1:
                                        _char = stack.pop()
                                        stack.append(ord(_char))
                    else : ... # 报错 TypeError : variable contains length chars, but toOrder expected a char
            elif token.lower() == 'true':
                                        stack.append(1)
            elif token.lower() == 'false' :
                                        stack.append(0)
            i += 1
        return stack[0]


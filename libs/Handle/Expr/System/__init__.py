cmd_word = {'Run'}

def Lib_find(self, stc, operatingMethod, pgCounter):
    if operatingMethod in cmd_word:
        if not hasattr(self, 'cmd_handler'):
            from .cmd import CmdHandler
            self.cmd_handler = CmdHandler()
        return self.cmd_handler.handleCmd(stc, operatingMethod, pgCounter)
    return None

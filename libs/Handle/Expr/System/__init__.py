cmd_word = {'Run'}

def Lib_find(self, stc, operatingMethod, pgCounter):
    if operatingMethod in cmd_word:
        if not hasattr(self, '_handler'):
            from .cmd import CmdHandler
            #self.


import sys

sql_word = {'Conn', 'Execute', 'Fetchall', 'Commit', 'Close'}


def Lib_find(self, stc, operatingMethod, pgCounter):
    if operatingMethod in sql_word:
        if not hasattr(self, 'stc_handler'):
            from .stchandle import STCHandler
            self.stc_handler = STCHandler()
        return self.stc_handler.handleStc(stc, operatingMethod, pgCounter)
    return None
    # 报错
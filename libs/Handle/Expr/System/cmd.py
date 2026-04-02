import os
from os import system
import error as er

class CmdHandler:
    def __init__(self):
        ...

    def handleCmd(self, stc: str, operatingMethod: str, pgCounter: int):
        try:
            match operatingMethod:
                case 'Run':
                    os.system(stc)
                    return True
                case _:
                    return er.errException(6, f"module 'System' has no attribute '{operatingMethod}'", pgCounter, stc)
        except os.error as e:
            return er.errException(1000, f"{str(e)}", pgCounter, stc)

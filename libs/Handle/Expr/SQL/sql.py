import sqlite3

def __init__(self):
    self.conn = ''
    self.SqlWord = ['Exe']


def handleStc(self, stc, operatingMethod):
    match operatingMethod:
        case 'conn':
            conn_name = stc
            self.conn = sqlite3.connect(conn_name)
            return True
        case 'Exct':
            ...

        case _:
            return None
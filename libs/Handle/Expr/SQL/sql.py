# OperateSys/libs/Handle/Expr/SQL/sql.py
import sqlite3

# 补充类定义（原代码缺少类，__init__和handleStc无归属）
class SQLHandler:
    def __init__(self):
        self.conn = ''
        self.cursor = ''

    def handleStc(self, stc, operatingMethod):
        match operatingMethod:
            case 'Conn':
                conn_name = stc
                self.conn = sqlite3.connect(conn_name)  # 连接数据库

            case 'Execute':
                if not self.conn:  # 增加连接校验
                    raise Exception("SQL connection not initialized")
                self.cursor = self.conn.cursor()
                self.cursor.execute(stc)

            case 'Fetchall':
                if not self.cursor:
                    raise Exception("SQL cursor not initialized")
                rows = self.cursor.fetchall()  # 返回查询结果
                for row in rows:
                    print(row)
                return True

            case 'Commit':
                return self.conn.commit()

            case 'Close':
                if self.conn:
                    self.conn.close()  # 修正重复close的问题
                    self.conn = ''  # 重置连接

            case _:
                return None

        return True
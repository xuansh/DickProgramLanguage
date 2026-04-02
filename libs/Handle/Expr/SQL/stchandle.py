import sqlite3
import error as er


class STCHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def handleStc(self, stc: str, operatingMethod: str, pgCounter: int):
        """
        处理 SQL 相关指令
        :param stc: SQL 语句或数据库名称
        :param operatingMethod: 操作类型
        :param pgCounter: 错误处理所需的行计数器
        """
        try:
            match operatingMethod:
                case 'Conn':
                    # 关闭旧连接（如果存在）
                    if self.conn:
                        self.conn.close()
                    self.conn = sqlite3.connect(stc)
                    return True

                case 'Execute':
                    if not self.conn:
                        return er.errException(4, "No active connection", pgCounter, stc)

                    # 建议每次执行重新获取 cursor 以保证最新状态
                    self.cursor = self.conn.cursor()
                    self.cursor.execute(stc)
                    return True

                case 'Fetchall':
                    if not self.cursor:
                        return er.errException(4, "No active cursor (Execute SQL first)", pgCounter, stc)

                    rows = self.cursor.fetchall()
                    for row in rows:
                        print(row)
                    return True

                case 'Commit':
                    if self.conn:
                        self.conn.commit()
                        return True
                    return er.errException(4, "Commit failed: No connection", pgCounter, stc)

                case 'Close':
                    if self.cursor:
                        self.cursor.close()
                        self.cursor = None
                    if self.conn:
                        self.conn.close()
                        self.conn = None
                    return True

                case _:
                    return er.errException(6, f"module 'SQL' has no attribute '{operatingMethod}'", pgCounter, stc)

        except sqlite3.Error as e:
            # 如果是执行阶段出错，尝试回滚
            if self.conn and operatingMethod in ['Execute', 'Commit']:
                self.conn.rollback()
            # 将具体的 SQL 错误传给错误处理模块
            return er.errException(4, f"{str(e)}", pgCounter, stc)

        except Exception as e:
            return er.errException(4, f"System Error: {str(e)}", pgCounter, stc)
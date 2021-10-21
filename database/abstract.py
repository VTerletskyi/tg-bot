import sqlite3
from loguru import logger


class AbstractRepository:

    def __init__(self, path_file):
        try:
            self.conn = sqlite3.connect(path_file)
            self.cur = self.conn.cursor()
            logger.debug(f"Connecting to {self.conn}")

        except sqlite3.Error as error:
            logger.error(f"Error connecting to sqlite3 {error}")

    def initialize(self, _list: list):
        return [self.cur.execute(i) for i in _list]

    def select(self, params: dict):
        return self.cur.execute(
            f'''SELECT {', '.join(params["columns"])} FROM {params["tableName"]} WHERE {', '.join(params["condition"])}'''
        ).fetchall()

    def upsert(self, params: dict):
        self.cur.execute(
            f'''INSERT OR REPLACE INTO {params["tableName"]} VALUES ({', '.join(params["values"])});'''
        )
        self.conn.commit()
        return self.cur.lastrowid

    # def update(self, params: dict):
    #     self.cur.execute(
    #         f'''UPDATE {params["tableName"]} SET {', '.join(params["replace"])} WHERE {', '.join(params["condition"])}'''
    #     )
    #     self.conn.commit()
    #     return self.cur.lastrowid

    def __del__(self):
        logger.debug("Connection closed")
        self.cur.close()

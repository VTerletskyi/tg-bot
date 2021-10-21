from datetime import datetime
from pathlib import Path

from backend.database.abstract import AbstractRepository


class Corpus(AbstractRepository):

    @staticmethod
    def generate_relation(telegram_id, operation):
        return \
            {
                "tableName": "corpus",
                "columns":
                    [
                        "telegram_id",
                        "time",
                        "operation"
                    ],
                "columnsTypes":
                    {
                        "telegram_id": "INTEGER",
                        "time": "REAL",
                        "operation": "TEXT"
                    },
                "values":
                    [
                        f"{telegram_id}",
                        f"'{datetime.now()}'",
                        f"'{operation}'"
                    ]
            }

    def __init__(self, params):
        super().__init__(path_file=Path(f"backend/database/users.db").absolute())
        self.params = params
        self.columnsTypes = [' '.join((key, value)) for key, value in self.params["columnsTypes"].items()]

        self.initialize(
            [f'''CREATE TABLE IF NOT EXISTS {self.params["tableName"]} ({', '.join(self.columnsTypes)});'''])

    def insert_user_operation(self):
        return self.upsert(self.params)


if __name__ == "__main__":
    pass

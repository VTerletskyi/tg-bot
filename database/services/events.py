from pathlib import Path

from database.abstract import AbstractRepository


class Events(AbstractRepository):

    @staticmethod
    def generate_relation(dict_):
        return \
            {
                "tableName": "events",
                "columns":
                    [
                        "telegram_id",
                        "event_name",
                        "title",
                        "description",
                        "media",
                        "end_time"
                    ],
                "columnsTypes":
                    {
                        "telegram_id": "INTEGER",
                        "event_name": "TEXT",
                        "title": "TEXT",
                        "description": "TEXT",
                        "media": "TEXT",
                        "end_time": "TEXT",

                    },
                "values":
                    [
                        f"'{dict_['telegram_id']}'",
                        f"'{dict_['event_name']}'",
                        f"'{dict_['title']}'",
                        f"'{dict_['description']}'",
                        f"'{dict_['media']}'",
                        f"'{dict_['end_time']}'"
                    ],
                "condition":
                    [
                        f"telegram_id = {dict_['telegram_id']}",
                        # f"title = '{dict_['title']}'",
                        # f"description = '{dict_['description']}'",
                        # f"media = '{dict_['media']}'",
                        # f"end_time = '{dict_['end_time']}'"

                    ]
            }

    def __init__(self, params):
        super().__init__(path_file=Path(f"../database/events.db").absolute())
        self.params = params
        self.columnsTypes = [' '.join((key, value)) for key, value in self.params["columnsTypes"].items()]
        self.initialize(
            [f'''CREATE TABLE IF NOT EXISTS {self.params["tableName"]} ({', '.join(self.columnsTypes)});'''])

    def upsert_event(self):
        return self.upsert(self.params)

    def select_event(self):
        return self.select(self.params)

    # def update_user_language(self):
    #     return self.update(self.params)


if __name__ == "__main__":
    pass
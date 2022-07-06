import os

import psycopg2


class DBWriter:
    is_connect = False
    conn = None
    cur = None

    def __init__(self):
        if result := self.connect_db():
            self.conn, self.cur = result
            self.prepare_table()
            self.is_connect = True

    def __del__(self):
        if self.conn:
            self.cur.close()
            self.conn.close()

    @staticmethod
    def connect_db():
        try:
            conn = psycopg2.connect(
                database=os.environ.get('POSTGRES_NAME'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                port=5432,
                host=os.environ.get('POSTGRES_HOST')
            )
            return conn, conn.cursor()
        except psycopg2.OperationalError:
            print("Нет соединения с БД, проверьте настройки подключения.")

    def prepare_table(self):
        cur = self.cur
        cur.execute("""
        CREATE TABLE IF NOT EXISTS region_notes (
        name VARCHAR(255) NOT NULL,
        year INTEGER NOT NULL,
        value INTEGER NOT NULL
        );
        """)
        cur.execute("DELETE FROM region_notes;")

    def insert_db(self, values):
        self.cur.execute(f"""
        INSERT INTO region_notes (name, year, value)
        values {','.join(values)};
        """)
        self.conn.commit()

    @staticmethod
    def prepare_data(data):
        headers = data[0]
        _, _, *years = headers
        regions = data[1:]
        query_values = []
        for region in regions:
            name, _, *values = region
            years_values = zip(years, values)
            for year, value in years_values:
                query_values.append(
                    str((name, year, value))
                )
        return query_values

    def write_data(self, data: list[list]):
        query_values = self.prepare_data(data)
        self.insert_db(query_values)

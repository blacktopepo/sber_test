import os

import psycopg2


class DBWriter:
    is_connect = False

    def __init__(self):
        if result := self.connect_db():
            self.conn, self.cur = result
            self.make_tables()
            self.is_connect = True

    def __del__(self):
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
                host="db"
            )
            return conn, conn.cursor()
        except psycopg2.OperationalError:
            print("Нет соединения с БД, проверьте настройки подключения.")


    def make_tables(self):
        cur = self.cur
        cur.execute("""
        DROP DATABASE IF EXISTS region_notes;
        """)
        cur.execute("""
        CREATE TABLE region_notes (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        year INTEGER NOT NULL,
        value INTEGER NOT NULL
        );
        """)

    def insert_db(self, values):
        self.cur.execute("""
        INSERT INTO region_notes (name, year, value)
        values {','.join(values)};
        """
        )
        self.conn.commit()

        self.cur.execute('select * from region_notes;')
        print(self.cur.fetchall())

    def prepare_data(self, data):
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

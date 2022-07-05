import psycopg2 as psycopg2


class DBWriter:
    is_connect = False

    def __init__(self):
        if result := self.connect_db():
            self.conn, self.cur = result
            self.make_db()
            self.is_connect = True



    @staticmethod
    def connect_db():
        try:
            conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="postgres",
                port="5432",
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

    def insert_db(self, query):
        self.cur.execute(f"""
        INSERT INTO region_notes (name, year, value)
        values {query};
        """
        )

    def write_data(self, data):
        headers = data[0]
        _, _, *years = headers
        years = {count: year for count, year in enumerate(years)}
        regions = data[1:]
        for region in regions:



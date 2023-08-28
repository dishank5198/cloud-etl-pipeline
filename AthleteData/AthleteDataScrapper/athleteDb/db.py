import psycopg2


class PostgresConnector:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname="postgres",
            )
            self.cur = self.conn.cursor()
            print("Connected to PostgreSQL!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        self.cur.close()
        self.conn.close()
        print("Disconnected from PostgreSQL.")

    def create_table(self, table_name):
        try:
            self.cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, school TEXT, firstName TEXT, lastName TEXT, sportName TEXT, jerseyNumber TEXT, position TEXT, weight TEXT, height TEXT, academicYear TEXT, hometown TEXT, previousSchool TEXT, email TEXT, insertedTime TIMESTAMP DEFAULT NOW());"
            )

            self.conn.commit()
            print(f"{table_name} table created successfully!")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_data(self, data, table_name):
        try:
            for row in data:
                values = tuple(row.values())
                placeholders = ','.join(['%s' for _ in range(len(row))])
                sql = f"INSERT INTO {table_name} ({','.join(row.keys())}) VALUES ({placeholders})"
                self.cur.execute(sql, values)
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
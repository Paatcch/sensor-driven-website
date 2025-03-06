""" Implementing helper functions and classes related to databases"""
import sqlite3

class MeasurementsDB:
    """ Handles the messurements database, so it can connect and do queries and insertions """
    db_conn = None
    db_name = None
    db_table_name = None

    def __init__(self, db_name: str = "Measurements", db_table_name: str = "measurements"):
        """ Initializes the database and its variables. Creates or connects to the database"""
        self.db_name = db_name
        self.db_table_name = db_table_name
        self.db_conn = sqlite3.connect(self.db_name + ".db")
        c = self.db_conn.cursor()

        # AUTOINCREMENT increments id by one every time a new touple is created,
        # if is is not declared in INSERT
        # measurement is in JSON format
        c.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.db_table_name}
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CO2 INTEGER,
                TVOC INTEGER,
                time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        )
        self.commit()

    def commit(self):
        """ Commits changes to the database"""
        self.db_conn.commit()

    def close(self):
        """ Closes the connection to the databse """
        self.db_conn.close()

    def add_measurement(self, CO2, TVOC): #skal jeg seriøst skrive det med småt for pylint. co2 gør ondt at kigge på...
        """ Adds a measurement to the database """
        c = self.db_conn.cursor()
        c.execute(f"""INSERT INTO {self.db_table_name} (CO2, TVOC)
                  VALUES (?, ?)""",(CO2, TVOC))
        self.commit()

    def get_measurements(self):
        """ Retrieves all measurements from the database """
        c = self.db_conn.cursor()
        c.execute(f"SELECT * from {self.db_table_name} ORDER BY time DESC")
        c.fetchall()

    def get_min(self, mes_type):
        """ Retrieves the smallest measurements of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        if mes_type in('CO2', 'TVOC'):
            c = self.db_conn.cursor()
            c.execute(f"SELECT MIN({mes_type}) FROM {self.db_table_name}")
            return c.fetchall()
        return None

    def get_max(self, mes_type):
        """ Retrieves the largest measurements of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        if mes_type in('CO2', 'TVOC'):
            c = self.db_conn.cursor()
            c.execute(f"SELECT MAX({mes_type}) FROM {self.db_table_name}")
            return c.fetchall()
        return None

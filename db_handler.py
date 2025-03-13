""" Implementing helper functions and classes related to databases"""
import sqlite3
from typing import List

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
        c.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.db_table_name}
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                CO2 INTEGER NOT NULL,
                TVOC INTEGER NOT NULL,
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

    def add_measurement(self, CO2, TVOC):
        """ Adds a measurement to the database """
        c = self.db_conn.cursor()
        c.execute(f"""INSERT INTO {self.db_table_name} (CO2, TVOC)
                  VALUES (?, ?)""",(CO2, TVOC))
        self.commit()

    def get_measurements(self) -> List[sqlite3.Row]:
        """ Retrieves all measurements from the database """
        c = self.db_conn.cursor()
        c.execute(f"SELECT * FROM {self.db_table_name} ORDER BY time DESC")
        return c.fetchall()

    def get_min(self, mes_type):
        """ Retrieves the smallest measurements of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        return self.get_extreme(mes_type, 'ASC')

    def get_max(self, mes_type):
        """ Retrieves the largest measurements of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        return self.get_extreme(mes_type, 'DESC')

    def get_latest(self, mes_type):
        """ Retrieves the latest measurement of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        if mes_type in('CO2', 'TVOC'):
            c = self.db_conn.cursor()
            c.execute(f"""SELECT {mes_type}, time FROM {self.db_table_name}
                      ORDER BY time DESC LIMIT 1""")
            return c.fetchone()
        return None

    def get_extreme(self, mes_type, direction):
        """ Retrieves the largest/smallets measurements of either CO2 or TVOC from the database 
            mes_type must either "CO2" or "TVOC"."""
        if mes_type in('CO2', 'TVOC'):
            c = self.db_conn.cursor()
            c.execute(f"""SELECT {mes_type}, time FROM {self.db_table_name}
                      ORDER BY {mes_type} {direction}, time DESC LIMIT 1""")
            return c.fetchone()
        print('You need to write "CO2" or "TVOC" :) ')
        return None

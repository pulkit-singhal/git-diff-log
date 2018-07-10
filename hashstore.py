import sqlite3

class HashStore(object):
	def __init__(self):
		self.__get_connection__()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS hashes (hash text)")
		self.__close_connection()

	def insert(self, value):
		self.__get_connection__()
		self.cursor.execute("INSERT IGNORE INTO hashes VALUES (?)", (value, ))
		self.__close_connection()

	def is_present(self, value):
		self.__get_connection__()
		self.cursor.execute("SELECT COUNT(*) FROM hashes WHERE hash = ?", (value, ))
		cnt = self.cursor.fetchone()[0]
		self.__close_connection()
		return cnt == 1

	def __get_connection__(self):
		self.conn = sqlite3.connect("ignored_hashes.db")
		self.cursor = self.conn.cursor()

	def __close_connection(self):
		self.conn.commit()
		self.conn.close()
import sqlite3

class HashStore(object):
	def __init__(self):
		self.__getConnection__()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS hashes (hash text)")
		self.__closeConnection()

	def insert(self, value):
		self.__getConnection__()
		self.cursor.execute("INSERT IGNORE INTO hashes VALUES (?)", (value, ))
		self.__closeConnection()

	def isPresent(self, value):
		self.__getConnection__()
		self.cursor.execute("SELECT COUNT(*) FROM hashes WHERE hash = ?", (value, ))
		cnt = self.cursor.fetchone()[0]
		self.__closeConnection()
		return cnt == 1

	def __getConnection__(self):
		self.conn = sqlite3.connect("ignored_hashes.db")
		self.cursor = self.conn.cursor()

	def __closeConnection(self):
		self.conn.commit()
		self.conn.close()
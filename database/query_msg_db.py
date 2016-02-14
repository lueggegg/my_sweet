import sqlite3

class msg_db_query:
	def __init__(self, count_per_page=20):
		self.conn = sqlite3.connect('message.db')
		self.curs = self.conn.cursor()
		self.count = self.record_count()
		self.count_per_page = count_per_page
		self.pages = (self.count + self.count_per_page -1)/self.count_per_page
		self.current_page = 0

	def __del__(self):
		self.conn.close()

	def record_count(self):
		try:
			self.curs.execute('SELECT COUNT(*) FROM msg')
			return self.curs.fetchone()[0]
		except Exception, e:
			print e

	def query_page(self, page):
		offset = page * self.count_per_page
		try:
			self.curs.execute('SELECT * FROM msg Limit %d, %d' % (offset, self.count_per_page))
			data = self.curs.fetchall()
			self.current_page = page
			return data
		except Exception, e:
			print e

	def query_last_page(self):
		return self.query_page(self.pages - 1)

	def query_first_page(self):
		return self.query_page(0)

	def query_pre_page(self):
		if self.current_page == 0:
			return self.query_first_page()
		return self.query_page(self.current_page - 1)

	def query_next_page(self):
		if self.current_page == self.pages - 1:
			return self.query_last_page()
		return self.query_page(self.current_page + 1)


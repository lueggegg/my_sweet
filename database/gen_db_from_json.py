import sqlite3
import re
import json
import os

class db_generator:
	def __init__(self):
		print 'begin db'
		self.conn = sqlite3.connect('message.db')
		self.curs = self.conn.cursor()
		self.create_table()
		self.json_path = '../jsons'

	def __del__(self):
		# self.drap_table()
		self.conn.commit()
		self.conn.close()
		print 'end db'

	def create_table(self):
		try:
			self.curs.execute('''
				CREATE TABLE IF NOT EXISTS msg(
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					sender TEXT,
					date TEXT,
					time TEXT,
					msg TEXT
					)
				''')
		except Exception, e:
			print e

	def drap_table(self):
		try:
			self.curs.execute('DROP TABLE IF EXISTS msg')
		except Exception, e:
			print e

	def insert_msg(self, sender, date, time, msg):
		self.curs.execute('INSERT INTO msg (sender, date, time, msg) VALUES (?, ?, ?, ?)', [sender, date, time, msg])

	def insert_to_db_from_a_json_file(self, filename):
		filename = '%s/%s' % (self.json_path, filename)
		fid = open(filename, 'r')
		data = fid.read()
		# data = data.decode('utf-8')
		data = re.sub('"([0-9]:[0-5][0-9]:[0-5][0-9])"', r'"0\1"', data)
		data = json.loads(data)
		for day_msg in data:
			_date = day_msg['date']
			for msg in day_msg['day_msg']:
				_sender = msg['sender']
				_time = msg['time']
				_msg = msg['msg']
				self.insert_msg(_sender, _date, _time, _msg)
		fid.close()

	def insert_all_jsons(self):
		files = self.find_all_json_files()
		for f in files:
			self.insert_to_db_from_a_json_file(f)

	def find_all_json_files(self):
		return os.listdir(self.json_path)

	def record_count(self):
		try:
			self.curs.execute('SELECT COUNT(*) FROM msg')
			return self.curs.fetchone()
		except Exception, e:
			print e

	def show_all(self):
		try:
			self.curs.execute('SELECT * FROM msg')
			data = self.curs.fetchall()
			for d in data:
				print "%u: %s  %s %s " % d[:-1]
				print "\t%s" % d[-1]
		except Exception, e:
			print e

	def show_limit(self, offset, count):
		try:
			self.curs.execute('SELECT * FROM msg Limit %d, %d' % (offset, count))
			data = self.curs.fetchall()
			for d in data:
				print "%u: %s  %s %s " % d[:-1]
				print "\t%s" % d[-1]
		except Exception, e:
			print e

	def execute(self, sql):
		try:
			self.curs.execute(sql)
			return self.curs.fetchall()
		except Exception, e:
			print e
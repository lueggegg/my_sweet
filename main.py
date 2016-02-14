# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import query_msg_db
from tornado.escape import xhtml_unescape
import os, re

g_port = 8888
g_template_path = 'template'
g_current_page = 0

class TestHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('%s/ff.html' % g_template_path)

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		record_url = "http:/localhost:%d/record" % 1234;
		self.render("%s/login.html" % g_template_path, user_name="你的名字", 
			author_name="作者名字", record_url=record_url)

class RecordHandler(tornado.web.RequestHandler):
	def initialize(self):
		self.msg_db = query_msg_db.msg_db_query()
		self.author = u'\u661f\u615f'
		# self.author = '星慟'
		# self.author = self.author.decode('gbk')

	def get_current_page(self):
			self.msg_db.current_page = int(self.get_argument("current_page")) - 1

	def get(self):
		page = self.get_argument('page', 'last')
		if page == 'last':
			msgs = self.msg_db.query_last_page()
		elif page == 'first':
			msgs = self.msg_db.query_first_page()
		elif page == 'pre':
			self.get_current_page()
			msgs = self.msg_db.query_pre_page()
		elif page == 'next':
			self.get_current_page()
			msgs = self.msg_db.query_next_page()
		else:
			page = int(page) - 1
			msgs = self.msg_db.query_page(page)
		msgs_map = []
		for msg in msgs:
			msg_map = {'sender': msg[1]
				, 'date': msg[2]
				, 'time': msg[3]
			}
			msg_map['msg'] = re.sub('<[iI][mM][gG] src="(.+?)"', r'<img src="static/\1"', msg[4])
			if msg_map['sender'] == self.author:
				msg_map['color'] = '#0c0'
			else:
				msg_map['color'] = '#00c' 
			msgs_map.append(msg_map)
		s = self.render_string("%s/record.html" % g_template_path, msgs=msgs_map,
			total_pages=self.msg_db.pages, current_page=self.msg_db.current_page+1)
		self.write(xhtml_unescape(s))

def makd_app():
	settings = {
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
	}
	return tornado.web.Application([
		(r'/', LoginHandler),
		(r'/login', LoginHandler),
		(r'/record', RecordHandler),
		(r'/test', TestHandler),
		], **settings)

def main(port=None):
	global g_port
	if port is None:
		port = g_port
	else:
		g_port = port
	app = makd_app()
	app.listen(port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	main()
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import sqlite3
import json

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

class DatabaseHandler():
    def __init__(self, dbName):
        conn = sqlite3.connect('scorelib.dat')
        self.cursor = conn.cursor()

    def _doQuery(self, author):
        return self.cursor.execute('select person.name, score.name, print.id from person left '
                            'join score_author on person.id = score_author.composer '
                            'join score on score_author.score = score.id '
                            'join edition on score.id = edition.score left '
                            'join print on edition.id = print.edition '
                            'where person.name like "%{}%"'.format(author))

    def getResult(self, author):
        result = self._doQuery(author)

        list = []
        for r in result:
            item = {}
            item['Composer'] = r[0]
            item['Score'] = r[1]
            item['PrintNumber'] = r[2]
            list.append(item)

        chain = json.dumps(list)
        return chain


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes('<html><head><title>Exercise 06.</title></head>', 'utf8'))
        self.query = urlparse(self.path).query
        if('f=json' in self.query):
            rx = re.compile(r"(.*author=)([^&]*)(.*)")
            m = rx.match(self.query)
            if m is not None:
                author = m.group(2)
                dh = DatabaseHandler('scorelib.dat')
                output = dh.getResult(author)
                self.wfile.write(bytes("<body><p>%s</p>" % output ,'utf8'))



        self.wfile.write(bytes("</body></html>", 'utf8'))

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print('Server is starting')
    try:
      httpd.serve_forever()
    except KeyboardInterrupt:
      pass
    httpd.server_close()
    print("Server has stopped")

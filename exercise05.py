from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes('<html><head><title>Title goes here.</title></head>', 'utf8'))
        self.wfile.write(bytes("<body><p>This is my page.</p>", 'utf8'))
        self.wfile.write(bytes("<p>You asked for: %s</p>" % self.path, 'utf8'))
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

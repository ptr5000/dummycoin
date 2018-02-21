
import SimpleHTTPServer
import SocketServer
import handler
import urlparse

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

URLS = {
    '/': handler.status,
    '/mine': handler.mine,
    '/wallet/create': handler.create_wallet,
    '/wallet/info': handler.wallet_info,
    '/wallet/send': handler.wallet_send
}

class DummyCoinHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        o = urlparse.urlparse(self.path)

        try:
            URLS[o.path]
        except:
            self.send_response(404)
            self.end_headers()
            return

        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.send_header('Access-Control-Request-Method','*')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(URLS[o.path](post_body))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Request-Method','*')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        
        self.end_headers()

PORT = 3001

httpd = SocketServer.TCPServer(("", PORT), DummyCoinHandler)

print "serving at port", PORT
httpd.serve_forever()


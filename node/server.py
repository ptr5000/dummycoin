
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
    def do_GET(self):
        o = urlparse.urlparse(self.path)

        try:
            URLS[o.path]
        except:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        self.wfile.write(URLS[o.path](o.query))

PORT = 3001

httpd = SocketServer.TCPServer(("", PORT), DummyCoinHandler)

print "serving at port", PORT
httpd.serve_forever()


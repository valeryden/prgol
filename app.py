import http.server
import socketserver

class HelloWorldHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, World!")

handler = HelloWorldHandler
with socketserver.TCPServer(("", 8000), handler) as httpd:
    print("Server started at localhost:8000")
    httpd.serve_forever()

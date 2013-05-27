from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import time
import json
from Queue import Queue

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/data':
            self.send_response(200)
            self.send_header("Content-type", "text/event-stream")
            self.end_headers()

            self.queue = Queue(0)
            self.server.client_manager.subscribe(self)
            while True:
                item = self.queue.get(True)
                sdata = json.dumps(item)
                try:
                    self.wfile.write('retry: 1000\ndata: ' + sdata + '\n\n')
                except:
                    self.server.client_manager.unsubscribe(handler)
                    return

        else:
            try:
                content, content_type = self.server.file_manager.read(self.path)
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content)
            except:
                self.send_response(404)



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, file_manager, client_manager):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.file_manager = file_manager
        self.client_manager = client_manager

class WebServer:
    def start(self, host, port, file_manager, client_manager):
        ThreadingMixIn.daemon_threads = True
        httpd = ThreadedHTTPServer((host, port), RequestHandler, file_manager, client_manager)
        print time.asctime(), "Server Starts - %s:%s" % (host, port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (host, port)


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
            queue = Queue(0)
            self.server.packet_queue.subscribe(queue)

            while True:
                item = queue.get(True)
                sdata = '{"host" : "%s", "port" : "%s"}' % (item['src'], item['dport'])
                try:
                    self.wfile.write('retry: 1000\ndata: ' + sdata + '\n\n')
                except:
                    self.server.packet_queue.unsubscribe(queue)
                    return

        elif self.path == '/dns':
            self.send_response(200)
            self.send_header("Content-type", "text/event-stream")
            self.end_headers()
            queue = Queue(0)
            self.server.dns_queue.subscribe(queue)

            while True:
                item = queue.get(True)
                sdata = '{"host" : "%s", "name" : "%s"}' % (item['host'], item['name'])
                try:
                    self.wfile.write('retry: 1000\ndata: ' + sdata + '\n\n')
                except:
                    self.server.dns_queue.unsubscribe(queue)
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
    def __init__(self, server_address, RequestHandlerClass, file_manager, packet_queue, dns_queue):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.file_manager = file_manager
        self.packet_queue = packet_queue
        self.dns_queue    = dns_queue

class WebServer:
    def __init__(self, file_manager, packet_queue, dns_queue):
        self.file_manager = file_manager
        self.packet_queue = packet_queue
        self.dns_queue    = dns_queue

    def start(self, host, port):
        ThreadingMixIn.daemon_threads = True
        httpd = ThreadedHTTPServer((host, port), RequestHandler, self.file_manager, self.packet_queue, self.dns_queue)
        print time.asctime(), "Server Starts - %s:%s" % (host, port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (host, port)


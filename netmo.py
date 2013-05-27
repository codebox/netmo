import socket, sys, time
from struct import *
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from threading import Lock,Thread
import json
import time
from Queue import Queue
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import os
from file_manager import FileManager

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8182

class Buffer:
    def __init__(self):
        self.clients = []

    def add(self, data):
        for client in self.clients:
            client.queue.put(data)

    def subscribe(self, client):
        self.clients.append(client)

    def unsubscribe(self, client):
        self.clients.remove(client)

buffer = Buffer()
file_manager = FileManager('web')

def packet_to_dict(packet):
    #http://www.binarytides.com/python-packet-sniffer-code-linux/
    ip_header = packet[0:20]
    iph = unpack('!BBHHHBBH4s4s' , ip_header)
     
    version_ihl = iph[0]
    version = version_ihl >> 4
    ihl = version_ihl & 0xF
    
    iph_length = ihl * 4

    protocol = iph[6]
    s_addr = socket.inet_ntoa(iph[8]);
    d_addr = socket.inet_ntoa(iph[9]);
    
    d = {}
    d['src'] =  str(s_addr)
    d['dest'] =  str(d_addr)
    d['protocol'] =  str(protocol)

    tcp_header = packet[iph_length:iph_length+20]
     
    #now unpack them :)
    tcph = unpack('!HHLLBBHHH' , tcp_header)
     
    source_port = tcph[0]
    dest_port = tcph[1]

    d['sport'] =  str(tcph[0])
    d['dport'] =  str(tcph[1])

    return d     

lock = Lock()

def setup_sniffer():
    def filter(d):
        if d.get('src') in ['192.168.1.9', '127.0.0.1']:
            return None
        return d

    def sniff(buffer):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except socket.error , msg:
            print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
         
        # receive a packet
        while True:
            packet = s.recvfrom(1024)
            d = packet_to_dict(packet[0])
            if filter(d):
                buffer.add(d)

    t = Thread(target=sniff, args = (buffer,))
    t.daemon = True
    t.start()

def item_to_json(item):
    return json.dumps(item)

def respond(handler):
    handler.queue = Queue(0)
    buffer.subscribe(handler)
    while True:
        item = handler.queue.get(True)
        sdata = item_to_json(item)
        try:
            handler.wfile.write('retry: 1000\ndata: ' + sdata + '\n\n')
        except:
            buffer.unsubscribe(handler)
            return


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        if s.path == '/data':
            s.send_response(200)
            s.send_header("Content-type", "text/event-stream")
            s.end_headers()

            respond(s)
        else:
            try:
                content, content_type = file_manager.read(s.path)
                s.send_response(200)
                s.send_header("Content-type", content_type)
                s.end_headers()
                s.wfile.write(content)
            except:
                s.send_response(404)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ ok """

if __name__ == '__main__':
    setup_sniffer()
    server_class = ThreadedHTTPServer
    ThreadingMixIn.daemon_threads = True
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

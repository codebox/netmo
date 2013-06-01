import socket
from threading import Thread
import time
from struct import *

class ReverseDns:
    def __init__(self, queue):
        self.cache = {}
        self.queue = queue

    def query(self, ip):
        def do_query():
            result = ip
            try:
                result = socket.gethostbyaddr(ip)[0]
                self.queue.submit({'host' : ip, 'name' : result})
                print 'resolved',ip,result
            except:
                print 'resolve failed',ip
            self.cache[ip] = result

        self.cache[ip] = ip
        t = Thread(target=do_query)
        t.daemon = True
        t.start()


    def lookup(self, ip):
        if ip not in self.cache:
            self.query(ip)

        return self.cache[ip]

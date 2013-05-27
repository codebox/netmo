import socket
from threading import Thread
from struct import *

class ReverseDns:
    def __init__(self):
        self.cache = {}

    def query(self, ip):
        def do_query():
            result = ip
            try:
                result = socket.gethostbyaddr(ip)[0]
                print 'resolved',ip,result
            except:
                pass
            self.cache[ip] = result

        self.cache[ip] = ip
        t = Thread(target=do_query)
        t.daemon = True
        t.start()


    def lookup(self, ip):
        if ip not in self.cache:
            self.query(ip)

        return self.cache[ip]

import socket
from threading import Thread
import time
from struct import *

class ReverseDns:
    def __init__(self, callback):
        self.cache = {}
        self.callback = callback

    def query(self, ip):
        def do_query():
            result = ip
            try:
                result = socket.gethostbyaddr(ip)[0]
                self.callback({'src' : ip, 'host' : result, 'count' : 0})
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

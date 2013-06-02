import socket
from threading import Thread
from struct import *
import string
import re

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

    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4
    h_size = iph_length + tcph_length * 4
    data_size = len(packet) - h_size
    data = packet[h_size:]

    text = filter(lambda x: x in string.printable.replace('"','').replace('  ', ' '), data)
    d['data'] = re.sub('\s\s+', ' ', text);

    return d     

class Sniffer:
    def __init__(self, queue, reverse_dns):
        self.queue = queue
        self.reverse_dns = reverse_dns

    def filter(self, d):
        if d.get('src') in ['127.0.0.1']:
            return None
        return d

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        
        def receive():
            while True:
                packet = s.recvfrom(1024)
                d = packet_to_dict(packet[0])
                if self.filter(d):
                    d['host'] = self.reverse_dns.lookup(d['src'])
                    self.queue.submit(d)

        t = Thread(target=receive)
        t.daemon = True
        t.start()


from file_manager import FileManager
from sniffer import Sniffer
from web_server import WebServer
from reverse_dns import ReverseDns
from Queue import Queue

class QueueManager:
    def __init__(self):
        self.callbackFns = []
        self.queue = Queue(0)

    def subscribe(self, callbackFn):
        self.callbackFns.append(callbackFn)

    def unsubscribe(self, callbackFn):
        self.callbackFns.remove(callbackFn)

    def start(self):
        while True:
            item = self.queue.get(True)
            for callbackFn in self.callbackFns:
                callbackFn(data)

    def submit(self, item):
        self.queue.put(item)


if __name__ == '__main__':
    packet_queue = Queue(0)
    dns_queue    = Queue(0)

    file_manager = FileManager('web')
    web_server   = WebServer(file_manager, packet_queue, dns_queue)

    reverse_dns = ReverseDns(dns_queue)

    sniffer = Sniffer(packet_queue, reverse_dns)
    sniffer.start()

    WebServer(file_manager, packet_queue, dns_queue).start('0.0.0.0', 8182)



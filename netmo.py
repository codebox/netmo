from file_manager import FileManager
from sniffer import Sniffer
from web_server import WebServer
from reverse_dns import ReverseDns
from Queue import Queue

class QueueManager:
    def __init__(self):
        self.queues = []

    def subscribe(self, queue):
        self.queues.append(queue)

    def unsubscribe(self, queue):
        self.queues.remove(queue)

    def submit(self, item):
        for queue in self.queues:
            queue.put(item)


if __name__ == '__main__':
    packet_queue = QueueManager()
    dns_queue    = QueueManager()

    file_manager = FileManager('web')
    web_server   = WebServer(file_manager, packet_queue, dns_queue)

    reverse_dns = ReverseDns(dns_queue)

    sniffer = Sniffer(packet_queue, reverse_dns)
    sniffer.start()

    WebServer(file_manager, packet_queue, dns_queue).start('0.0.0.0', 8182)



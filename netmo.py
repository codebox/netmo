from file_manager import FileManager
from sniffer import Sniffer
from web_server import WebServer

class ClientManager:
    def __init__(self):
        self.clients = []

    def on_packet(self, data):
        for client in self.clients:
            client.queue.put(data)

    def subscribe(self, client):
        self.clients.append(client)

    def unsubscribe(self, client):
        self.clients.remove(client)

file_manager = FileManager('web')
client_manager = ClientManager()

if __name__ == '__main__':
    sniffer = Sniffer(client_manager.on_packet)
    sniffer.start()
    WebServer().start('0.0.0.0', 8182, file_manager, client_manager)



import os.path

class FileManager:
    def __init__(self, file_dir):
        self.dir = os.path.abspath(file_dir)

    def get_content_type(self, file_name):
        _, ext = os.path.splitext(file_name)

        if ext:
            ext = ext.lower()

        if ext == '.html':
            return 'text/html'
        elif ext == '.css':
            return 'text/css'
        elif ext == '.js':
            return 'text/javascript'
        else:
            return 'text/plain'

    def read(self, file_name):
        path = os.path.abspath(self.dir + file_name)

        if path.startswith(self.dir) and os.path.exists(path):
            data = open(path).read()
            content_type = self.get_content_type(file_name)
            return (data, content_type)

        else:
            raise ValueError('not found: ' + file_name)


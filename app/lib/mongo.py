from pymongo import MongoClient


class ConnectionFactory(object):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def create(self):
        return MongoClient(
            host=self.host,
            port=self.port
        )

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


class Feed(object):

    def __init__(self, connection_factory: ConnectionFactory,
                 collection: str, db_name: str):
        self.instance = None
        self.connection_factory = connection_factory
        self._collection = collection
        self.db_name = db_name

    def connection(self) -> MongoClient:
        if not self.instance:
            self.instance = self.connection_factory.create()
            self.instance[self.db_name][self._collection]\
                .create_index('name', unique=True)
        return self.instance[self.db_name]

    def collection(self):
        return self.connection()[self._collection]

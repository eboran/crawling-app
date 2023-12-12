import pytest
import pymongo
import mongomock


@pytest.fixture
@mongomock.patch(servers=(('server.example.com', 27017),))
def mongo_client():
    return pymongo.MongoClient('server.example.com')

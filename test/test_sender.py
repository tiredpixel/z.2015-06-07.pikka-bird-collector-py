import json
from httmock import urlmatch, HTTMock
import msgpack

from pikka_bird_collector.sender import Sender


SERVER_HOST = 'pikka-bird.example.com'
SERVER_URI  = 'http://%s' % SERVER_HOST


@urlmatch(netloc=SERVER_HOST, path='/collections', method='post')
def mock_collections_post_201(url, request):
    # force parse
    if request.headers['Content-Type'] == 'application/json':
        json.loads(request.body)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        msgpack.unpackb(request.body, encoding='utf-8')
    
    return {
        'status_code': 201,
        'content':     {}}

@urlmatch(netloc=SERVER_HOST, path='/collections', method='post')
def mock_collections_post_204(url, request):
    return {
        'status_code': 204}

@urlmatch(netloc=SERVER_HOST, path='/collections', method='post')
def mock_collections_post_422(url, request):
    return {
        'status_code': 422,
        'content':     {}}

@urlmatch(netloc=SERVER_HOST, path='/collections', method='post')
def mock_collections_post_500(url, request):
    return {
        'status_code': 500,
        'content':     'very very broken'}


class TestSender:
    
    def test_send_json(self, collection_valid):
        sender = Sender(SERVER_URI, format='json')
        
        with HTTMock(mock_collections_post_201):
            r = sender.send(collection_valid)
        
        assert r == True
    
    def test_send_binary(self, collection_valid):
        sender = Sender(SERVER_URI, format='binary')
        
        with HTTMock(mock_collections_post_201):
            r = sender.send(collection_valid)
        
        assert r == True
    
    def test_send_204(self, collection_valid):
        sender = Sender(SERVER_URI)
        
        with HTTMock(mock_collections_post_204):
            r = sender.send(collection_valid)
        
        assert r == True
    
    def test_send_422(self, collection_valid):
        sender = Sender(SERVER_URI)
        
        with HTTMock(mock_collections_post_422):
            r = sender.send(collection_valid)
        
        assert r == False
    
    def test_send_500(self, collection_valid):
        sender = Sender(SERVER_URI)
        
        with HTTMock(mock_collections_post_500):
            r = sender.send(collection_valid)
        
        assert r == False
    
    def test_send_connection_failed(self, collection_valid):
        sender = Sender('http://localhost:666')
        
        r = sender.send(collection_valid)
        
        assert r == False

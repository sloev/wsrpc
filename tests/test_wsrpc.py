import sys
import json

from tornado.gen import coroutine, Return
from tornado.testing import AsyncTestCase, bind_unused_port, gen_test
from tornado.httpserver import HTTPServer
from tornado.websocket import websocket_connect
from wsrpc.server import create_app
from wsrpc.handler import add_to_ws_lookup

APP = create_app()

@coroutine
def echo(self, args, callback_id, FUNC_NAME):
    self.push(args, callback_id, FUNC_NAME)

class TestWsRPC(AsyncTestCase):
    def setUp(self):
        super(TestWsRPC, self).setUp()
        server = HTTPServer(APP)
        socket, self.port = bind_unused_port()
        server.add_socket(socket)

    def _create_client(self):
        return websocket_connect(
                'ws://localhost:{}/?username=joe&password=secret'.format(self.port)
                )

    @gen_test
    def test_add_echo_function(self):
        add_to_ws_lookup(echo)
        client = yield self._create_client()
        original_string = 'echo_this'
        json_string = json.dumps(
                {
                    'instruction':'echo',
                    'args':original_string,
                    'callback_id':'testing'
                    })
        client.write_message(json_string)
        response = yield client.read_message()
        json_dict = json.loads(response)
        echo_string = json_dict['args']
        self.assertEqual(echo_string, original_string)


    @gen_test
    def test_encode_and_decode_base64(self):
        client = yield self._create_client()
        original_string = 'echo_this'
        json_string = json.dumps(
                {
                    'instruction':'base64encode',
                    'args':original_string,
                    'callback_id':'testing'
                    })
        client.write_message(json_string)
        response = yield client.read_message()
        json_dict = json.loads(response)
        b64encoded_string = json_dict['args']
        json_string = json.dumps(
                {
                    'instruction':'base64decode',
                    'args':b64encoded_string,
                    'callback_id':'testing'
                    })
        client.write_message(json_string)
        response = yield client.read_message()
        json_dict = json.loads(response)
        processed_string = json_dict['args']
        self.assertEqual(processed_string, original_string)

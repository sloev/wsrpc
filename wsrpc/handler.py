from tornado.gen import coroutine
from tornado.websocket import WebSocketHandler
from functools import wraps
import base64
import json
import logging

INSTRUCTIONS = {}

def add_to_ws_lookup(func):
    func_name = func.__name__
    @wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['FUNC_NAME'] = func_name
        return func(*args, **kwargs)
    tmp_func = wrapper

    INSTRUCTIONS[func_name] = tmp_func

    return tmp_func

@add_to_ws_lookup
@coroutine
def base64encode(self, args, callback_id, FUNC_NAME):
    string = args
    logging.info("b64 encoding string %s", string)
    b64_string = base64.b64encode(string)
    self.push(b64_string, callback_id, FUNC_NAME)

@add_to_ws_lookup
@coroutine
def base64decode(self, args, callback_id, FUNC_NAME):
    b64string = args
    logging.info("b64 decoding string %s", b64string)
    string = base64.b64decode(b64string)
    self.push(string, callback_id, FUNC_NAME)

class WsRPCHandler(WebSocketHandler):
    @coroutine
    def open(self):
        user = self.settings['authenticator'](**self.request.arguments)
        if not user:
            self.clear()
            self.close()
            return
        self.username = user['username']

    def push(self, msg_data, callback_id=None, FUNC_NAME=None):
        if callback_id is None or FUNC_NAME is None:
            raise ValueError("push missing args")
        json_dict = {
                'args':msg_data,
                'callback_id':callback_id,
                'instruction':FUNC_NAME
                }
        string = json.dumps(json_dict)
        self.write_message(string)
        logging.info("pushed message to user:%s", self.username)

    def on_close(self):
        username = getattr(self, 'username',"not authenticated")
        logging.info("user:\"%s\" closed the websocket", username)

    @coroutine
    def on_message(self, string):
        instruction = None
        try:
            if not isinstance(string, basestring):
                raise ValueError("not string")
            json_dict = json.loads(string)
            if not isinstance(json_dict, dict):
                raise ValueError("not dict")
            if not 'args' in json_dict:
                json_dict['args'] = None

            instruction = json_dict['instruction']
            callback_id = json_dict['callback_id']
            args = json_dict['args']

            func = INSTRUCTIONS[instruction]
            yield func(self, args, callback_id)
        except KeyError, e:
            logging.exception(e.message)
        except ValueError, e:
            logging.exception(e.message)


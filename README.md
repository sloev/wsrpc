## WsRPC - RPC with python, tornado and websockets

This project is an extract from a private repository, all history has been removed and domain specific context removed aswell.

### What?

This project demonstrates how an RPC thru Websockets can be constructed using Tornado Websocket handlers.

The demo project introduces a lookup dictionary with functions that get different dependencies injected.

The functions are attached to the lookup table by a decorator that also can be used at runtime.

This means that you can call:

```python
add_to_ws_lookup(my_new_function)
```

and then a new RPCall will be available in the running Websocket. Connected Clients will not need to reconnect to see this.

####JSON format

The format is:

```javascript
{"instruction":"silly instruction", "args":"silly args", "callback_id":"34_callme"}
```

**instruction** is the name of the function you call, directly the same as the func name in python.

**args** can really be anything

**callback_id** is a voluntary(i havent checked how volluntary :-) id that you can give in order to better differentiate when receiving the responses. Remember the Websocket is full-duplex.

##How to run
install dependencies (atm. only tornado):

```bash
sudo pip install -r requirements.txt
```

see tests for dox, and run them:

```bash
python -m tornado.testing discover tests
```

##Copyright
Johannes Gårdsted Valbjørn 2016

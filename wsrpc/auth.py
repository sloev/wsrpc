import logging
db = {
        'users':{
            'joe':{
                'username':'joe',
                'password':'secret'
                }
            }
        }

def authenticator(*args, **kwargs):
    try:
        username = kwargs['username'][0]
        password = kwargs['password'][0]
        user = db['users'][username]
        if user['password'] == password:
            logging.info("auth matched")
            return user
    except KeyError:
        pass
    except TypeError:
        pass
    logging.warning("auth not matched")
    return None

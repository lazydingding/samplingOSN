#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Running Environment: Python 3.5.1"""

__version__ = '1.7'
__author__ = 'Luping Yu (lazydingding@gmail.com)'

'''Python SDK for renren API, designed for social network research'''

import socket
from urllib import request
from urllib.error import HTTPError

class API():
    '''For detailed API documents, please visit
    http://open.renren.com/wiki/English_version_for_API2'''

    def __init__(self, access_token_pool):
        '''Import access_token pool'''
        self.tokens = access_token_pool

    def __getattr__(self, attr):
        return Wrapper(self, attr)

class Wrapper():
    '''Dynamic invocation for each interface'''
    URL = "https://api.renren.com/v2/"

    def __init__(self, api, name):
        self.api = api
        self.name = name

    def __getattr__(self, attr):
        return Wrapper(self.api, "%s/%s" % (self.name, attr))

    def __call__(self, **kw):
        url = self.URL + self.name + encode_params(**kw)
        return http_request(self.api, url)

def encode_params(**kw):
    '''Return a URL-encoded string for a dictionary of paramteres.'''
    s = '?'
    for k, v in kw.items():
        s = s + str(k) + '=' + str(v) + '&'
    return s.strip('&')

def http_request(api, url0):
    while True:
        f = None
        url = url0 + "&access_token=%s" % api.tokens[0]
        # timeout = 15s
        # socket.setdefaulttimeout(10)
        try:
            # f = request.urlopen(url)
            f = request.urlopen(url, timeout=15)
            return f.read().decode('utf-8')
        except HTTPError as e:
            if not error_handling(api, e):
                return None
        #except IOError as e: IncompleteRead
        except Exception as e:
            print(e)
        finally:
            if f:
                f.close()
            # print("token: " + self.tokens[0])

def error_handling(api, e):
    '''Extract error message'''
    message = e.read().decode('utf-8')
    if "invalid_authorization.INVALID-TOKEN" in message:
        delete_token(api)
        return True
    elif "forbidden.APP_OVER_INVOCATION_LIMIT" in message:
        change_token(api)
        return True
    elif "The requested resource () is not available" in message:
        print("APIError: Invalid interface name!")
    elif ("invalid_request.USER_NOT_EXIST" in message or
    "forbidden.NO_RIGHT" in message):
        pass
    else:
        print(message)

def change_token(api):
    '''Change the token if it overs the limit'''
    api.tokens.append(api.tokens[0])
    api.tokens.pop(0)
    print("New-TOKEN:%s" % api.tokens[0])

def delete_token(api):
    '''Delete the token if it is invalid'''
    print("Invalid-TOKEN:%s" % api.tokens[0])
    api.tokens.pop(0)

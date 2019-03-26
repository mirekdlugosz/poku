# -*- coding: utf-8 -*-

""" Pocket auth utils """

import requests


def get_request_token(consumer_key):
    """ get request token from api """
    data = {'consumer_key': consumer_key, 'redirect_uri': 'getpocket.com'}
    headers = {'x-accept': 'application/json'}
    r = requests.post('https://getpocket.com/v3/oauth/request',
                      data=data, headers=headers)
    if r.ok:
        return r.json()['code']
    else:
        return None


def generate_auth_url(request_token):
    """ return auth url for user to authorize application """
    url = ('https://getpocket.com/auth/authorize'
           '?request_token={0}'
           '&redirect_uri=https://getpocket.com').format(request_token)

    return url


def get_access_token(consumer_key, request_token):
    """ get access token from api """
    data = {'consumer_key': consumer_key, 'code': request_token}
    headers = {'x-accept': 'application/json'}
    r = requests.post('https://getpocket.com/v3/oauth/authorize',
                      data=data, headers=headers)
    if r.ok:
        return r.json()['access_token']
    else:
        return None


def get_items(consumer_key, access_token):
    """ get a list pocket items from api """
    data = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'detailType': 'complete'
    }
    r = requests.post('https://getpocket.com/v3/get', data=data)

    if r.ok:
        return [i for i in r.json()['list'].values()]
    else:
        return None


def item_to_dict(p_item):
    """ convert pocket item to universal dict """
    out = {
        'url': p_item.get('resolved_url') or p_item.get('given_url'),
        'title': p_item.get('resolved_title') or p_item.get('given_title'),
        'tags': sorted(p_item.get('tags', {}).keys()),
        'timestamp': int(p_item.get('time_updated'))
    }

    return out

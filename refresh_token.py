#!/usr/bin/env python

import sys
import json
import requests
import yaml
import urllib.parse


def encode_url(prefix: str, queries: dict) -> str:
    u = urllib.parse.urlparse(prefix)
    q = urllib.parse.urlencode(queries)

    _ = (u[0], u[1], u[2], '', q, '')
    access_url = urllib.parse.urlunparse(_)

    return access_url


def refresh_token():
    """ request a new access token using the refresh token """
    with open('clientkeys.yml', 'r') as k, open('tokens.yml', 'r') as t:
        keys = yaml.load(k)
        tokens = yaml.load(t)

    queries = keys
    queries.pop('redirect_uri')
    queries['grant_type'] = 'refresh_token'
    try:
        queries['refresh_token'] = tokens['refresh_token']
    except KeyError:
        print('tokens.yml seems broken')
        sys.exit()

    _url = 'https://www.producteev.com/oauth/v2/token'
    url = encode_url(_url, queries)

    res = requests.get(url)
    tokens = json.loads(res.text)
    # need exception when 'error' has been returned from the server
    with open('tokens.yml', 'w') as outfile:
        yaml.dump(tokens, outfile)


if __name__ == '__main__':
    refresh_token()

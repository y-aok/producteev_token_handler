#!/usr/bin/env python

import json
import requests
import urllib.parse
import yaml
from flask import Flask, request

k = open('clientkeys.yml', 'r')

app = Flask(__name__)

init_url = 'https://www.producteev.com/oauth/v2/auth'
init_queries = yaml.load(k)
init_queries['response_type'] = 'code'
init_queries.pop('client_secret')
init_u = urllib.parse.urlparse(init_url)
init_q = urllib.parse.urlencode(init_queries)

k.close()

_p = (init_u[0], init_u[1], init_u[2], '', init_q, '')
access_url = urllib.parse.urlunparse(_p)

print('server is ready')
print('now access to:')
print(access_url)
print('and authenticate this app.')


@app.route('/producteev_init/', methods=['GET'])
def token():
    """receive the 'code' and get json (initial token config)"""

    # parse out 'code' from GET request
    code = request.args.get('code')
    url = "https://www.producteev.com/oauth/v2/token"
    s = urllib.parse.urlparse(url)

    # generate a request for tokens
    with open('clientkeys.yml', 'r') as key:
        queries = yaml.load(key)
    print(queries)
    queries['grant_type'] = 'authorization_code'
    queries['code'] = code
    _q = urllib.parse.urlencode(queries)

    p = (s[0], s[1], s[2], '', _q, '')
    post_url = urllib.parse.urlunparse(p)

    print('accessing ' + post_url)
    res = requests.get(post_url)
    print(res.text)

    # save the tokens
    tokens = json.loads(res.text)
    print(tokens)
    with open('tokens.yml', 'w') as outfile:
        yaml.dump(tokens, outfile)

    return 'OK'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

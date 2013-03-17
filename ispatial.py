#!/usr/bin/env python
import httplib, urllib
from urlparse import urlparse
import sys
import json as simplejson


ispatial_url = 'https://ispatialv3-workshop.t-sciences.com/'

def main():
    # Calling iSpatial, Should tell you that you are not logged in
    r = http_req(ispatial_url + '/rpc/layer/query')
    print r.content

# --------- Helper functions ----------
def http_req(url, method='GET', params={}, headers={}):
    """ Basic HTTP request / response. Only url is required

        url - The url to request. Can include query params
        method - GET, POST, etc.
        params - Additional parameters passed as a dictionary
                 {'p1':'value1', 'p2':'value2'}.
                 These will be added to the GET query parameters
        headers - Additional headers to be send with the request

        Returns a Response object with fields:
            content, headers, status and reason
    
        Example:
        r = http_req('www.google.com/', params={'q': 'interesting_topic'})
        print r.content, r.headers, r.status, r.reason
    """
    if not url.startswith('http'): url = 'http://' + url
    u = urlparse(url)
    httpc = httplib.HTTPSConnection if u.scheme == 'https' \
                                    else httplib.HTTPConnection
    conn = httpc(u.netloc)
    params = urllib.urlencode(params)
    query = '?' + u.query
    if method == 'GET':
        query += ('&' if u.query else '')  + params
        params = None
    conn.request(method, u.path + query, params, headers)
    response = conn.getresponse()
    headers = {k:v for k,v in response.getheaders()}
    content = response.read()
    conn.close()
    return Response(content, response.status,
                    response.reason, headers)

class Response(object):
    def __init__(self, content, status, reason, headers):
        self.content = content
        self.status = status
        self.reason = reason
        self.headers = headers

if __name__ == '__main__':
    main()

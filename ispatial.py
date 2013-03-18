#!/usr/bin/env python
import httplib, urllib
from urlparse import urlparse
import sys
import json as simplejson

ispatial_url = 'https://ispatialv3-workshop.t-sciences.com'

# Please change the flickr_api_key
flickr_api_key = '5d49e2dc9774adf2f1065f48c5376b2c'

def main():
    flickr_params = {
        'tags': '',
        'per_page': 2  # Number of photos returned (leave at 2 for now)
    }
    flickr_search(flickr_params)
    

# --------- Helper functions ----------
def flickr_search(params):
    "Calls the Flickr Search REST endpoint"
    flickr_search_url = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&privacy_filter=1&safe_search=1&content_type=1&has_geo=1&sort=interestingness-desc&extras=geo%2C+tags&format=json&nojsoncallback=1&woe_id=23424977&accuracy=3'.format(flickr_api_key)
    # Hint: once you get the response, use simplejson to convert
    # its contents into a dictionary
    # e.g json = simplejson.loads(json_string) will return a dictionary with
    # keys and values that you can access with json['key1']['key11']


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

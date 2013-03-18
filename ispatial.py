#!/usr/bin/env python
import httplib, urllib
from urlparse import urlparse
import sys
import json as simplejson

# Please change the flickr_api_key
flickr_api_key = '5d49e2dc9774adf2f1065f48c5376b2c'

ispatial_url = 'https://ispatialv3-workshop.t-sciences.com'

def main():
    flickr_params = {
        #'tags': '',
        'per_page': 2  # Number of photos returned
    }
    photos = flickr_search(flickr_params)
    for photo in photos:
        photo_url = flickr_get_url(photo)
        photo['url'] = photo_url
        print 'Photo: ', photo

    default_layer_id = ispatial_get_home_layer_id()
    print '\n\ndefault_layer_id: ', default_layer_id
    
# --------- Helper functions ----------
def ispatial_add_point(params):
    "Adds a point and returns its id"
    rpcJson = {
        'title': params['title'],
        'description': params['tags'],
        'geometry': '{ "type": "Point", "coordinates": [ %s, %s ] }' % (
            params['longitude'], params['latitude']),
        'type_name': 'Object'
    }
    json = ispatial_call('/rpc/object/create', {'rpcJson': simplejson.dumps(rpcJson)})
    print 'Added point: ', json
    return json['data'][0]['id']

def ispatial_add_link(params):
    "Adds a link and returns its id"
    rpcJson = {
        'original_name': params['title'],
        'url': params['url']
    }
    json = ispatial_call('/rpc/file/create', {'rpcJson': simplejson.dumps(rpcJson)})
    return json['data'][0]['id']

def flickr_get_url(photo):
    "Converts a Search record into flickr URL"
    return 'http://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'.format(
        **photo)

def flickr_search(params):
    "Calls the Flickr Search REST endpoint"
    flickr_search_url = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&privacy_filter=1&safe_search=1&content_type=1&has_geo=1&sort=interestingness-desc&extras=geo%2C+tags&format=json&nojsoncallback=1&woe_id=23424977&accuracy=3'.format(flickr_api_key)
    r = http_req(flickr_search_url, params=params)
    json = simplejson.loads(r.content)
    if not r.status == 200 or (json and not json['stat']=='ok'):
        print "Flickr search failed. ", r.status, json
        sys.exit(-1)
    return json['photos']['photo']

def ispatial_get_home_layer_id():
    "Returns the current user's home layer id"
    return 'nothing yet'

def ispatial_call(endpoint, params={}):
    "Calls an iSpatial endpoint"
    headers = { 'Cookie': sessionid }
    url = ispatial_url + endpoint
    r = http_req(url, params=params, headers=headers)
    json = simplejson.loads(r.content)
    if not r.status == 200 or (json and not json['success']):
        print "Error when calling iSpatial: ", r.status, json
    return json

def ispatial_auth(ispatial_user, ispatial_user_pw):
    """ Connects to ispatial and sets a session token.
        The token will be used in all future requests
    """
    url = ispatial_url + '/rpc/user/login'
    params = {'username': ispatial_user, 'password': ispatial_user_pw}
    r = http_req(url, params=params)
    json = simplejson.loads(r.content)
    if not r.status == 200 or not json['success']:
        print "iSpatial was unable to authenticate user. ", r.status, json
        sys.exit(-1)
    global sessionid
    sessionid = r.headers['set-cookie'].split(';')[0]

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
    if len(sys.argv) == 3:
        ispatial_user = sys.argv[1]
        ispatial_auth(ispatial_user = ispatial_user,
                      ispatial_user_pw = sys.argv[2])
    main()



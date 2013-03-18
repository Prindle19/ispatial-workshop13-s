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

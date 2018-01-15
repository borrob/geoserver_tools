"""This file communicates with geoserver over the REST interface to deal with
the layers. It has functionality to create and delete layers. This
class uses the utility class Util (see util.py) to read the configuration and
the enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME layers

Example:
    >>> config = Util()
    >>> layers = get_layers(config)
    >>> print layers
    >>> print layer_exists(layername, config)
    >>> print get_layer_info(config)
"""
import json
import logging
from util import Util

def get_layers(u):
    """Get an overview of all layers.

    Uses the util class to get the specifices on the server etc.

    Returns python dict with name of the datastores as key and a dict as
    value. This dict contains the href to the layer..
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/layers.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('layers') == '':
        return None
    layers = json_data.get('layers').get('layer')

    out = {}
    for layer in layers:
        out[layer.get('name')] = {'href': layer.get('href')}
    return out

def layer_exists(layername, u):
    """Check if layer already exists in this geoserver
    configuration.

    Returns True of False.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/layers/' + \
                                  layername + '.json',
                           payload = None,
                           mime = 'application/json')
    return stat == 200

def get_layer_info(layername, u):
    """Get information on the layer

    Returns a dict with the layer info.
    """
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/layers/' + \
                                        layername + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Layer: "' + layername + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Layerdoes not exist!'}

    ds_info = json.loads(ds_request).get('layer')
    return ds_info

#TODO
#def create_layer(layername, u):

#TODO
#def delete_layer(layername, u):

#TODO
#def delete_all_layers(u):

def main():
    config = Util()
    layers = get_layers(config)
    print layers
    print layer_exists('tasmania_roads', config)
    print get_layer_info('tasmania_roads', config)

if __name__ == '__main__':
    main()

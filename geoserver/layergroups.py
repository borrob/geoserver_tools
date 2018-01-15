"""This file communicates with geoserver over the REST interface to deal with
the layergroups. It has functionality to create and delete layergroups. This
class uses the utility class Util (see util.py) to read the configuration and
the enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME featurestype

Example:
    >>> config = Util()
    >>> layergroups = get_layergroups(config)
    >>> print layergroups
    >>> print layergroup_exists(config)
    >>> print get_layergroup_info(config)
"""
import json
import logging
from util import Util

def get_layergroups(u):
    """Get an overview of all layergroups.

    Uses the util class to get the specifices on the server etc.

    Returns python dict with name of the datastores as key and a dict as
    value. This dict contains the href to the layergroup..
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/layergroups.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('layerGroups') == '':
        return None
    layergroups = json_data.get('layerGroups').get('layerGroup')

    out = {}
    for layergroup in layergroups:
        out[layergroup.get('name')] = {'href': layergroup.get('href')}
    return out

def layergroup_exists(layergroupname, u):
    """Check if layergroup already exists in this geoserver
    configuration.

    Returns True of False.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/layergroups/' + \
                                  layergroupname + '.json',
                           payload = None,
                           mime = 'application/json')
    return stat == 200

def get_layergroup_info(layergroupname, u):
    """Get information on the layergroup

    Returns a dict with the layergroup info.
    """
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/layergroups/' + \
                                        layergroupname + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Layergroup: "' + layergroupname + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Layergroup does not exist!'}

    ds_info = json.loads(ds_request).get('layerGroup')
    return ds_info

#TODO
#def create_layergroup(layergroupname, u):

#TODO
#def delete_layergroup(layergroupname, u):

#TODO
#def delete_all_layergroups(u):

def main():
    config = Util()
    layergroups = get_layergroups(config)
    print layergroups
    print layergroup_exists('tasmania', config)
    print get_layergroup_info('tasmania', config)

if __name__ == '__main__':
    main()

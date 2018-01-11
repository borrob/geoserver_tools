"""This file communicates with geoserver over the REST interface to deal with
the featuretypes. It has functionality to create and delete featuretypes. This
class uses the utility class Util (see util.py) to read the configuration and
the enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME featurestype

Example:
    >>> config = Util()
    >>> featuretypes = get_featuretypes('tiger', 'nyc', config)
    >>> print featuretypes
    >>> print featuretype_exists('tiger','nyc', 'giant_polygon', config)
    >>> print get_featuretype_info('tiger', 'nyc', 'giant_polygon', config)
"""
import json
import logging
import workspace
import datastore
from util import Util

def get_featuretypes(workspace, datastore, u):
    """Get an overview of all featurestype of this datastore in the workspace.

    Uses the util class to get the specifices on the server etc. Assumes the
    workspace exists.

    Returns python dict with name of the datastores as key and a dict as
    value. This dict contains the href to the datastore.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspace + \
                                  '/datastores/' + datastore + \
                                  '/featuretypes.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('featureTypes') == '':
        return None
    featuretypes = json_data.get('featureTypes').get('featureType')

    out = {}
    for featuretype in featuretypes:
        out[featuretype.get('name')] = {'href': featuretype.get('href')}
    return out

def featuretype_exists(workspacename, datastorename, featuretypename, u):
    """Check if featuretype in datastore  alreade exists in this geoserver
    configuration.

    Returns True of False.
    """
    if (not(datastore.datastore_exists(workspacename, datastorename, u))):
            logging.error('Featuretype cannot exist if datastore doesn\'t ' + \
                          'exist.')
            return False
    
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspacename + \
                                  '/datastores/' + datastorename + \
                                  '/featuretypes/' + featuretypename + '.json',
                           payload = None,
                           mime = 'application/json')
    return stat == 200

def get_featuretype_info(workspacename, datastorename, featuretypename, u):
    """Get information on the featuretype

    Returns a dict with the featuretype info.
    """
    if (not(datastore.datastore_exists(workspacename, datastorename, u))):
            logging.error('Datastore doesn\'t exist, so no info on ' + \
                          'featuretype available.')
            return {'info': 'No datastore, so no featuretype info.'}
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + workspacename + \
                                        '/datastores/' + datastorename + \
                                        '/featuretypes/' + featuretypename + \
                                        '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Featuretype: "' + featuretypename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Featuretype does not exist!'}

    ds_info = json.loads(ds_request).get('featureType')
    return ds_info

#TODO
#def create_datastore(workspace, datastorename, u):

#TODO
#def delete_datastore(workspace, datastorename, u):

#TODO
#def delete_all_datastores(workspace, u):

def main():
    config = Util()
    featuretypes = get_featuretypes('tiger', 'nyc', config)
    print featuretypes
    print featuretype_exists('tiger','nyc', 'giant_polygon', config)
    print get_featuretype_info('tiger', 'nyc', 'giant_polygon', config)

if __name__ == '__main__':
    main()

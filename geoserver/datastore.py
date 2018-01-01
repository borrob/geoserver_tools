"""This file communicates with geoserver over the REST interface to deal with
the datastores. It has functionality to create and delete datastores. This class
uses the utility class Util (see util.py) to read the configuration and the
enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME datastore

Example:
    >>> print 'calling datastore.main'
    >>> config = Util()
    >>> datastores = get_datastores('tiger', config)
    >>> print datastores
    >>> print datastore_exists('tiger','nyc', config)
    >>> print get_datastore_info('tiger', 'nyc', config)
"""
import json
import logging
import workspace
from util import Util

def get_datastores(workspace, u):
    """Get an overview of all datastores of this workspace.

    Uses the util class to get the specifices on the server etc. Assumes the
    workspace exists.

    Returns python dict with name of the datastores as key and a dict as
    value. This dict contains the href to the datastore.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspace + \
                                  '/datastores.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('dataStores') == '':
        return None
    datastores = json_data.get('dataStores').get('dataStore')

    out = {}
    for datastore in datastores:
        out[datastore.get('name')] = {'href': datastore.get('href')}
    return out

def datastore_exists(workspacename, datastorename, u):
    """Check if datastore alreade exists in this geoserver configuration.

    Returns True of False.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Datastore cannot exist if workspace doesn\'t exist.')
            return False
    
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspacename + \
                                  '/datastores/' + datastorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    return stat == 200

def get_datastore_info(workspacename, datastorename, u):
    """Get information on the datastore

    Returns a dict with the datastore info.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Workspace doesn\'t exist, so no info on ' + \
                          'datastore available.')
            return {'info': 'No workspace, so no datastore info.'}
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + workspacename + \
                                        '/datastores/' + \
                                        datastorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Datastore: "' + datastorename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Datastore does not exist!'}

    ds_info = json.loads(ds_request).get('dataStore')
    return ds_info

#TODO
#def create_datastore(workspace, datastorename, u):

#TODO
#def delete_datastore(workspace, datastorename, u):

#TODO
#def delete_all_datastores(workspace, u):

def main():
    print 'calling datastore.main'
    config = Util()
    datastores = get_datastores('tiger', config)
    print datastores
    print datastore_exists('tiger','nyc', config)
    print get_datastore_info('tiger', 'nyc', config)

if __name__ == '__main__':
    main()

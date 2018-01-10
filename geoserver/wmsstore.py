"""This file communicates with geoserver over the REST interface to deal with
the wmsstores. It has functionality to create and delete wmsstores. This class
uses the utility class Util (see util.py) to read the configuration and the
enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME wmsstore

Example:
    >>> print 'calling wmsstore.main'
    >>> config = Util()
    >>> wmsstores = get_wmsstores('tiger', config)
    >>> print wmsstores
    >>> print wmsstore_exists('tiger','nyc', config)
    >>> print get_wmsstore_info('tiger', 'nyc', config)
"""
import json
import logging
import workspace
from util import Util

def get_wmsstores(workspace, u):
    """Get an overview of all wmsstores of this workspace.

    Uses the util class to get the specifices on the server etc. Assumes the
    workspace exists.

    Returns python dict with name of the wmsstores as key and a dict as
    value. This dict contains the href to the wmsstore.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspace + \
                                  '/wmsstores.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('wmsStores') == '':
        return None
    wmsstores = json_data.get('wmsStores').get('wmsStore')

    out = {}
    for wmsstore in wmsstores:
        out[wmsstore.get('name')] = {'href': wmsstore.get('href')}
    return out

def wmsstore_exists(workspacename, wmsstorename, u):
    """Check if wmsstore alreade exists in this geoserver configuration.

    Returns True of False.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('WMSstore cannot exist if workspace doesn\'t exist.')
            return False
    
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspacename + \
                                  '/wmsstores/' + wmsstorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    return stat == 200

def get_wmsstore_info(workspacename, wmsstorename, u):
    """Get information on the wmsstore

    Returns a dict with the wmsstore info.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Workspace doesn\'t exist, so no info on ' + \
                          'wmsstore available.')
            return {'info': 'No workspace, so no wmsstore info.'}
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + workspacename + \
                                        '/wmsstores/' + \
                                        wmsstorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('WMSstore: "' + wmsstorename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'WMSstore does not exist!'}

    ds_info = json.loads(ds_request).get('wmsStore')
    return ds_info

#TODO
#def create_wmsstore(workspace, wmsstorename, u):

#TODO
#def delete_wmsstore(workspace, wmsstorename, u):

#TODO
#def delete_all_wmsstores(workspace, u):

def main():
    print 'calling wmsstore.main'
    config = Util()
    wmsstores = get_wmsstores('tiger', config)
    print wmsstores
    print wmsstore_exists('tiger','nyc', config)
    print get_wmsstore_info('tiger', 'nyc', config)

if __name__ == '__main__':
    main()

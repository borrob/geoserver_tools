"""This file communicates with geoserver over the REST interface to deal with
the wmtsstores. It has functionality to create and delete wmtsstores. This class
uses the utility class Util (see util.py) to read the configuration and the
enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME wmtsstore

Example:
    >>> print 'calling wmtsstore.main'
    >>> config = Util()
    >>> wmtsstores = get_wmtsstores('tiger', config)
    >>> print wmtsstores
    >>> print wmtsstore_exists('tiger','nyc', config)
    >>> print get_wmtsstore_info('tiger', 'nyc', config)
"""
import json
import logging
import workspace
from util import Util

def get_wmtsstores(workspace, u):
    """Get an overview of all wmtsstores of this workspace.

    Uses the util class to get the specifices on the server etc. Assumes the
    workspace exists.

    Returns python dict with name of the wmtsstores as key and a dict as
    value. This dict contains the href to the wmtsstore.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspace + \
                                  '/wmtsstores.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('wmtsStores') == '':
        return None
    wmtsstores = json_data.get('wmtsStores').get('wmtsStore')

    out = {}
    for wmtsstore in wmtsstores:
        out[wmtsstore.get('name')] = {'href': wmtsstore.get('href')}
    return out

def wmtsstore_exists(workspacename, wmtsstorename, u):
    """Check if wmtsstore alreade exists in this geoserver configuration.

    Returns True of False.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('WMTSstore cannot exist if workspace doesn\'t exist.')
            return False
    
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspacename + \
                                  '/wmtsstores/' + wmtsstorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    return stat == 200

def get_wmtsstore_info(workspacename, wmtsstorename, u):
    """Get information on the wmtsstore

    Returns a dict with the wmtsstore info.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Workspace doesn\'t exist, so no info on ' + \
                          'wmtsstore available.')
            return {'info': 'No workspace, so no wmtsstore info.'}
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + workspacename + \
                                        '/wmtsstores/' + \
                                        wmtsstorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('WMTSstore: "' + wmtsstorename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'WMTSstore does not exist!'}

    ds_info = json.loads(ds_request).get('wmtsStore')
    return ds_info

#TODO
#def create_wmtsstore(workspace, wmtsstorename, u):

#TODO
#def delete_wmtsstore(workspace, wmtsstorename, u):

#TODO
#def delete_all_wmtsstores(workspace, u):

def main():
    print 'calling wmtsstore.main'
    config = Util()
    wmtsstores = get_wmtsstores('tiger', config)
    print wmtsstores
    print wmtsstore_exists('tiger','nyc', config)
    print get_wmtsstore_info('tiger', 'nyc', config)

if __name__ == '__main__':
    main()

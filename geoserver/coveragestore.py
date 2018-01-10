"""This file communicates with geoserver over the REST interface to deal with
the coveragestores. It has functionality to create and delete coveragestores. This class
uses the utility class Util (see util.py) to read the configuration and the
enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME coveragestore

Example:
    >>> print 'calling coveragestore.main'
    >>> config = Util()
    >>> coveragestores = get_coveragestores('tiger', config)
    >>> print coveragestores
    >>> print coveragestore_exists('tiger','nyc', config)
    >>> print get_coveragestore_info('tiger', 'nyc', config)
"""
import json
import logging
import workspace
from util import Util

def get_coveragestores(workspace, u):
    """Get an overview of all coveragestores of this workspace.

    Uses the util class to get the specifices on the server etc.

    Returns python dict with name of the coveragestores as key and a dict as
    value. This dict contains the href to the coveragestore.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspace + \
                                  '/coveragestores.json',
                           payload = None,
                           mime = 'application/json')
    json_coverage = json.loads(ds_request)
    if json_coverage.get('coverageStores') == '':
        return None
    coveragestores = json_coverage.get('coverageStores').get('coverageStore')

    out = {}
    for coveragestore in coveragestores:
        out[coveragestore.get('name')] = {'href': coveragestore.get('href')}
    return out

def coveragestore_exists(workspacename, coveragestorename, u):
    """Check if coveragestore alreade exists in this geoserver configuration.

    Returns True of False.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Coveragestore cannot exist if workspace doesn\'t exist.')
            return False
    
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/workspaces/' + workspacename + \
                                  '/coveragestores/' + coveragestorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    return stat == 200

def get_coveragestore_info(workspacename, coveragestorename, u):
    """Get information on the coveragestore

    Returns a dict with the coveragestore info.
    """
    if (not(workspace.workspace_exists(workspacename, u))):
            logging.error('Workspace doesn\'t exist, so no info on ' + \
                          'coveragestore available.')
            return {'info': 'No workspace, so no coveragestore info.'}
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + workspacename + \
                                        '/coveragestores/' + \
                                        coveragestorename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Coveragestore: "' + coveragestorename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Coveragestore does not exist!'}

    ds_info = json.loads(ds_request).get('coverageStore')
    return ds_info

#TODO
#def create_coveragestore(workspace, coveragestorename, u):

#TODO
#def delete_coveragestore(workspace, coveragestorename, u):

#TODO
#def delete_all_coveragestores(workspace, u):

def main():
    print 'calling coveragestore.main'
    config = Util()
    coveragestores = get_coveragestores('tiger', config)
    print coveragestores
    print coveragestore_exists('tiger','nyc', config)
    print get_coveragestore_info('tiger', 'nyc', config)

if __name__ == '__main__':
    main()

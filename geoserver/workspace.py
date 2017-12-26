"""This file communicates with geoserver over the REST interface to deal with
the workspaces. It has functionality to create and delete workspaces. This class
uses the utility class Util (see util.py) to read the configuration and the
enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME workspace

Example:
    >>> config = Util()
    >>> ws = Workspace()
    >>> workspaces = ws.get_workspaces(config)
    >>> print 'Does workspace "blabla" exist?'
    >>> print ws.workspace_exists('blabla', config)
    >>> wsi = ws.get_workspace_info('cite', config)
    >>> workspaces['cite']['info'] = wsi
    >>> print workspaces['cite']
"""
import json
import logging

from util import Util

def get_workspaces(u):
    """Get an overview of all workspaces.

    Uses the util class to get the specifices on the server etc.

    Returns python dict with name of the workspaces as key and a dict as
    value. This dict contains the href to the workspace.
    """
    stat, ws_request = u.request(method = 'GET',
                           path = 'rest/workspaces.json',
                           payload = None,
                           mime = 'application/json')
    ws = json.loads(ws_request).get('workspaces').get('workspace')

    out = {}
    for w in ws:
        out[w.get('name')] = {'href': w.get('href')}
    return out

def workspace_exists(workspacename, u):
    """Check if workspace alreade exists in this geoserver configuration.

    Returns True of False.
    """
    stat, ws_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + \
                                            workspacename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    return stat == 200

def get_workspace_info(workspacename, u):
    """Get information on the workspaces

    Returns a dict with the workspace info.
    """
    stat, ws_request = u.request(method = 'GET',
                                 path = 'rest/workspaces/' + \
                                        workspacename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Workspace: "' + workspacename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Workspace does not exist!'}

    ws_info = json.loads(ws_request).get('workspace')
    return ws_info

def create_workspace(workspacename, u):
    """Create a new workspace

    Does not check if the workspace already exists.

    Returns True or False if succesful.
    """
    logging.info('Creating workspace "' + workspacename +'"')
    payload = '<workspace>'
    payload += '<name>'
    payload += workspacename
    payload +='</name>'
    payload +='</workspace>'

    stat, ws_request = u.request(method = 'POST',
                                 path = 'rest/workspaces',
                                 payload = payload,
                                 mime = 'text/xml')

    return stat == 201

def make_workspace_default(workspacename, u):
    """Make the workspace the default option.

    Return True or False if succesful.
    """
    if(not(workspace_exists(workspacename))):
        logging.error('Could not make workspace "' + workspacename + \
            '" the default workspace, since it doesn\'t exists.')
        return False

    payload = '<workspace>'
    payload += '<name>'
    payload += workspacename
    payload +='</name>'
    payload +='</workspace>'

    stat, ws_request = u.request(method = 'PUT',
                                 path = 'rest/workspaces/default',
                                 payload = payload,
                                 mime = 'text/xml')

    return stat == 200

def delete_workspace(workspacename, u):
    """Delete the workspace from the geoserver.

    Does not checkt if the workspace exists.

    Returns True or False if succesful.
    """
    logging.info('Deleting workspace "' + workspacename + '"')
    stat, ws_request = u.request(method = 'DELETE',
                                 path = 'rest/workspaces/' + workspacename,
                                 payload = None,
                                 mime = 'text/xml')

    return stat == 200

def delete_all_workspaces(u):
    """Delete all the workspaces from the geosever.
    """
    logging.info('Deleting ALL workspaces.')
    workspaces = get_workspaces(u)
    for ws in workspaces:
        delete_workspace(ws, u)

def main():
    print 'calling workspace.main'
    config = Util()
    workspaces = get_workspaces(config)
    print 'Does workspace "blabla" exist?'
    print workspace_exists('blabla', config)
    wsi = get_workspace_info('cite', config)
    workspaces['cite']['info'] = wsi
    print workspaces['cite']
    print '----'
    print workspaces

if __name__ == '__main__':
    main()

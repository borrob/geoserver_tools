"""This file communicates with geoserver over the REST interface to deal with
the styles. It has functionality to create and delete styles. This
class uses the utility class Util (see util.py) to read the configuration and
the enable general functionality. Make sure there is a valid configuration file.

TODO: add function to RENAME styles

Example:
    >>> config = Util()
    >>> styles = get_styles(config)
    >>> print styles
    >>> print style_exists(stylename, config)
    >>> print get_style_info(config)
"""
import json
import logging
from util import Util

def get_styles(u):
    """Get an overview of all styles.

    Uses the util class to get the specifices on the server etc.

    Returns python dict with name of the datastores as key and a dict as
    value. This dict contains the href to the style..
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/styles.json',
                           payload = None,
                           mime = 'application/json')
    json_data = json.loads(ds_request)
    if json_data.get('styles') == '':
        return None
    styles = json_data.get('styles').get('style')

    out = {}
    for style in styles:
        out[style.get('name')] = {'href': style.get('href')}
    return out

def style_exists(stylename, u):
    """Check if style already exists in this geoserver
    configuration.

    Returns True of False.
    """
    stat, ds_request = u.request(method = 'GET',
                           path = 'rest/styles/' + \
                                  stylename + '.json',
                           payload = None,
                           mime = 'application/json')
    return stat == 200

def get_style_info(stylename, u):
    """Get information on the style

    Returns a dict with the style info.
    """
    stat, ds_request = u.request(method = 'GET',
                                 path = 'rest/styles/' + \
                                        stylename + '.json',
                                 payload = None,
                                 mime = 'application/json')
    if stat != 200:
        logging.error('Style: "' + stylename + '" does not' + \
                      ' exist! Cannot get information.')
        return {'info': 'Style does not exist!'}

    ds_info = json.loads(ds_request).get('style')
    return ds_info

#TODO
#def create_style(stylename, u):

#TODO
#def delete_style(stylename, u):

#TODO
#def delete_all_styles(u):

def get_sld(stylename, u):
    if not(style_exists(stylename, u)):
        logging.error('Style does not exist, cannot get SLD!')
        return

    stat, req = u.request(method = 'GET', path = 'rest/styles/' + stylename + '.sld')
    if stat != 200:
        logging.error('Something went wrong getting the SLD:' + stylename)
        return
    return req

#TODO
#def upload_sld():

#TODO
#def set_style_as_default(stylenam, u):

def main():
    config = Util()
    styles = get_styles(config)
    print styles
    print style_exists('capitals', config)
    print get_style_info('line', config)
    print get_sld('line', config)

if __name__ == '__main__':
    main()

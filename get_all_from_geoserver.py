"""Get all the data from a single geoserver.

Put all the data into a python dict and dump it to json.

TODO: layersgroups and the 'other' stores
"""

import json
from geoserver import util
from geoserver import workspace
from geoserver import datastore
from geoserver import featuretype
from geoserver import layers
from geoserver import styles

config = util.Util(config_file='settings.cfg')
gs = {}

### WORKSPACES, DATASTORES, AND FEATUERS ###
workspaces = workspace.get_workspaces(config)
default_workspace = workspace.get_name_of_default_workspace(config)
gs['workspaces'] = {}

for w in workspaces:
    gs['workspaces'][w] = {}
    gs['workspaces'][w]['name'] = w
    gs['workspaces'][w]['default'] = w == default_workspace

    dat_store = datastore.get_datastores(w, config)
    if dat_store:
        gs['workspaces'][w]['datastores'] = {}
        for d in dat_store:
            gs['workspaces'][w]['datastores'][d] = \
                datastore.get_datastore_info(w, d, config)

            features = featuretype.get_featuretypes(w, d, config)
            if features:
                gs['workspaces'][w]['datastores'][d]['featuretypes'] = {}
                for f in features:
                    gs['workspaces'][w]['datastores'][d]['featuretypes'][f] = \
                        featuretype.get_featuretype_info(w, d, f, config)

### LAYERS ###
gs_layers = layers.get_layers(config)
gs['layers'] = {}

if gs_layers:
    for l in gs_layers:
        gs['layers'][l] = {}
        gs['layers'][l] = layers.get_layer_info(l, config)

### STYLES ###
gs_styles = styles.get_styles(config)
gs['styles'] = {}

if gs_styles:
    for s in gs_styles:
        gs['styles'][s] = {}
        gs['styles'][s] = styles.get_style_info(s, config)

        # write SLD to file
        with open(gs['styles'][s]['filename'], 'w') as f:
            f.write(styles.get_sld(s, config))

with open('geoserver_config.json', 'w') as f:
    f.write(json.dumps(gs))

with open('geoserver_config_prettyprint.json', 'w') as f:
    f.write(json.dumps(gs, indent=4, sort_keys=True))

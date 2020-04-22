#!/usr/bin/env python3

import json
import numpy
from flask import abort
from flask import request
from flask import render_template
from flask import Response

from libs import pyhis
from contexts import elf
from . import routes


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError


@routes.route('/<string:network>')
def provider(network):

    services = pyhis.Services()
    providers = services.get_data_providers()

    # check that the network exists
    known_networks = providers.NetworkName.values
    known_networks = [net.upper() for net in known_networks]

    try:
        idx = known_networks.index(network.upper())
    except Exception:
        abort(404)

    # get info for the provider via wof
    provider = providers.iloc[idx]

    # convert pandas df to dict.
    # this is necessary because the to_dict function returns 64bit numpy
    # data types which are not json serializable :(
    pdata = {}
    for k, v in provider.to_dict().items():
        if type(v) == numpy.int64:
            v = int(v)
        pdata[k] = v

#    import pdb; pdb.set_trace()
#    # get sites for this service
#    sites = services.get_sites(xmin=pdata['minx'],
#                               ymin=pdata['miny'],
#                               xmax=pdata['minx'] + 10,
#                               ymax=pdata['miny'] + 10,
# THIS DOESNT SEEM CORRECT      networkIDs=str(pdata['ServiceID']),
#                               degStep=3)

    pdata['title'] = f"{pdata['NetworkName']} " \
                     f"- {pdata['organization']}"

    # write json-ld
    json_ld = {
                "@context": [],
                "@id": f"http://localhost:5000/{network}",
                "@type": []
              }
    elf = {
            '@context': 'https://opengeospatial.github.io/ELFIE/json-ld/' +
                        'elf.jsonld',
            'name': f"{pdata['organization']} " +
                    f"({pdata['NetworkName']})",
            'description': f'HIS Data Provider - {pdata["NetworkName"]}',
            'geo': {'@type': 'schema:GeoShape',
                    'box': f'{pdata["miny"]},{pdata["minx"]} ' +
                           f'{pdata["maxy"]},{pdata["maxx"]}'},
            'gsp:hasGeometry': {'@type': 'gsp:Geometry',
                                'gsp:asWKT': 'POLYGON (' +
                                f'({pdata["miny"]},{pdata["minx"]}) ' +
                                f'({pdata["maxy"]},{pdata["minx"]}) ' +
                                f'({pdata["maxy"]},{pdata["maxx"]}) ' +
                                f'({pdata["miny"]},{pdata["maxx"]}) ' +
                                f'({pdata["miny"]},{pdata["minx"]}))'},
          }

#    elf_geo = {
#              "@type": "schema.GeoCoordinates",
#              "schema.latitude": dat['meta']['lat'],
#              "schema.longitude": dat['meta']['lon']
#              }
#    elf_hasGeometry = {
#                      "@type": "gsp:Geometry",
#                      "gsp:asWKT": f"POINT ({dat['meta']['lon']}, " +
#                                   f"{dat['meta']['lat']})"
#                     }

    json_ld.update(elf)

#    # define the hy_features
#    json_ld['@context'].append('https://opengeospatial.github.io/ELFIE/json-ld/hyf.jsonld')
#    json_ld['HY_HydroLocationType'] = 'hydrometricStation'
#    json_ld['@type'].append('http://www.opengeospatial.org/standards/waterml2/hy_features/HY_HydroLocation')

    pdata['jsonld'] = json.dumps(json_ld, sort_keys=True,
                                 indent=4, separators=(',', ': '))

    # return either the page or ld+json
    arg = request.args.get('jsonld')
    if arg is None:
        return render_template("provider.html", data=pdata)
    else:
        return Response(response=pdata['jsonld'],
                        mimetype="application/json")


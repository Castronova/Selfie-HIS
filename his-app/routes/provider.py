#!/usr/bin/env python3

import json
import ulmo
import numpy
from flask import abort
from flask import request
from flask import render_template
from flask import Response

from libs import pyhis
from libs import hyfeatures
from contexts import elf
from . import routes


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError

def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
 
   return dict3

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
    # get sites for this service
    sites = ulmo.cuahsi.wof.get_sites(pdata['servURL'])

    pdata['title'] = f"{pdata['NetworkName']} " \
                     f"- {pdata['organization']}"

    # write json-ld
    json_ld = {
                "@context": [],
                "@id": f"http://localhost:5000/{network}",
                "@type": []
              }
    elf = {
            '@context': ['https://opengeospatial.github.io/ELFIE/json-ld/elf.jsonld'],
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
    # build hydrometricNetwork
    # todo: loop
    hyf = hyfeatures.HydrometricNetwork()
                                        
    for k, v in sites.items():
        """
        {'code': 'AMES',
 'location': {'latitude': '42.066667', 'longitude': '-71.1'},
 'name': '117 CANTON STREET, EASTON, AMES POND',
 'network': 'TRWA',
 'site_property': {'state': 'MA'}}
        """

        # todo set description
        lat = v['location']['latitude']
        lon = v['location']['longitude']
        hyf.add_feature(v['name'],
                        f'{request.url}/{v["code"]}',
                        geo={"@type": "schema:GeoShape",
                             "point": f"{lat} {lon}"},
                        gsp={"@type": "gsp:Geometry",
                             "gsp:asWKT": f"POINT ( {lat} {lon} )"})

    json_ld.update(elf)
    json_ld['@context'].extend(hyf.get_context())
    json_ld.update(hyf.as_dict())

    pdata['jsonld'] = json.dumps(json_ld, sort_keys=False,
                                 indent=4, separators=(',', ': '))

    # return either the page or ld+json
    arg = request.args.get('jsonld')
    if arg is None:
        return render_template("provider.html", data=pdata)
    else:
        return Response(response=pdata['jsonld'],
                        mimetype="application/json")


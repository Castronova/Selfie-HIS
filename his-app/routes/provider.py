#!/usr/bin/env python3

import json
import ulmo
import numpy
import urllib
from flask import abort
from flask import request
from flask import render_template
from flask import Response

from libs import pyhis
from libs import hyfeatures
from libs import provider
from libs import site

from contexts import elf
from . import routes


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError



def build_jsonld(pdata, sites):

    pdata['title'] = f"{pdata['NetworkName']} " \
                     f"- {pdata['organization']}"

    # write json-ld
    # TODO: make sure that @id works when networkname contains spaces
    encoded_network = urllib.parse.quote(pdata['NetworkName'])
    json_ld = {
                "@context": [],
                "@id": f"{request.url_root}{encoded_network}",
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

        # todo set description
        lat = v['location']['latitude']
        lon = v['location']['longitude']

        # isolate the url without the query parameters
        req_url = request.url.split('?')[0]

        hyf.add_feature(v['name'],
                        f'{req_url}/{v["code"]}',
                        geo={"@type": "schema:GeoShape",
                             "point": f"{lat} {lon}"},
                        gsp={"@type": "gsp:Geometry",
                             "gsp:asWKT": f"POINT ( {lat} {lon} )"})

    json_ld.update(elf)
    json_ld['@context'].extend(hyf.get_context())
    json_ld.update(hyf.as_dict(geoms=False))

    pdata['jsonld'] = json.dumps(json_ld, sort_keys=False,
                                 indent=4, separators=(',', ': '))

    # return ld+json
    return pdata['jsonld']


def build_geojson(sites):
    req_url = request.url.split('?')[0]
    features = []
    for k, v in sites.items():
        feature = {'type': 'Feature'}
        feature['geometry'] = {'type': 'Point',
                               'coordinates': [
                                   float(v['location']['longitude']),
                                   float(v['location']['latitude'])
                                   ]
                               }
        feature['properties'] = {'SiteName': v['name'],
                                 'SiteCode': v['code'],
                                 'Network': v['network'],
                                 'PID': f'<a href={req_url}/{v["code"]}>link</a>',
                                 }
        features.append(feature)


    geo = {'type': 'FeatureCollection',
           'features': features}
    return json.dumps(geo, indent=4)

@routes.route('/<string:network>')
def provider_index(network):

    pdata = provider.get_provider(network)
    sites = site.get_sites(pdata)
    jsonld = build_jsonld(pdata, sites)

    # return either the page or ld+json
    arg = request.args.get('f')
    if arg == 'jsonld':
        # return ld+json
        return Response(response=jsonld,
                        mimetype="application/json")
    elif arg == 'geojson':
        geojson = build_geojson(sites)
        return Response(response=geojson,
                        mimetype="application/json")
    else:
        return render_template("provider.html", data=pdata)

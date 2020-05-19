#!/usr/bin/env python3

import json
import numpy
import urllib
from flask import abort
from flask import render_template
from flask import request, Response

from libs import pyhis
from libs import provider as wof_provider
from libs import site as wof_site

from contexts import elf
from . import routes


class Site(elf.ElfContext):
    def __init__(self, site, provider):

        super(Site, self).__init__()

        self.name = f'{site["name"].strip()} - ' + \
                    f'{provider["NetworkName"]}'

        # todo: site network is sometimes different than provider network.
        #       I don't this this is right. I'm using provider network here.
        self.description = f'{site["name"]} - ' + \
                           f'{provider["NetworkName"]} - ' + \
                           f'{site["code"]}'
        lon = float(site['location']['longitude'])
        lat = float(site['location']['latitude'])

        self.geometry_from_wkt(f"POINT ({lon} {lat})")


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError


def build_geojson(provider, site):

    geo = {'type': 'Feature',
           'geometry': {
               'type': 'Point',
               'coordinates': [float(site['location']['longitude']),
                               float(site['location']['latitude'])]
               }, 'properties': {
                   'SiteName': site['name'],
                   'SiteCode': site['code'],
                   'Network': provider['NetworkName']
                   }
           }
    return json.dumps(geo, indent=4)


@routes.route('/<string:network>/<string:siteid>')
def site_index(network, siteid):

    provider = wof_provider.get_provider(network)
    site = wof_site.get_site(provider, network, siteid)
#    jsonld = build_jsonld(pdata, sites)


    site_context = Site(site, provider)

    # loop through the observation series for this site
    series = []
    for k, v in site['series'].items():
        series.append(site['series'][k]['variable'])


    # add global metadata
    dat = {}
    dat['series'] = series
    lon = float(site['location']['longitude'])
    lat = float(site['location']['latitude'])
    purl = f'{request.url_root}{urllib.parse.quote(provider["NetworkName"])}'
    dat['meta'] = {'siteid': site['code'],
                   'sitename': site['name'].strip(),
                   'lat': lat,
                   'lon': lon,
                   'provider': provider['NetworkName'],
                   'provider_url': purl,
                   }

    dat['title'] = f"{provider['NetworkName']} {site['name'].strip()}" \
                   f" - {site['code']}"

    json_ld = {
                "@context": site_context.context_url,
                "@id": f"http://localhost:5000/{network}/{siteid}",
                "@type": []
              }

    json_ld.update(site_context.context)

    # define the hy_features
    json_ld['@context'].append('https://opengeospatial.github.io/ELFIE/json-ld/hyf.jsonld')
    json_ld['HY_HydroLocationType'] = 'hydrometricStation'
    json_ld['@type'].append('http://www.opengeospatial.org/standards/waterml2/hy_features/HY_HydroLocation')
    dat['jsonld'] = json.dumps(json_ld, sort_keys=True,
                               indent=4, separators=(',', ': '))

    arg = request.args.get('f')
    if arg is None or arg == 'html':
        return render_template('site.html', data=dat)
    elif arg == 'jsonld':
        return Response(dat['jsonld'],
                        mimetype='application/json')
    elif arg == 'geojson':
        geojson = build_geojson(provider, site)
        return Response(geojson,
                        mimetype='application/json')





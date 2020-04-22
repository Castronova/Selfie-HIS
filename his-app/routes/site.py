#!/usr/bin/env python3

import json
import numpy
from flask import abort
from flask import render_template
from flask import request, Response

from libs import pyhis
from contexts import elf
from . import routes


class Site(elf.ElfContext):
    def __init__(self, wof_site_info_object, wof_data_provider_object):

        super(Site, self).__init__()

        s = wof_site_info_object.iloc[0].to_dict()
        p = wof_data_provider_object.iloc[0].to_dict()

        self.name = f'{s["sitename"].strip()} - ' + \
                    f'{p["NetworkName"]}'
        self.description = f'{s["sitename"]} - ' + \
                           f'{p["NetworkName"]} - ' + \
                           f'{s["siteid"]}'

        self.geometry_from_wkt(f"POINT ({s['lon']} {s['lat']})")


def convert(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError


@routes.route('/<string:network>/<string:siteid>')
def site(network, siteid):

    services = pyhis.Services()
    providers = services.get_data_providers()

    # check that the network exists
    known_networks = providers.NetworkName.values
    known_networks = [net.upper() for net in known_networks]

    try:
        idx = known_networks.index(network.upper())
    except Exception:
        abort(404)

    # get info for the provider via WOF
    provider = providers.iloc[idx].to_dict()

    # get WDSL
    wsdl = provider['servURL']

    # for some reason the uppercase WSDL doesn't work
    wsdl = wsdl.replace('WSDL', 'wsdl')

    try:
        # get site info
        sites = services.get_sites_info([wsdl], [f'{network}:{siteid}'])
    except Exception:
        abort(404)

    site_context = Site(sites, providers)

    data = []
    for i in range(0, len(sites)):
        data.append(sites.iloc[i].to_dict())

    # add global metadata
    dat = {}
    dat['series'] = data
    dat['meta'] = {'siteid': data[0]['siteid'],
                   'sitename': data[0]['sitename'].strip(),
                   'lat': data[0]['lat'],
                   'lon': data[0]['lon'],
                   'provider': provider['NetworkName'],
                   }

    dat['title'] = f"{provider['NetworkName']} {data[0]['sitename'].strip()}" \
                   f" - {data[0]['siteid']}"

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

    arg = request.args.get('jsonld')
    if arg is None:
        return render_template("site.html", data=dat)
    else:
        return Response(dat['jsonld'],
                        mimetype='application/json')




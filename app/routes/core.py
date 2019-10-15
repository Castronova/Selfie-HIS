#!/usr/bin/env python3

import json
from flask import jsonify, render_template, request

from libs import pyhis
from contexts import elf
from . import routes


@routes.route('/')
@routes.route('/index')
def index():
    dat = [
            {'name': 'CocoRaHs Service Provider',
             'url': f'{request.url}CocoRaHs'},
            {'name': 'CocoRaHs Site',
             'url': f'{request.url}CocoRaHs/us1masf0004'},
            {'name': 'NWISGW Service Provider',
             'url': f'{request.url}NWISGW'},
            {'name': 'NWISGW Site',
             'url': f'{request.url}NWISGW/422324071070701'},
            ]
    return render_template("index.html", data=dat)


# CocoRaHs:US1MAMD0054

@routes.route('/test/<string:network>/<string:siteid>')
def test(network, siteid):

    services = pyhis.Services()
    providers = services.get_data_providers()

    # check that the network exists
    known_networks = providers.NetworkName.values
    known_networks = [net.upper() for net in known_networks]
    idx = known_networks.index(network.upper()) or None

    if idx is None:
        return f"""
                Error: network '{network}' could not be found
                in the HIS
                """

    provider = providers.iloc[idx]
    networkname = provider.NetworkName
    sitecode = f'{networkname}:{siteid}'
    wsdl = provider.servURL

    # this fails if wsdl is uppercase, but I don't know why
    wsdl = wsdl.replace('WSDL', 'wsdl')

    try:
        info = services.get_sites_info([wsdl], [sitecode], verbose=True)
    except Exception as e:
        msg = f"""
        Error querying site metadata. Please verify that the
        network name and site id are correct. Networkname= {networkname}, siteid={siteid}.
        """
        return msg


    # todo make sure the wof response contains data
    dat = info.iloc[0]

    ec = elf.ElfContext()
    ec.name = f'{dat.sitename.strip()} - {network}'
    ec.description = f'{dat.sampleMedium} - {dat.valuetype}'
    ec.geo = {
              "@type": "schema.GeoCoordinates",
              "schema.latitude": dat.lat,
              "schema.longitude": dat.lon
              }
    ec.hasGeometry = {
                      "@type": "gsp:Geometry",
                      "gsp:asWKT": f"POINT ({dat.lon}, {dat.lat})"
                     }

    json_ld = {
                "@context": [ec.context_url],
                "@id": f"{provider.ServiceDescriptionURL}/{sitecode}",
                "@type": 'NOT SURE WHAT TO PUT HERE'
              }
    json_ld.update(ec.context)

    return jsonify(json_ld)

#!/usr/bin/env python3

import sys
import csv
import pyhis
import argparse

# NOTE THIS REQUIRES SUDS-JURKO, suds-py3 will not work!


def get_provider(providers, provider_id):

    # check that the network exists
    known_networks = providers.NetworkName.values
    known_networks = [net.upper() for net in known_networks]

    try:
        pidx = known_networks.index(provider_id.upper())
        # get info for the provider via wof
        provider = providers.iloc[pidx]
    except Exception:
        return None
    return provider


if __name__ == '__main__':
    desc = 'Utility for generating geoconnex namespace csv'
    p = argparse.ArgumentParser(description=desc)
    p.add_argument('-p',
                   required=True,
                   help='HIS provider ID')
    p.add_argument('-bbox',
                   nargs='+',
                   type=str,
                   default=['-109.1', '31.3', '-102.8', '37.1'], 
                   help='bounding box: llon llat ulon ulat')
    p.add_argument('-keyword',
                   default='',
                   help='keyword to search for')

    args = p.parse_args()

    services = pyhis.Services()
    print('collecting data providers', flush=True)
    providers = services.get_data_providers()
    print(f'collecting providers that matches {args.p}', flush=True)
    provider = get_provider(providers, args.p)
    if provider is None:
        print('invalid provider id')
        sys.exit(0)

    # get WDSL
    wsdl = provider['servURL']

    # for some reason the uppercase WSDL doesn't work
    wsdl = wsdl.replace('WSDL', 'wsdl')
    network_name = provider['NetworkName']
    network_id = str(provider['ServiceID'])

    print('getting sites', flush=True)
    kwargs = {'conceptKeyword': args.keyword,
              }
    sites = services.get_sites(float(args.bbox[0]),
                               float(args.bbox[1]),
                               float(args.bbox[2]),
                               float(args.bbox[3]),
                               pattern=network_name,
                               **kwargs)
    import pdb; pdb.set_trace()

    # TODO: Write geojson

#    try:
#        # get site info
#        sites = services.get_sites_info([wsdl], [f'{network}:{siteid}'])
#    except Exception:
#        print('error collecting sites')
#        sys.exit(1)
#
#    # convert pandas df to dict.
#    # this is necessary because the to_dict function returns 64bit numpy
#    # data types which are not json serializable :(
#    pdata = {}
#    for k, v in provider.to_dict().items():
#        if type(v) == numpy.int64:
#            v = int(v)
#        pdata[k] = v
#
##    import pdb; pdb.set_trace()
#    # get sites for this service
#    sites = services.get_sites(xmin=pdata['minx'],
#                               ymin=pdata['miny'],
#                               xmax=pdata['minx'] + 10,
#                               ymax=pdata['miny'] + 10,
# THIS DOESNT SEEM CORRECT      networkIDs=str(pdata['ServiceID']),
#                               degStep=3)
#
#    pdata['title'] = f"{pdata['NetworkName']} " \
#                     f"- {pdata['organization']}"
#

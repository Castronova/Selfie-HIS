#!/usr/bin/env python3

import os
import sys
import ulmo
import pyhis
import urllib
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
                   help='HIS provider ID. Use "All" to run for every provider')
    p.add_argument('--creator',
                   default='acastronova@cuahsi.org',
                   help='PID creator email')
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
    print(f'finding match for: "{args.p}"', flush=True)

    provider_ids = []
    if args.p.lower() == 'all':
        provider_ids = providers.NetworkName.values
    else:
        provider_ids = [args.p]

    i = 0
    failed = {}
    skipped = {}
    for pid in provider_ids:
        i += 1
        print(f'Processing {pid}: [{i} of {len(provider_ids)}]')
        provider = get_provider(providers, pid)
        fname = f'CUAHSI_HIS_{pid.replace(" ", "_")}_ids.csv'

        # skip if file already exists
        if os.path.exists(fname):
            msg = 'file already exists'
            print(f'  - skipping, {msg}')
            skipped[pid] = msg
            continue

        # skip if provider was not found
        if provider is None:
            msg = f'could not find match for: provider="{pid}"'
            print(f'  - skipping, {msg}')
            skipped[pid] = msg
            continue

        # get WDSL
        wsdl = provider['servURL']

        try:
            # get provider sites
            print('  + collecting sites', flush=True)
            sites = ulmo.cuahsi.wof.get_sites(wsdl)

            # append to existing namespace if one already exists
            print('  + writing geoconnex csv')
            header = 'id,target,creator,description,lat,lon,' + \
                     'c1_type,c1_match,c1_value\n'
            with open(fname, 'w') as f:
                f.write(header)
                for siteid, meta in sites.items():
                    code = meta['code']
                    net = urllib.parse.quote(provider.NetworkName)
                    geo_network = provider.NetworkName.replace(' ', '_')
                    lat = meta['location']['latitude']
                    lon = meta['location']['longitude']
                    des = meta['name'].replace(',', ' ')
                    url = f'http://selfie.cuahsi.org/{net}/{code}'
                    f.write(f'https://geoconnex.us/cuahsi/his/{geo_network}/{code},')
                    f.write(f'{url},')
                    f.write(f'{args.creator},')
                    f.write(f'{des},')
                    f.write(f'{lat},')
                    f.write(f'{lon},')
                    f.write(f'QueryString,')
                    f.write(f'f?=.*,')
                    f.write(f'{url}?f=${{C:f:1}}\n')
        except Exception as e:
            failed[pid] = str(e)
            continue

    
    print(f'\nSkipped: {len(skipped.keys())} providers')
    for k, v in skipped.items():
        print(f'{k} - {v}') 

    print(f'\nFailed: {len(failed.keys())} providers')
    for k, v in failed.items():
        print(f'FAILED: {k} - {v}') 


import suds
import ulmo
import pyhis

"""
FAILED: TRMM_3B42_7 - Type not found: 'queryInfo'
FAILED: EnviroDIY - HTTP Error 500: Internal Server Error
FAILED: NLDAS_FORA - Server raised fault: 'Unrecognized service. List of available method(s): GetSites GetSitesXml GetSiteInfo GetSiteInfoObject GetVariableInfo GetVariableInfoObject GetValues GetValuesObject'
FAILED: TarlandHydrology - <unknown>:138:7: mismatched tag
FAILED: WW2100 OHIS - <unknown>:138:7: mismatched tag
FAILED: NLDAS_NOAH - Server raised fault: 'Unrecognized service. List of available method(s): GetSites GetSitesXml GetSiteInfo GetSiteInfoObject GetVariableInfo GetVariableInfoObject GetValues GetValuesObject'
FAILED: OGIMET-ARCTIC - <unknown>:1:269: not well-formed (invalid token)
FAILED: GHCN - 'location'
FAILED: EPA_Lake_Harsha_Data - <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)>
FAILED: RushValley - HTTP Error 404: Not Found
"""

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

ids = [
       'TRMM_3B42_7',
       'EnviroDIY',
       'NLDAS_FORA',
       'TarlandHydrology',
       'WW2100 OHIS',
       'NLDAS_NOAH',
       'OGIMET-ARCTIC',
       'GHCN',
       'EPA_Lake_Harsha_Data',
       'RushValley']

services = pyhis.Services()
providers = services.get_data_providers()

suds_failed = {}
ulmo_failed = {}
for i in ids:
    provider = get_provider(providers, i)
    if provider is None:
        print(f'Skipping {i}')
        continue
    wsdl = provider['servURL']
    name = provider['NetworkName']
    
    try:
        print(f'Querying {name} [SUDS]...', end='', flush=True)
        client = suds.client.Client(wsdl)
        sites = client.service.GetSites()
        print('success')
    except Exception as e:
        print(f'FAILED')
        suds_failed[name] = str(e)



    try:
        print(f'Querying {name} [ULMO]...', end='', flush=True)
        sites = ulmo.cuahsi.wof.get_sites(wsdl)
        print('success')
    except Exception as e:
        ulmo_failed[name] = str(e)
        print('FAILED')

print('\nThe following providers failed during GetSites query [SUDS]')
for i, f in suds_failed.items():
    print(f'{i}: {f}')

print('\nThe following providers failed during GetSites query [ULMO]')
for i, f in ulmo_failed.items():
    print(f'{i}: {f}')



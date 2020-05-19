
import numpy
from libs import pyhis
from flask import abort


def get_provider(network):
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

    return pdata

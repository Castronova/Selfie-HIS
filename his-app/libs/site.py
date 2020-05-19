
import ulmo
from flask import abort
from flask import render_template


def get_sites(provider):

    # get sites for provider
    try:
        sites = ulmo.cuahsi.wof.get_sites(provider['servURL'])
    except Exception as e:
        return render_template('500.html', data=dict(error=e))
    return sites


def get_site(provider, network, siteid):

    # get info for single site
    try:
        return ulmo.cuahsi.wof.get_site_info(provider['servURL'],
                                             [f'{network}:{siteid}'])
    except Exception:
        abort(404)

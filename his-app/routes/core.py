#!/usr/bin/env python3

from flask import render_template, request

from libs import pyhis
from . import routes


@routes.route('/')
@routes.route('/index')
def index():
    his = pyhis.Services()
    dp = his.get_data_providers()
    dat = []
    for idx, p in dp.iterrows():
        dat.append(dict(name=p.Title,
                        url=f'{request.url}{p.NetworkName}',
                        sitecount=f'{p.sitecount}',
                        orgsite=f'{p.orgwebsite}'))

    return render_template("index.html", data=dat)

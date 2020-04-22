#!/usr/bin/env python3

import json
from flask import jsonify, render_template, request

from libs import pyhis
from contexts import elf
from . import routes


@routes.route('/')
@routes.route('/index')
def index():
    his = pyhis.Services()
    dp = his.get_data_providers()
    dat = []
    for idx, p in dp.iterrows():
        dat.append(dict(name=p.Title, url=f'{request.url}{p.NetworkName}'))

    return render_template("index.html", data=dat)

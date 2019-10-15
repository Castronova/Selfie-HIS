#!/usr/bin/env python3

from flask import render_template
from . import routes


@routes.errorhandler(404)
def not_found(error):
    return render_template("404.html")


#!/usr/bin/env python3

import os
from flask import Flask
from routes import *

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

app = Flask('CUAHSI SELFIE',
            template_folder=template_dir,
            static_folder=static_dir,
            static_url_path='/static')

app.config['JSON_SORT_KEYS'] = False
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)

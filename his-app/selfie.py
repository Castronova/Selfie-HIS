#!/usr/bin/env python3

import os
from flask import Flask
from routes import *

# necessary to allow unverified ssl calls
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

application = Flask('CUAHSI SELFIE',
            	    template_folder=template_dir,
            	    static_folder=static_dir,
            	    static_url_path='/static')

application.config['JSON_SORT_KEYS'] = False
application.register_blueprint(routes)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)

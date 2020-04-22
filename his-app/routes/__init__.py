from flask import Blueprint
routes = Blueprint('routes', __name__)

from .core import *
from .site import *
from .provider import *
from .error import *

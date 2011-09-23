#!/usr/bin/env python

import logging
import re
import sys

from django.utils import simplejson
from google.appengine.ext import webapp

class APIController(webapp.RequestHandler):
    def post(self):
        
    

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

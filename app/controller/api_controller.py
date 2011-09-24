#!/usr/bin/env python

import logging
import re
import sys

from django.utils import simplejson
from google.appengine.ext import webapp

class APIController(webapp.RequestHandler):
    def get(self):
        self.response.headers[ 'content-type' ] = 'text/event-stream'
        
        self.response.out.write( 'shit' );
    

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

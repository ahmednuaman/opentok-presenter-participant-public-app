#!/usr/bin/env python

import sys
import uuid

from app.model import channel_model
from django.utils import simplejson
from google.appengine.api import channel
from google.appengine.ext import webapp

class APIController(webapp.RequestHandler):
    def get(self):
        self.response.out.write('shit')
    
    def post(self):
        i   = str( uuid.uuid4() )
        t   = channel.create_channel( i )
        
        channel_model.add_channel( t )
        
        self.response.out.write( t )
    

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

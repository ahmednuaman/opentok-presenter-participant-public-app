#!/usr/bin/env python

import logging
import re
import sys

from app.controller import crush_controller
from app.controller import user_controller
from app.helper import encryption_helper
from app.model import log_model
from app.model import user_model
from django.utils import simplejson
from google.appengine.ext import webapp

class APIController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'req' )
        
        if req is None:
            error( 'No request' )
            
        else:
            req = encryption_helper.decode( req )
            
            try:
                req = simplejson.loads( req )
                
            except ValueError:
                error( 'This does\'t look like JSON: ' + req )
            
            if req[ 'method' ]:
                m   = req[ 'method' ]
                
                if m == 'check_user':
                    res = user_controller.check_user( req[ 'uid' ] )
                    
                elif m == 'set_crushes':
                    res = crush_controller.set_crushes( req[ 'uid' ], req[ 'crushes' ] )
                    
                elif m == 'set_crush':
                    res = crush_controller.set_crush( req[ 'uid' ], req[ 'crush' ] )
                    
                elif m == 'get_crushes':
                    res = crush_controller.get_crushes( req[ 'uid' ] )
                    
                elif m == 'remove_crush':
                    res = crush_controller.remove_crush( req[ 'uid' ], req[ 'crush' ] )
                    
                else:
                    error( 'Not a valid method: ' + req[ 'method' ] )
                    
                res = simplejson.dumps( res )
                
                res = encryption_helper.encode( res )
                
                self.response.headers[ 'content-type' ] = 'application/json'
                
                self.response.out.write( res )
                
            else:
                error( 'No method supplied' )
            
        
    

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

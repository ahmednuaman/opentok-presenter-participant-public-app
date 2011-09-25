#!/usr/bin/env python

import os
import sys
import uuid

from app.model import channel_model
from app.model import stream_model
from django.utils import simplejson
from google.appengine.api import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

COOKIE_NAME = 'FLokfGUUiprgVdCUHSKZvxb8qV5yWVjA0WS3z6UXJliYCXRAsSoJJ4BCi6GcTZb'

class PublicController(webapp.RequestHandler):
    def post(self):
        i   = str( uuid.uuid4() )
        t   = channel.create_channel( i )
        
        channel_model.add_channel( t )
        
        self.response.out.write( t )
    

class PresenterController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'method' )
        
        msg = None
        
        if req is 'set_streams':
            msg = simplejson.loads( self.request.get( 'streams' ) )
        
        if msg is not None:
            msg = simplejson.dumps( msg )
            
            send( msg )
        
    

class ParticipantController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'method' )
    

class LoginController(webapp.RequestHandler):
    def get(self):
        load( self )
    
    def post(self):
        pre = pre_or_part( self, True, False )
        l   = False
        e   = False
        
        if pre:
            if self.request.get( 'username' ) == 'Christy' and self.request.get( 'password' ) == 'mklohyzaxiW9VMIi1hTLmRoX8tL3bPU4bQIoAjyHH9Ih6GaBtUpymkFR49yO4qd':
                l   = True
                
            else:
                e   = True
            
            self.request.cookies[ COOKIE_NAME ] = 1 if l else 0
        
        load( self, { 'error': e, 'logged_in': l } )
    

def pre_or_part(s, t, f):
    return t if s.request.path == '/presenter/login' else f

def load(s, d={ }):
    s.response.out.write( template.render( 'template/' + pre_or_part( s, 'presenter', 'participant' ) + '.html', d ) )

def send(m):
    cs  = channel_model.get_channels()
    
    for c in cs:
        channel.send_message( c, m )
    

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

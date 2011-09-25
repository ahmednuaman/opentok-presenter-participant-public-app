#!/usr/bin/env python

import os
import sys
import uuid

from app.helper import config_helper
from app.helper import opentok_helper
from app.model import channel_model
from app.model import stream_model
from django.utils import simplejson
from google.appengine.api import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

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
        
        if req == 'set_streams':
            msg = simplejson.loads( self.request.get( 'streams' ) )
            
        elif req == 'connected':
            stream_model.add_stream( self.request.get( 'session_id' ), True, True )
            
            msg = True
            
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
        c   = config()
        l   = False
        e   = False
        t   = ''
        
        if pre:
            if self.request.get( 'username' ) == c.pre.username and self.request.get( 'password' ) == c.pre.password:
                l   = True
                
                sdk = opentok_helper.OpenTokSDK( c.tokbox.api_key, c.tokbox.secret )
                
                s   = sdk.create_session( self.request.url )
                t   = sdk.generate_token( s.session_id, c.role.presenter, c.pre.username )
                
            else:
                e   = True
            
            self.request.cookies[ c.cookie_name ] = 1 if l else 0
        
        load( self, { 'error': e, 'logged_in': l, 'token': t, 'session_id': s.session_id, 'config': c.tokbox } )
    

def config():
    c   = config_helper.config()
    
    return c

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

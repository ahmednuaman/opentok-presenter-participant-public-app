#!/usr/bin/env python

import datetime
import os
import sys
import uuid

from app.helper import config_helper
from app.helper import opentok_helper
from app.model import channel_model
from app.model import participant_model
from app.model import stream_model
from django.utils import simplejson
from gaesessions import get_current_session
from google.appengine.api import channel
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PublicController(webapp.RequestHandler):
    def post(self):
        self.response.out.write( create_channel() )
    

class PresenterController(webapp.RequestHandler):
    def post(self):
        sess    = get_current_session()
        
        if sess.is_active() is False:
            error( 'Not authed' )
        
        if sess.has_key( 'logged_in' ) is False:
            error( 'Bad session' )
        
        if sess[ 'logged_in' ] is not True:
            error( 'Not logged in' )
        
        req = self.request.get( 'method' )
        
        msg = None
        
        if req == 'set_streams':
            msg = simplejson.loads( self.request.get( 'streams' ) )
            
        elif req == 'connected':
            stream_model.delete_current_presenter()
            
            stream_model.add_stream( self.request.get( 'stream_id' ), True, True )
            
            msg = stream_model.get_streams()
            
        
        if req == 'connected' or req == 'update':
            get_all_streams( self )
            
        
        if msg is not None:
            msg = simplejson.dumps( msg )
            
            send( msg )
        
    

class ParticipantController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'method' )
        
        msg = None
        
        if req == 'connected':
            stream_model.add_stream( self.request.get( 'stream_id' ) )
            
            msg = create_channel()
            
        if msg is not None:
            msg = simplejson.dumps( msg )
            
            send( msg )
        
    

class LoginController(webapp.RequestHandler):
    def get(self):
        load( self )
    
    def post(self):
        pre = pre_or_part( self, True, False )
        c   = config()
        l   = False
        e   = False
        s   = ''
        t   = ''
        
        
        sess    = get_current_session()
        
        if sess.is_active():
            sess.terminate()
        
        if pre:
            if self.request.get( 'username' ) == c.pre.username and self.request.get( 'password' ) == c.pre.password:
                l   = True
                
            else:
                e   = True
            
            if l:
                sess[ 'logged_in' ] = True
            
        else:
            em  = self.request.get( 'email' )
            
            if len( em ) > 0:
                part    = participant_model.get_participant_by_email( em )
                
                if part is not None:
                    l   = True
                    
                else:
                    e   = True
                    
                
            else:
                e   = True
                
            
        
        if l:
            sdk = opentok_helper.OpenTokSDK( c.tokbox.api_key, c.tokbox.secret )
            
            # s   = sdk.create_session( self.request.url ).session_id
            t   = sdk.generate_token( c.tokbox.session_id, c.role.presenter if pre else c.role.participant )
        
        d   = { 'error': e, 'logged_in': l, 'token': t, 'session_id': c.tokbox.session_id, 'config': c.tokbox, 'email': '', 'time': '' }
        
        if pre is False and l and part:
            d[ 'email' ]    = em
            d[ 'time']      = part.time
        
        load( self, d )
    

class AddInitDataController(webapp.RequestHandler):
    def get(self):
        participant_model.add_participant( 'ahmednuaman@googlemail.com', datetime.datetime.now() )
    

def config():
    c   = config_helper.config()
    
    return c

def create_channel():
    i   = str( uuid.uuid4() )
    t   = channel.create_channel( i )
    
    channel_model.add_channel( t )
    
    return t

def get_all_streams(s):
    s.response.out.write( simplejson.dumps( stream_model.get_all_streams() ) )

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

#!/usr/bin/env python

import datetime
import os
import sys
import uuid

from app.helper import config_helper
from app.helper import opentok_helper
from app.model import participant_model
from app.model import stream_model
from django.utils import simplejson
from gaesessions import get_current_session
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class PublicController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'method' )
        
        if req is None:
            error( 'No method' )
            
        
        if req == 'get_streams':
            self.response.out.write( simplejson.dumps( stream_model.get_streams() ) )
        
    
    def get(self):
        c   = config()
        
        sdk = opentok_helper.OpenTokSDK( c.tokbox.api_key, c.tokbox.secret )
        
        t   = sdk.generate_token( c.tokbox.session_id, c.role.public )
        
        d   = { 'token': t, 'session_id': c.tokbox.session_id, 'config': c.tokbox }
        
        self.response.out.write( template.render( 'template/public.html', d ) )
    

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
        
        if req == 'set_stream':
            stream_model.delete_current_participant()
            
            stream_model.update_stream( self.request.get( 'stream_id' ), True )
            
        elif req == 'connected':
            stream_model.delete_current_participant()
            stream_model.delete_current_presenter()
            
            stream_model.add_stream( self.request.get( 'stream_id' ), True, True )
            
        if req == 'connected' or req == 'update':
            get_all_streams( self )
            
        
    

class ParticipantController(webapp.RequestHandler):
    def post(self):
        req = self.request.get( 'method' )
        
        if req == 'connected':
            stream_model.add_stream( self.request.get( 'stream_id' ) )
            
            d   = { 'presenter_id': stream_model.get_current_presenter() }
            
            self.response.out.write( simplejson.dumps( d ) )
            
        
    

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
        participant_model.add_participant( 'ahmednuaman@googlemail.com', '7:00' )
        participant_model.add_participant( 'tmillar48@hotmail.co.uk', '8:00' ) # 8
        participant_model.add_participant( 'martin.reed@bbh.co.uk', '8:10' ) # 8.10
        participant_model.add_participant( 'daniel@mothernewyork.com', '8:20' ) # 8.20
        participant_model.add_participant( 'melanie.arrow@bbh.co.uk', '8:30' ) # 8.30
    

def config():
    c   = config_helper.config()
    
    return c

def get_all_streams(s):
    s.response.out.write( simplejson.dumps( stream_model.get_all_streams() ) )

def pre_or_part(s, t, f):
    return t if s.request.path == '/presenter/login' else f

def load(s, d={ }):
    s.response.out.write( template.render( 'template/' + pre_or_part( s, 'presenter', 'participant' ) + '.html', d ) )

def error(s):
    logging.error( s )
    
    print s
    
    sys.exit(0)

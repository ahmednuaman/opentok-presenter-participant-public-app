#!/usr/bin/env python

from google.appengine.ext import db

class StreamModel(db.Model):
    stream  = db.StringProperty()
    active  = db.BooleanProperty(default=False)

def add_stream(s):
    m   = StreamModel()
    
    m.stream    = s
    
    m.put()

def add_streams(a):
    for s in a:
        m   = StreamModel()
        
        m.stream    = s
        
        m.put()
    

def get_stream(s):
    q   = StreamModel().gql( 'WHERE stream = :1', s ).get()
    
    return q

def get_streams():
    q   = StreamModel().all()
    
    ss  = [ ]
    
    if q is not None:
        for s in q:
            ss.append( { 'stream': s.stream, 'active': s.active } )
        
    
    return ss

def update_stream(s, a):
    s   = get_stream( s )
    
    s.active    = a
    
    s.put()

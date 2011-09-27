#!/usr/bin/env python

from google.appengine.ext import db

class StreamModel(db.Model):
    stream      = db.StringProperty()
    active      = db.BooleanProperty(default=False)
    presenter   = db.BooleanProperty(default=False)

def add_stream(s, a=False, p=False):
    m   = StreamModel()
    
    m.stream    = s
    m.active    = a
    m.presenter = p
    
    if p:
        delete_current_presenter()
    
    m.put()

def add_streams(a):
    for s in a:
        m   = StreamModel()
        
        m.stream    = s
        
        m.put()
    

def get_current_presenter():
    q   = StreamModel().gql( 'WHERE presenter = :1', True ).get()
    
    if q is not None:
        return q.stream

def get_stream(s):
    q   = StreamModel().gql( 'WHERE stream = :1', s ).get()
    
    if q is not None:
        return q.stream

def get_streams():
    q1  = StreamModel().gql( 'WHERE presenter = :1', True ).get()
    q2  = StreamModel().gql( 'WHERE active = :1 and presenter = :2', True, False ).get()
    
    ss  = { 'presenter': str( q1.stream ) if q1 is not None else '', 'participant': str( q2.stream ) if q2 is not None else '' }
    
    return ss

def get_all_streams():
    q   = StreamModel().gql( 'WHERE presenter = :1', False ).fetch( 1000 )
    
    ss  = [ ]
    
    if q is not None:
        for s in q:
            ss.append( s.stream )
        
    
    return ss

def update_stream(s, a):
    s   = StreamModel().gql( 'WHERE stream = :1', s ).get()
    
    s.active    = a
    
    s.put()

def delete_current_participant():
    q   = StreamModel().gql( 'WHERE active = :1 and presenter = :2', True, False ).get()
    
    if q is not None:
        q.active    = False
        
        q.put()
    

def delete_current_presenter():
    q   = StreamModel().gql( 'WHERE presenter = :1', True ).get()
    
    if q is not None:
        q.delete()
    

#!/usr/bin/env python

import datetime

from google.appengine.ext import db

class ParticipantModel(db.Model):
    email   = db.StringProperty()
    time    = db.DateTimeProperty()

def add_participant(s, t):
    m   = ParticipantModel()
    
    m.email = s
    m.time  = t
    
    m.put()

def get_participant_by_email(e):
    q   = ParticipantModel().gql( 'WHERE email = :1', e ).get()
    
    return q

def get_participants():
    q   = ParticipantModel().all()
    
    ps  = [ ]
    
    if q is not None:
        for p in q:
            ps.append( c.channel )
        
    
    return ps

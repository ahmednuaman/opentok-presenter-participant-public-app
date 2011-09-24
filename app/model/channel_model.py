#!/usr/bin/env python

from google.appengine.ext import db

class ChannelModel(db.Model):
    channel = db.StringProperty()

def add_channel(s):
    m   = ChannelModel()
    
    m.channel   = s
    
    m.put()

def get_channels():
    q   = ChannelModel().all()
    
    cs  = [ ]
    
    if q is not None:
        for c in q:
            cs.append( c.channel )
        
    
    return cs

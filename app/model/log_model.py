#!/usr/bin/env python

from google.appengine.ext import db

class LogModel(db.Model):
    uid         = db.StringProperty()
    timestamp   = db.DateTimeProperty(auto_now_add=True)
    action      = db.StringProperty()

def log(uid, action):
    m   = LogModel()
    
    m.uid       = uid
    m.action    = action
    
    m.put()

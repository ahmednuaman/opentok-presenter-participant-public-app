#!/usr/bin/env python

from google.appengine.ext import db

class StreamModel(db.Model):
    stream  = db.StringProperty()
    active  = db.BooleanProperty(default=False)

def add_stream(s):
    

def add_streams(a):
    

def get_stream(s):
    

def get_streams():
    

def update_stream(s):
    

#!/usr/bin/env python

import yaml

from google.appengine.api import memcache

class obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)
            
        
    

def config():
    c = memcache.get( 'config' )
    
    if c is None:
        f   = open( 'config.yaml' )
        
        c   = yaml.load( f.read() )
        
        c   = obj( c )
        
        memcache.add( 'config', c )
    
    return c

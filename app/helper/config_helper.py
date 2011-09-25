#!/usr/bin/env python

import yaml

from google.appengine.api import memcache

def config():
    c = memcache.get( 'config' )
    
    if c is None:
        f   = open( 'config.yaml' )
        
        c   = yaml.load( f.read() )
        
        memcache.add( 'config', c )
    
    return c

#!/usr/bin/env python

import sys

from app.controller import api_controller
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

def main():
    application = webapp.WSGIApplication( [
        ( '/api',   api_controller.APIController )
    ], debug=True )
    util.run_wsgi_app( application )

if __name__ == '__main__':
    main()

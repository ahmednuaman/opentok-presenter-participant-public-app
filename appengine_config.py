from gaesessions import SessionMiddleware

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
import os
COOKIE_KEY = ')[DY\'A]U\5i<gRS:dPYh<}Zia>Ic0GtS2[">~}M@7a-uhX^C#K2jod\)IaAB@e=Af!n&*EUd+(IA-WeJ=,+E>FHdb;S]Uc:\"2t5WulzN|xnJw+OQVj"th=6wv\'#4-+n;/.,u?agp":LC{m{1-(BupxSjI@OC!K2:hTk#;YoG/r^SH6sF;8D:ST#&<F+E'

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
  app = recording.appstats_wsgi_middleware(app)
  return app

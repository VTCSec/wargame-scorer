#!/usr/bin/env python2
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site
from twisted.internet import reactor
from flask import Flask, render_template, g

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)

def check_scores():
    print "checking scores..."
    reactor.callLater(5, check_scores)

reactor.callLater(5, check_scores)
reactor.listenTCP( 8080, site )
reactor.run()


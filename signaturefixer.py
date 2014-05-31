__author__ = "Fernando Medrano"
__date__ = "Mar 6, 20143"
__license__ = "MIT"

import argparse
import codecs
import json
import pymongo
import urllib2
from pprint import PrettyPrinter
import sys
from pymongo import MongoClient
import threading

def url_expander_thread(thisTweet,numero):
    print("iniciando hilo %s " % str(numero))
    try:
        client = MongoClient('localhost', 27017)
        db = client['todos_tweets']
    except Exception as e:
        print('*** STOPED %s' % str(e))

    resp = urllib2.urlopen(thisTweet["tweet"]["entities"]["urls"][-1]["expanded_url"])
    str_url = resp.url
    thisTweet["over_expanded_url"] = str_url

    params = str_url.split('/')
    keys = params[len(params)-1].split('?')
    checkin_id = keys[0]
    if (len(keys)>1):
        lastvars = keys[1].split('&')
        almost_signature = lastvars[0].split('=')
        if(len(almost_signature[1]) > 3) :
            signature = almost_signature[1]
        else:
            signature = None
    else:
        signature = None
    print '{0} - {1}'.format( str(checkin_id), str(signature))
    thisTweet["checkin_id"] = checkin_id
    thisTweet["signature"] = signature
    try:
        db.activities.save(thisTweet)
    except Exception as e:
        print('*** STOPED %s' % str(e))

if __name__ == '__main__':
    # Construct the client object
    #client = foursquare.Foursquare(client_id='NT3I005CN2G5FQATJNONYEGENXAIJTEGBCA5KUKFHWFVJNWB', client_secret='ZMDXLTCEU2BXJNHHHLRD23I4GUXTPHMEMJ3ATQQFCJEW5RDL', redirect_uri='http://www.agenciaunica.com')

    # Build the authorization url for your app 
    #auth_uri = client.oauth.auth_url()
    #print auth_uri
    
    try:
            client = MongoClient('localhost', 27017)
            db = client['todos_tweets']
            activities = db.activities
    
    
    except Exception as e:
	    print('*** STOPED %s' % str(e))
        
    try:
        i = 0;
        for a in range (20):
            lastTweets = activities.find({"$where": "this.checkin_id.length < 8"}).sort('id', -1).limit(1000)
            for lastTweet in lastTweets:
                t = threading.Thread(target=url_expander_thread, args=(lastTweet, i)) 
                t.start()
                i+=1
                if (i % 5) == 0 : 
                    t.join()
    except Exception as e:
        print lastTweet["tweet"]["entities"]["urls"][-1]["expanded_url"]
        print('*** STOPPED %s' % str(e))

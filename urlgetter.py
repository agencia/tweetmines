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
	    
    #print thisTweet["_id"]
    #print "\n%s" % (thisTweet["entities"]["urls"][-1]["expanded_url"])
    resp = urllib2.urlopen(thisTweet["entities"]["urls"][-1]["expanded_url"])
    str_url = resp.geturl()
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
    #print checkin_id
    #print signature
            
    try:
        if signature is None:
            activitie = { "tweet": thisTweet, "signature": None, "over_expanded_url": str(str_url), "checkin_id": str(checkin_id)}
        else :
            activitie = { "tweet": thisTweet, "signature": str(signature), "over_expanded_url": str(str_url), "checkin_id": str(checkin_id)}
        db.tweets.save(thisTweet)
        db.tweets.remove(thisTweet)
        db.activities.insert(activitie)
        #print "checkin {}, signature {}, url {}".format(checkin_id, signature, str_url)
        print("ha finalizado el hilo %s " % str(numero))
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
            tweets = db.tweets
    
    
    except Exception as e:
	    print('*** STOPED %s' % str(e))
    try:
        i = 0;
        for a in range(100):
            lastTweets = tweets.find({'over_expanded_url': { '$exists': False }}).limit(1000)
            for lastTweet in lastTweets:
                t = threading.Thread(target=url_expander_thread, args=(lastTweet, i)) 
                t.start()
                i+=1
                if (i % 30) == 0 : 
                    t.join()
                
    except Exception as e:
        print('*** STOPPED %s' % str(e))
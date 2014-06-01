__author__ = "Fernando Medrano"
__date__ = "Mar 5, 20143"
__license__ = "MIT"

import argparse
import codecs
import json
import pymongo
import urllib2
from pprint import PrettyPrinter
import sys
from pymongo import MongoClient
import foursquare
import datetime
import threading

def checkin_getter_thread(thisActivitie, numero, thisClient):
    print "ha iniciado el hilo {}".format(numero)
    try:
            client = MongoClient('localhost', 27017)
            db = client['todos_tweets']
    except Exception as e:
	    print('*** STOPED %s' % str(e))
    
    #print lastActivitie["_id"]
    try:
        if thisActivitie["signature"] is None:
            checkin = thisClient.checkins(str(thisActivitie["checkin_id"]))
        else:
            checkin = thisClient.checkins(str(thisActivitie["checkin_id"]),params={'signature':str(thisActivitie["signature"])})
        thisActivitie["checkin"] = checkin
        #print "location is {},{}".format(checkin["checkin"]["venue"]["location"]["lat"],checkin["checkin"]["venue"]["location"]["lng"])
        urllib2.urlopen("http://agenciaunica.com/setpin?pin={},{}".format(checkin["checkin"]["venue"]["location"]["lat"],checkin["checkin"]["venue"]["location"]["lng"]))

        db.activities.save(thisActivitie)
        print "ha finalizado el hilo {}, checkin_id: {}, CC: {}".format(numero, thisActivitie["checkin_id"],checkin["checkin"]["venue"]["location"]["cc"])
        #print 'rate remaining {0}'.format(thisClient.rate_remaining)
    except Exception as e:
        if str(e).startswith('Invalid checkin id') :
            print('**** removing checkin_id :  %s' % thisActivitie["checkin_id"])
            db.activities.remove({'checkin_id' : str(thisActivitie['checkin_id'])})
        #if str(e) == 'Quota exceeded' :
        #break;
        print('*** STOPED %s' % str(e))
        print('*** CheckinID: %s' %thisActivitie["checkin_id"])
                        

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
            accounts = db.accounts
    
    
    except Exception as e:
	    print('*** STOPED %s' % str(e))

    try:
        clients = accounts.find({}).sort('usage', 1)
        i=0
        for account in clients:
            client_4sqr = foursquare.Foursquare(client_id=account['client_id'], client_secret=account['secret'], version='20140423')
            #print 'rate remaining {0}'.format(client_4sqr.rate_remaining())
            inicio = datetime.datetime.utcnow()
            try:
                lastActivities = activities.find({'checkin': { '$exists': False }}).sort('id', -1).limit(500)
                for lastActivitie in lastActivities:
                    t = threading.Thread(target=checkin_getter_thread, args=(lastActivitie, i, client_4sqr)) 
                    t.start()
                    i+=1
                    if (i % 30) == 0 : 
                        t.join()
            except Exception as e:
                print('*** STOPPED %s' % str(e))
                
            fin = datetime.datetime.utcnow()
            account["usage"] = fin
            db.accounts.save(account)
            print('inicio %s' % str(inicio))
            print('fin %s' % str(fin))
            
    except Exception as e:
        print('*** STOPPED %s' % str(e))
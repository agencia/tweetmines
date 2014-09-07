import pymongo
import json
import urllib

from pymongo import MongoClient

if __name__ == '__main__':
	try:
            client = MongoClient('localhost', 27017)
            db = client['devtweets']
            tweets = db.tweets
        except Exception as e:
                print('*** STOPPED %s' % str(e))

	for tweet in tweets.find():
		print "\n%s" % (tweet["entities"]["urls"][0]["expanded_url"])
		resp = urllib.urlopen(tweet["entities"]["urls"][0]["expanded_url"])
		print resp.url

__author__ = "Fernando Medrano"
__date__ = "Nov 23, 2013"
__license__ = "MIT"

import argparse
import codecs
import json
import pymongo
from pprint import PrettyPrinter
import sys
from pymongo import MongoClient



if __name__ == '__main__':
        # print UTF-8 to the console
        try:
                # python 3
                sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
        except:
                # python 2
                sys.stdout = codecs.getwriter('utf8')(sys.stdout)

        try:
            client = MongoClient('localhost', 27017)
            db = client['devtweets']
            tweets = db.tweets
        except Exception as e:
                print('*** STOPPED %s' % str(e))
            

        try:
                lastTweet = tweets.find({}).sort('id', -1).limit(1)
                print lastTweet[0]["id"];
        except KeyboardInterrupt:
                print('\nTerminated by user')
                
        except Exception as e:
                print('*** STOPPED %s' % str(e))

__author__ = "Fernando Medrano"
__date__ = "Nov 23, 2013"
__license__ = "MIT"

import argparse
import codecs
import json
import pymongo
from pprint import PrettyPrinter
import sys
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
from pymongo import MongoClient


def search(name, obj):
        """Breadth-first search for name in the JSON response and return value."""
        q = []
        q.append(obj)
        while q:
                obj = q.pop(0)
                if hasattr(obj, '__iter__'):
                        isdict = type(obj) is dict
                        if isdict and name in obj:
                                return obj[name]
                        for k in obj:
                                q.append(obj[k] if isdict else k)
        else:
                return None


def to_dict(param_list):
        """Convert a list of key=value to dict[key]=value"""                        
        if param_list:
                return {name: value for (name, value) in [param.split('=') for param in param_list]}
        else:
                return None


if __name__ == '__main__':
        # print UTF-8 to the console
        try:
                # python 3
                sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
        except:
                # python 2
                sys.stdout = codecs.getwriter('utf8')(sys.stdout)

        parser = argparse.ArgumentParser(description='Request any Twitter Streaming or REST API endpoint')
        parser.add_argument('-oauth', metavar='FILENAME', type=str, help='file containing OAuth credentials')
        parser.add_argument('-endpoint', metavar='ENDPOINT', type=str, help='Twitter endpoint')
        parser.add_argument('-parameters', metavar='NAME_VALUE', type=str, help='parameter NAME=VALUE', nargs='+')
        parser.add_argument('-fields', metavar='FIELD', type=str, help='print a top-level field in the json response', nargs='+')
        args = parser.parse_args()        

        try:
            client = MongoClient('localhost', 27017)
            db = client['devtweets']
            tweets = db.tweets
        except Exception as e:
                print('*** STOPPED %s' % str(e))
            

        try:
                params = to_dict(args.parameters)
                oauth = TwitterOAuth.read_file('./credentials.txt')
                api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access_token_key, oauth.access_token_secret)
                """response = api.request('statuses/filter', {'locations':'-102.878723,21.659981,-101.997757,22.473779'})"""
                #response = api.request('search/tweets', {'q':'Aguascalientes 4sq com, ags 4sq com', 'count': 450})
                lastTweet = tweets.find({}).sort('id', -1).limit(1)
                str_lastTweetId = str(lastTweet[0]["id"])
                pager = TwitterRestPager(api, 'search/tweets', {'q':'Aguascalientes 4sq com, ags 4sq com', 'count':100, 'since_id': str_lastTweetId})

                #for item in response.get_iterator():
                for item in pager.get_iterator(10):
                    print item
                    tweets.insert(item)
                    #print ('\n' % pager.get_rest_quota())
				
        except KeyboardInterrupt:
                print('\nTerminated by user')
                
        except Exception as e:
                print('*** STOPPED %s' % str(e))

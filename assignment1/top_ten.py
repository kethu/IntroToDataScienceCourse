import csv
import sys
import json
import unicodedata
import operator

def to_ascii(string):
	return unicodedata.normalize('NFKD', string).encode('ascii','ignore')

def add_hashtags_to_hashchain(hashtags, hashchain):
	for hashtag in hashtags:
		hashtext = hashtag[u'text']
		if hashchain.has_key(hashtext):
			hashchain[hashtext] += 1
		else:
			hashchain[hashtext] = 1
	return hashchain
		

def get_hash_tags(file_name):
	tweet_file = open(file_name)
	hashchain = {}
	for tweet_string in tweet_file:
		tweet = json.loads(tweet_string)
		hashtags = tweet[u'entities'][u'hashtags'] if tweet.has_key(u'entities') else []
		hashchain = add_hashtags_to_hashchain(hashtags, hashchain)
	return hashchain

def main():
	hashchain = get_hash_tags(sys.argv[1])
	for hashtag in sorted(hashchain.iteritems(), key=operator.itemgetter(1))[::-1][0:10]:
		print hashtag[0] + " " + str(float(hashtag[1]))

if __name__ == '__main__':
	main()

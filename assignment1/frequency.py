import sys
import json
import unicodedata

def to_ascii(string):
	return unicodedata.normalize('NFKD', string).encode('ascii','ignore')

def get_tweets(file_name):
	tweet_file = open(file_name)
	tweets = []
	for tweet_string in tweet_file:
		tweet = json.loads(tweet_string)
		u_tweet_text = tweet[u'text'] if tweet.has_key(u'text') else u''
		tweets.append(to_ascii(u_tweet_text))
	return tweets

def get_term_frequencies(tweets):
	frequency = {}
	count = 0
	for tweet in tweets:
		for term in tweet.split(' '):
			count += 1
			if frequency.has_key(term):
				frequency[term] += 1
			else:
				frequency[term] = 1
	return (count, frequency)

def main():
	tweets = get_tweets(sys.argv[1])
	term_frequencies = get_term_frequencies(tweets)
	for term, occurence in term_frequencies[1].items():
		if (not "\n" in term) and (not " " in term) and term.strip():
			print term + " " + str(float(occurence)/float(term_frequencies[0]))

if __name__ == '__main__':
	main()

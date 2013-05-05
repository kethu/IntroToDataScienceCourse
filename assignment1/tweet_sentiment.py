import csv
import sys
import json
import unicodedata

def get_sentiment_dictionary(file_name):
	sentiment_tsv = csv.reader(open(file_name), delimiter='\t')
	sent_dict = {}
	for entry in sentiment_tsv:
		sent_dict[entry[0]] = int(entry[1])
	return sent_dict

def to_lower_ascii(string):
	return str.lower(unicodedata.normalize('NFKD', string).encode('ascii','ignore'))

def get_tweets(file_name):
	tweet_file = open(file_name)
	tweets = []
	for tweet_string in tweet_file:
		tweet = json.loads(tweet_string)
		u_tweet_text = tweet[u'text'] if tweet.has_key(u'text') else u''
		tweets.append(to_lower_ascii(u_tweet_text))
	return tweets

def get_sentiment_score(term, sentiment_dictionary):
	return sentiment_dictionary[term] if sentiment_dictionary.has_key(term) else 0

def compute_total_sentiment(tweet, sentiment_dictionary):
	terms = tweet.split(' ')
	total_sentiment = 0
	for term in terms:
		total_sentiment += get_sentiment_score(term, sentiment_dictionary)
	return float(total_sentiment)

def main():
    sentiment_dictionary = get_sentiment_dictionary(sys.argv[1])
    tweets = get_tweets(sys.argv[2])
    for tweet in tweets:
		print compute_total_sentiment(tweet, sentiment_dictionary)

if __name__ == '__main__':
    main()

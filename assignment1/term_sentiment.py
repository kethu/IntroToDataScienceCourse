import csv
import sys
import json
import unicodedata
import operator

CURSE = 1

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

def get_sentimental_tweets(tweets, sentiment_dictionary):
	sentimental_tweets = {}
	for tweet in tweets:
		sentimental_tweets[tweet] = compute_total_sentiment(tweet, sentiment_dictionary)
	return sentimental_tweets

def update_terms_in_sentiment_dictionary(terms, individual_sentiment, sentiment_dictionary):
	for term in terms:
		if sentiment_dictionary.has_key(term):
			sentiment_dictionary[term] += individual_sentiment
		else:
			sentiment_dictionary[term] = individual_sentiment
	return sentiment_dictionary

def update_sentiment_dictionary(tweets, sentiment_dictionary, curse):
	if curse==0:
		return sentiment_dictionary
	else:
		sentimental_tweets = get_sentimental_tweets(tweets, sentiment_dictionary)
		for tweet, total_sentiment in sentimental_tweets.items():
			terms = tweet.split(' ')
			individual_sentiment = total_sentiment / len(terms)
			sentiment_dictionary = update_terms_in_sentiment_dictionary(terms, individual_sentiment, sentiment_dictionary)
		return update_sentiment_dictionary(tweets, sentiment_dictionary, curse - 1)

def get_new_term_sentiments(tweets, sentiment_dictionary):
	existing_terms = sentiment_dictionary.keys()
	sentiment_dictionary = update_sentiment_dictionary(tweets, sentiment_dictionary, CURSE)
	for term in existing_terms:
		sentiment_dictionary.pop(term)
	return sorted(sentiment_dictionary.iteritems(), key=operator.itemgetter(1))

def main():
    sentiment_dictionary = get_sentiment_dictionary(sys.argv[1])
    tweets = get_tweets(sys.argv[2])
    for t_term in get_new_term_sentiments(tweets, sentiment_dictionary):
		if (not "\n" in t_term[0]) and (not " " in t_term[0]) and t_term[0].strip():
			print t_term[0] + " " + str(t_term[1])

if __name__ == '__main__':
    main()

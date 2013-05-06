import csv
import sys
import json
import unicodedata
import operator

def get_state_dictionary():
	return {'wyoming': 'WY', 'north dakota': 'ND', 'guam': 'GU', 'washington': 'WA', 'alaska': 'AK', 'tennessee': 'TN', 'iowa': 'IA', 'nevada': 'NV',
		'maine': 'ME', 'colorado': 'CO', 'mississippi': 'MS', 'south dakota': 'SD', 'hawaii': 'HI', 'new jersey': 'NJ', 'oklahoma': 'OK',
		'delaware': 'DE', 'minnesota': 'MN', 'north carolina': 'NC', 'illinois': 'IL', 'virgin islands': 'VI', 'arkansas': 'AR',
		'puerto rico': 'PR', 'indiana': 'IN', 'maryland': 'MD', 'louisiana': 'LA', 'national': 'NA', 'texas': 'TX', 'district of columbia': 'DC',
		'arizona': 'AZ', 'wisconsin': 'WI', 'michigan': 'MI', 'kansas': 'KS', 'utah': 'UT', 'virginia': 'VA', 'oregon': 'OR', 'connecticut': 'CT',
		'montana': 'MT', 'california': 'CA', 'new mexico': 'NM', 'new york': 'NY', 'rhode island': 'RI', 'vermont': 'VT', 'georgia': 'GA',
		'northern mariana islands': 'MP', 'pennsylvania': 'PA', 'florida': 'FL', 'american samoa': 'AS', 'kentucky': 'KY', 'missouri': 'MO',
		'nebraska': 'NE', 'new hampshire': 'NH', 'idaho': 'ID', 'west virginia': 'WV', 'south carolina': 'SC', 'ohio': 'OH', 'alabama': 'AL',
		'massachusetts': 'MA'}

def get_sentiment_dictionary(file_name):
	sentiment_tsv = csv.reader(open(file_name), delimiter='\t')
	sent_dict = {}
	for entry in sentiment_tsv:
		sent_dict[entry[0]] = int(entry[1])
	return sent_dict

def is_selectable_tweet(tweet, states):
	return tweet.has_key(u'text') and tweet.has_key(u'place') and tweet[u'place'] != None and tweet[u'place'][u'country_code'] == u'US' and states.has_key(to_lower_ascii(tweet[u'place'][u'name']))

def to_lower_ascii(string):
	return str.lower(unicodedata.normalize('NFKD', string).encode('ascii','ignore'))

def append_to_tweets(state_code, tweet_text, tweets):
	if tweets.has_key(state_code):
		tweets[state_code].append(tweet_text)
	else:
		tweets[state_code] = [tweet_text]
	return tweets

def filter_and_append_tweets(tweet, tweets):
	states = get_state_dictionary()
	if is_selectable_tweet(tweet, states):
		tweet_text = to_lower_ascii(tweet[u'text']) if tweet.has_key(u'text') else ''
		state_code = states[to_lower_ascii(tweet[u'place'][u'name'])]
		tweets = append_to_tweets(state_code, tweet_text, tweets)
	return tweets

def get_tweets(file_name):
	tweet_file = open(file_name)
	tweets = {}
	for tweet_string in tweet_file:
		tweet = json.loads(tweet_string)
		tweets = filter_and_append_tweets(tweet, tweets)
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
	state_tweets = get_tweets(sys.argv[2])
	state_score_dict = {}
	for state, tweets in state_tweets.items():
		state_score = 0
		for tweet in tweets:
			state_score += compute_total_sentiment(tweet, sentiment_dictionary)
		state_score_dict[state] = state_score
	sorted_state_score = sorted(state_score_dict.iteritems(), key=operator.itemgetter(1))
	print sorted_state_score[::-1][0][0]

if __name__ == '__main__':
	main()

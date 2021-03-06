import unittest
import tweepy
import requests
import json
import re
import twitter_info

## SI 206 - W17 - HW5
## COMMENT WITH:
## Your section day/time: sec 3/ Thursday 6pm
## Any names of people you worked with on this assignment:

######## 500 points total ########

## Write code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function),
# and prints out the Tweet text and the created_at value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm an awesome Python programmer.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017

## .. plus one more.

## You should cache all of the data from this exercise in a file, and submit the cache file along with your assignment. 

## So, for example, if you submit your assignment files, and you have already searched for tweets about "rock climbing",
# when we run your code, the code should use CACHED data, and should not need to make any new request to the Twitter API.
## But if, for instance, you have never searched for "bicycles" before you submitted your final files, then if we enter "bicycles" when we run your code,
# it _should_ make a request to the Twitter API.

## The lecture notes and exercises from this week will be very helpful for this. 
## Because it is dependent on user input, there are no unit tests for this -- we will run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

## **** For 50 points of extra credit, create another file called twitter_info.py that contains your consumer_key, consumer_secret,
# access_token, and access_token_secret, import that file here, and use the process we discuss in class to make that information secure!
# Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information for an 'extra' Twitter account you make just for this class,
# and not your personal account, because it's not ideal to share your authentication information for a real account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these with variables rather than filling in the empty strings if you choose to do the secure way for 50 EC points
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) # Set up library to grab stuff from twitter with your authentication, and return it in a JSON-formatted way

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except statement shown in class.
## 2. Write a function to get twitter data that works with the caching pattern, so it either gets new data or caches data, depending upon what the input to search for is. You can model this off the class exercise from Tuesday.
## 3. Invoke your function, save the return value in a variable, and explore the data you got back!
## 4. With what you learn from the data -- e.g. how exactly to find the text of each tweet in the big nested structure -- write code to print out content from 3 tweets, as shown above.



CACHE_FNAME = "cache_file.json"
try:
	cache_file_obj = open(CACHE_FNAME,'r')
	cache_contents = cache_file_obj.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}



def get_twitter (key_words):
	if key_words in CACHE_DICTION:
		print("get info from cache for ", key_words)
		py_obj = CACHE_DICTION[key_words]
	else:
		print("get info from the web for ", key_words)
		response = api.home_timeline()
		py_obj = response
		CACHE_DICTION[key_words] = py_obj
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	txt_list = []
	time_list = []
	for word_diction in py_obj:
		txt_list.append(word_diction["text"])
	for word_diction in py_obj:
		time_list.append(word_diction["created_at"])
	final_dict = {}
	count = 0
	for txt in txt_list:
		final_dict[txt] = time_list[count]
		count += 1
	return final_dict

def search_tw(key_word, dict):
	count = 0
	final_dict = {}
	for txt in dict:
		if re.search(key_word, txt):
			count += 1
			final_dict[txt] = dict[txt]
	return final_dict

def print_3_tw(txt_list, time_list):
	num = len(txt_list)
	if num > 3:
		count = 0
		while count < 3:
			print("TEXT:", txt_list[count], "\n", "CREATED AT: ", time_list[count], "\n")
			count += 1
	else:
		count = 0
		while count < num:
			print("TEXT:", txt_list[count], "\n", "CREATED AT: ", time_list[count], "\n")
			count += 1

def main_func():
	words = input("Enter a key word you want to search: ")
	twits = get_twitter(words)
	dict = search_tw(words, twits)
	txt_list = []
	time_list = []
	for key in dict.keys():
		txt_list.append(key)
		time_list.append(dict[key])
	print_3_tw(txt_list, time_list)

main_func()
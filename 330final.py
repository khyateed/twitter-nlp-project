# SI 300 Final Project, By Khyatee Desai: Democrats vs. Republicans on Twitter
#################### README: This project combines HTML from ballotpedia.org with JSON from Twitter.
# The HTML is parsed to retrieve a list of current US Senators, separated into Democrats and Republicans
# Each senator name is then passed into the Twitter Search API to retrieve their twitter handle
# The user then inputs a keyword they would like to search
# Finally, the keyword is passed with each senator's twitter handle into the Twitter search API to retrieve the number of republican vs democratic senator tweets that contain the given keyword.
##### NOTE: All requests are commented out to account for rate-limiting and program runntime. 

# Example- Enter a word you want to search (press q to quit): women
# Dem Tweet Count: 84
# Repub Tweet Count: 56


# ---------------------------------------- IMPORTS AND CREDENTIALS-----------------------------------------------
import re
from ggplot import *
import pandas
import csv
import json
from bs4 import BeautifulSoup
import requests_oauthlib
key = 'Et4XxRp4SCDn8wS30EKTJuVZf'
secret = 'soFn6mtJXNCBFV0cJMrPBOGROwM798TTVGUSjHBLJCwhiUAbcv'
access_token = '743466833177681922-cRuAJGl4AuO6Wi7PipIiq1ARpBgGeno'
access_secret = 'kBAlSNgRyaEmHZ0yh6ZfEnG2iNO1NLJqTI6LaenKxCfRQ'

# ------------------------------------ STEP 1: SCRAPE-----------------------------------------------
# This step scrapes names of current senators and appends them to the list, "members"


# base_url = 'https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress'
# r = requests.get(base_url)
# outfile = open('step1.html', 'w', encoding="utf-8")
# outfile.write(r.text)
# outfile.close()
					

members=[]
lis=[]

t = open('step1.html','r')
soup = BeautifulSoup(t, "html.parser")
table = soup.table.find_all('tr')
for person in table:
    tups=[]
    lis = person.text.split('\n')
    if len(lis)>2:
    	tups.append((lis[1], lis[2]))
    	members.append(tups)

#--------------------------------------- STEP 2: PARTIES------------------------------------
# this step splits members into two lists: democrats and republicans.
dems=[]
repubs = []
for person in members:
	name = person[0][0]
	if "Democratic" in person[-1][-1]:
		x = re.search('\D+', name)
		dems.append(x.group(0))
	else:
		x = re.search('\D+', name)
		repubs.append(x.group(0))




#------------------------------------------STEP 3: HANDLES---------------------------------
# This step searches twitter api for the names and retrieves a twitter handle, writing it to either "dem_handles.txt" or "repub_handles.txt"


oauth = requests_oauthlib.OAuth1Session(key,
                        client_secret= secret,
                        resource_owner_key= access_token,
                        resource_owner_secret=access_secret)


								#================ Democrat Handles  ======================
# t = open('dem_handles.txt', 'w')
# for name in dems:
# 	r = oauth.get("https://api.twitter.com/1.1/users/search.json?", params = {'q': name, 'count': 1})
# 	data =r.json()
# 	for dic in data:
# 		print(dic['screen_name'])
# 		t.write(dic['screen_name'])
# 		t.write(',')
# t.close()
								#================ Republican Handles ===================
# t = open('repub_handles.txt', 'w')
# for name in repubs:
# 	r = oauth.get("https://api.twitter.com/1.1/users/search.json?", params = {'q': name, 'count': 1})
# 	data =r.json()
# 	for dic in data:
# 		print(dic['screen_name'])
# 		t.write(dic['screen_name'])
# 		t.write(',')
# t.close()


#------------------------------------------ STEP 4: TWEETS--------------------------------------------------------
# use the democratic and republican twitter handles to make individual search requests to retrieve that person's top 5 tweets, and append to text files "dem_tweets.txt" and "repub_tweets.txt"
							
						#========================= Democrat Tweets =====================
# infile = open('dem_handles.txt', 'r')
# outfile = open('dem_tweets.txt', 'w')
# text = infile.read()
# handles = text.split(',')
# for handle in handles:
# 	r = oauth.get("https://api.twitter.com/1.1/search/tweets.json?", params = {'q':  handle , 'count':100, 'result_type': 'recent'  })
# 	data = r.json()
# 	try:
# 		for status in data['statuses']:
# 			outfile.write(status['text']+'\n')
# 	except:
# 		print('failed')
# outfile.close()
# infile.close()


infile = open('dem_tweets.txt', 'r')
text = infile.read()
all_dem_tweets = text.split('\n')
infile.close()


						#=============== Republican Tweets ===================
# infile = open('repub_handles.txt', 'r')
# outfile = open('repub_tweets.txt', 'w')
# text = infile.read()
# handles = text.split(',')
# for handle in handles:
# 	r = oauth.get("https://api.twitter.com/1.1/search/tweets.json?", params = {'q':  handle , 'count':100, 'result_type': 'recent'  })
# 	data = r.json()
# 	try:
# 		for status in data['statuses']:
# 			outfile.write(status['text']+'\n')
# 	except:
# 		print('failed')
# outfile.close()
# infile.close()



infile = open('repub_tweets.txt', 'r')
text = infile.read()
all_repub_tweets = text.split('\n')
infile.close()

#-------------------------------------------STEP 5: CODING-----------------------------------------
#This step takes a keyword from the user and counts the frequency of that keyword among democrat and republican tweets from the cached text files.
lod=[]
dem_total =0
repub_total=0
while True:
	keyword = input("Enter a word you want to search (press q to quit): ")
	if keyword == 'q':
		break
	dic={}
	dem_count=0
	for tweet in all_dem_tweets:
		if keyword.lower() in tweet.lower():
				dem_count+=1
	repub_count=0
	for tweet in all_repub_tweets:
		if keyword.lower() in tweet.lower():
				repub_count+=1
	dem_total+=dem_count
	repub_total+=repub_count
	dic["Keyword"]= keyword
	dic["# Democrat Tweets"] = dem_count
	dic["# Republican Tweets"] = repub_count
	lod.append(dic)
	print("Dem Tweet Count:",dem_count)
	print("Repub Tweet Count:", repub_count)
	print(dem_total)
	print(repub_total)


#-------------------------------------STEP 6: GGPLOT ---------------------------------------
searches = pandas.DataFrame(lod)
if dem_total>repub_total:
	plot =ggplot(searches, aes(x="# Democrat Tweets", y="# Republican Tweets", label="Keyword") ) + geom_text(size=20, color='blue')
else:
	plot =ggplot(searches, aes(x="# Democrat Tweets", y="# Republican Tweets", label="Keyword") ) + geom_text(size=20, color='red')
print(plot)













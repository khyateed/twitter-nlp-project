import re
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
infile = open('dem_handles.txt', 'r')
outfile = open('dem_tweets.txt', 'w')
text = infile.read()
handles = text.split(',')
for handle in handles:
	r = oauth.get("https://api.twitter.com/1.1/search/tweets.json?", params = {'q':  handle , 'count':5, 'result_type': 'popular'  })
	data = r.json()
	try:
		for status in data['statuses']:
			outfile.write(status['text']+'\n')
	except:
		print('failed')
outfile.close()
infile.close()


# infile = open('dem_tweets.txt', 'r')
# text = infile.read()
# all_dem_tweets = text.split('\n')
# infile.close()


						#=============== Republican Tweets ===================
# infile = open('repub_handles.txt', 'r')
# outfile = open('repub_tweets.txt', 'w')
# text = infile.read()
# handles = text.split(',')
# for handle in handles:
# 	r = oauth.get("https://api.twitter.com/1.1/search/tweets.json?", params = {'q':  handle , 'count':5, 'result_type': 'popular'  })
# 	data = r.json()
# 	try:
# 		for status in data['statuses']:
# 			outfile.write(status['text']+'\n')
# 	except:
# 		print('failed')
# outfile.close()
# infile.close()



# infile = open('repub_tweets.txt', 'r')
# text = infile.read()
# all_repub_tweets = text.split('\n')
# infile.close()

#-------------------------------------------STEP 5: CODING-----------------------------------------


# keyword = input("Enter a word you want to search: ")
# dem_count=0
# for tweet in all_dem_tweets:
# 	if keyword.lower() in tweet.lower():
# 		dem_count+=1
# repub_count=0
# for tweet in all_repub_tweets:
# 	if keyword.lower() in tweet.lower():
# 		repub_count+=1

# print("Dem Tweets:",dem_count)
# print("Repub Tweets:", repub_count)











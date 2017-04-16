import re
import json
from bs4 import BeautifulSoup
import requests_oauthlib
key = 'Et4XxRp4SCDn8wS30EKTJuVZf'
secret = 'soFn6mtJXNCBFV0cJMrPBOGROwM798TTVGUSjHBLJCwhiUAbcv'
access_token = '743466833177681922-cRuAJGl4AuO6Wi7PipIiq1ARpBgGeno'
access_secret = 'kBAlSNgRyaEmHZ0yh6ZfEnG2iNO1NLJqTI6LaenKxCfRQ'

# ------------------------------------ STEP 1 -----------------------------------------------
# This step scrapes names of current congress members and appends them to the list, "members"


# base_url = 'https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress'
# r = requests.get(base_url)
# outfile = open('step1.html', 'w', encoding="utf-8")
# outfile.write(r.text)
# outfile.close()
					

members=[]
lis=[]

r = open('step1.html','r')
soup = BeautifulSoup(r, "html.parser")
table = soup.table.find_all('tr')
for person in table:
    tups=[]
    lis = person.text.split('\n')
    if len(lis)>2:
    	tups.append((lis[1], lis[2]))
    	members.append(tups)

#--------------------------------------- STEP 2 ------------------------------------
# this step splits members into two lists: democrats and republicans.






#------------------------------------------ STEP 3 ---------------------------------
# This step searches twitter api for the names and retrieves a twitter handle, writing it to the file "usernames.txt"


oauth = requests_oauthlib.OAuth1Session(key,
                        client_secret= secret,
                        resource_owner_key= access_token,
                        resource_owner_secret=access_secret)


# t = open('usernames.txt', 'w')
# for name in members:
# 	r = oauth.get("https://api.twitter.com/1.1/users/search.json?", params = {'q': name, 'count': 1})
# 	data =r.json()
# 	for dic in data:
# 		print(dic['screen_name'])
# 		t.write(dic['screen_name'])
# 		t.write(',')
# t.close()


# ------------------------------------------ STEP 4 ---------------------------------------

# t = open('usernames.txt', 'r')
# text = t.read()
# handles = text.split(',')
# handle = handles[3]
# r = oauth.get("https://api.twitter.com/1.1/search/tweets.json?", params = {'q':  handle , 'count':5, 'result_type': 'popular'  })
# print(r.json())


# get top hashtags per person
# distinguish democrats and republicans



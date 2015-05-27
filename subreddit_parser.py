#!/usr/bin/python
#TO DO:
#tackle the ?=1 suffix
#dates of various directories 

import praw
from datetime import date
from bs4 import BeautifulSoup
import requests
import os, sys, re, math, random, time 
import urllib

#preliminary login
user_agent = ("Anon_is_Browser")
r = praw.Reddit(user_agent=user_agent)
lmts = 100
user_name = "Some_user_id"
user_passwd = "Some_password"
r.login(user_name,user_passwd)
#eg, gifs, photoshopbattles, pics
subwords = ['gifs','pics','WarriorWomen']

#directory creation 
def directory_create(linker):
    dir0 = os.environ['HOME']
    return dir0+'/.reddit/'+linker.split('/')[-1]+'/'

extn2 = []
extn = ['jpg','jpeg','png','gif']
for i in extn:
    extn2.append(i.upper())
extns = extn + extn2

#submissions =  r.get_subreddit('suicidegirls').get_hot(limit=lmts)
def extractlink(submissions):
    links = []
    for submission in submissions:
        time.sleep(random.randint(0,5))
        if submission.url.split('.')[-1] in extns:  
            links.append(submission.url)
        else:
            htmlurl = requests.get(submission.url).text
            url = BeautifulSoup(htmlurl)
            if url.title is None:
               continue
            #print ('Album : {} \n'.format(url.title.string.encode('utf-8')))
            print (url.title)
            for image in url.find_all('a'):
                imageurl = image.get('href')
                if imageurl != None and imageurl.split('.')[-1] in extns:
                    if imageurl.startswith('http') or imageurl.startswith('www'):
                        links.append(imageurl)
                    else:
                        links.append('http:'+imageurl)      
    return links


def imageget(imglink,dldir):
    fn0 = imglink.split('/')[-1]
    flname = os.path.join(dir0,fn0)
    fout = open("flname","wb")
    fout.write(urllib.urlopen(imglink).read())
    fout.close() 

for subword in subwords:
    submit = r.get_subreddit(subword).get_hot(limit=lmts)
    #[print(subword ,":" ,x,"\n") for x in submit]
    sublinks = []
    sublinks = extractlink(submit)    
    vstr = str(date.today())
    dir0 = os.environ['HOME']+'/.reddit/'+subword+'/'+vstr
    if os.path.exists(dir0):
        pass
    else:
        os.mkdir(dir0)
    for sublink in sublinks:
        #osInput = 'wget -q '+sublink +' -P '+dir0  
        #os.system(osInput)  
	imageget(sublink,dir0)  
    print() 

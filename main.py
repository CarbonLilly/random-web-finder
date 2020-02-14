'''
Created on Feb 14, 2020

@author: Homeu
'''

from selenium import webdriver
from random import randint
import os
#URL-ify function
import sys


#domain to search
print("Beginning pre-initialization!")
domain = input("Please type the domain you want to search (ex: '.com' without quotes)\n Defaults to .com!:")
if domain is None or domain == "":
    domain = ".com"





def urlify(wordlist,domain):
    
    word = wordlist[randint(0,len(wordlist)-1)]
    
    url = "https://"+word+domain
    
    
    return url, word
def checklist(word,list):
    print("Checking against blacklist for word '"+word+"' ...")
    if word in list:
        print("Word found!")
        return True
    else:
        print("Word not found!")
        return False

#load word list
print ("Loading word list...")
#Reworked to read all ".txt" files from a directory!
wordlist = []
directory = sys.path[0] + r"\wordlists"



for entry in os.scandir(directory):
    if entry.path.endswith(".txt"):
        with open(entry.path,"r") as wordfile:
            wordlist.extend(wordfile.readlines())
            print("Found list "+entry.path)


print("Word list loaded!")


print("Initializing driver!")
driver = webdriver.Firefox()
print("Done!")
print("Entering main loop...")
while True:
    badwords = []
    print("Reloading blacklist")
    try:
        with open(("blacklist"+domain+".txt"),'r') as blacklist:
            badwords = blacklist.readlines()
    except:
        print("Blacklist not made for this domain!")
    while True:
        url, word = urlify(wordlist,domain)
        if not checklist(word,badwords):
            break
        else:
            print("Tried to use blacklisted word "+word+"!!")
    
    try:
        driver.get(url)
        cancel = input("'c' = cancel | 'b' = blacklist | ' ' = continue ")
        if cancel == 'c':
            break
        elif cancel == 'b':
            print("Blacklisting!!")
            with open(("blacklist"+domain+".txt"),'a') as blacklist:
                blacklist.write(word)
                
        elif cancel == 's':
            with open("strangewebsites.txt",'a') as webs:
                webs.write(word+domain)
                
    except:
        print(word+" didn't yield a valid URL!")
        print(word+" has been blacklisted!")
        with open(("blacklist"+domain+".txt"),'a') as blacklist:
            blacklist.write(word)
            
driver.close()



import requests
from bs4 import BeautifulSoup
#from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk import pos_tag
import nltk
from bs4.element import Comment
import urllib2
import os

link = "http://www.du.ac.in/du/index.php?page=libraries"

def tag_visible(element):
	if element.parent.name in ['style' , 'script' , 'meta' , '[document]']:
		return False
	if isinstance(element,Comment):
		return False
	return True
html = requests.get(link).text
soup = BeautifulSoup(html, "lxml")
#print soup
#soup = soup.get_text()
data=soup.findAll(text=True)
#print data

text=filter(tag_visible,data)
#print text
print(u" ".join(t.encode('ascii','ignore').decode('ascii').strip() for t in text))

file=open("file1.txt","w")
file.write(u" ".join(t.encode('ascii','ignore').decode('ascii').strip() for t in text))

corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader(".", "file1.txt")

paragraphs=corpus.paras()

sentences=corpus.sents()

words=corpus.words()

for p in paragraphs:
	print p 

for s in sentences:
	print s

for w in words:
	print w
		
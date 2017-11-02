#import requests
import urllib
from bs4 import BeautifulSoup
import HTMLParser
import math
import string
from bs4.element import Comment


page_links =[]
data =[]
def url_open(url):
  #request = urllib.Request(url)
  f = urllib.urlopen(url)  
  html = f.read().decode("utf-8").encode("cp850","replace").decode("cp850")
  soup = BeautifulSoup(html,"html5lib")
  return soup
url ='http://www.du.ac.in/du/index.php?page=libraries'
soup=url_open(url)

for text in soup.find_all("div",attrs={"id":"menuwrapper"}):
  for x in text.find_all('a'):
    full_link = x.get("href")
    if full_link.find('page')>0 or full_link.find('tutorial')>0:
    	#print(full_link)
    	page_links.append(full_link)

page_links.append(url)    	
print(page_links)
def tag_visible(element):
	if element.parent.name in ['style' , 'script' , 'meta' , '[document]']:
		return False
	if isinstance(element,Comment):
		return False
	return True
 
for link in page_links:
          if link.find("page")>0:
                  soup = url_open(str(link))
                  table = soup.find_all('div',attrs={"class":"content-inner grid_9 push_3"})
                  #text=filter(tag_visible,table)
                  for x in table:
                          string = x.text.encode('utf-8')
                          data.append(''.join( c for c in string if  c not in '\n\t\xa9'))
                  
	      
#print data
#print type(data)     
#remove stopwords
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
str1 = ''.join(str(e) for e in data)
#print type(str1)
import ast
tokens= word_tokenize(str1.decode('utf-8'))
filtered_words = [w for w in tokens if not w in stopwords.words('english')]
print filtered_words



#calculate tf-idf matrix
tokenize = lambda doc: doc.lower().split(" ")

def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents






tfidf_representation = tfidf(data)
#print tfidf_representation


#cosine similarity

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude
  
our_tfidf_comparisons = []
for count_0, doc_0 in enumerate(tfidf_representation):
    for count_1, doc_1 in enumerate(tfidf_representation):
        our_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), count_0, count_1))


print our_tfidf_comparisons

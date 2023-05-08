import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# set the website URL to crawl
url = "https://nettrakett.no/sokemotoroptimalisering-seo/"


# include regular text content
include_content = False
 
# send a GET request to the website's homepage
response = requests.get(url)
 
# parse the HTML code using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
 
# extract the text content of the webpage and split it into words
if include_content == True:
    text = soup.get_text()
else:
    text = ""
 
# get the meta title and add it to the text content
meta_title = soup.find("meta", {"name": "title"})
if meta_title:
    text += meta_title["content"] + " "
else:
    meta_title = soup.find("meta", {"property": "og:title"})
    if meta_title:
        text += meta_title["content"] + " "
 
 
 
# get the meta description and add it to the text content
meta_description = soup.find("meta", {"name": "description"})
if meta_description:
    text += meta_description["content"] + " "
 
 
# get all the headings (h1-h6) and add them to the text content
headings = soup.find_all(re.compile(r'h[1-6]'))
for heading in headings:
    text += heading.get_text() + " "
 
 
# split the text content into words
words = re.findall('\w+', text.lower())
 
# remove stopwords
stop_words = set(stopwords.words('norwegian'))
filtered_words = [word for word in words if not word in stop_words]
 
# count the frequency of each word using a Python dictionary
word_counts = Counter(filtered_words)
 
# sort the dictionary by frequency in descending order
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
 
# output the top 10 words with the highest frequency
n = 10
keyword_texts = [word[0] for word in sorted_words[:n]]
print("potential focus keywords for SEO:", keyword_texts)

with open('keywords.txt', 'w', encoding='utf-8') as f:
    for line in filtered_words:
        f.write(line)
        f.write('\n')

    #Open the text file and read its contents into a list of words
with open('keywords.txt', 'r') as f:
    words = f.read().split()
#Use a regular expression to remove any non-alphabetic characters from the words
words = [re.sub(r'[^a-zA-Z]', '', word) for word in words]
#Initialize empty dictionaries for storing the unigrams, bigrams, and trigrams
unigrams = {}
bigrams = {}
trigrams = {}
#Iterate through the list of words and count the number of occurrences of each unigram, bigram, and trigram
for i in range(len(words)):
    # Unigrams
    if words[i] in unigrams:
        unigrams[words[i]] += 1
    else:
        unigrams[words[i]] = 1
        
    # Bigrams
    if i < len(words)-1:
        bigram = words[i] + ' ' + words[i+1]
        if bigram in bigrams:
            bigrams[bigram] += 1
        else:
            bigrams[bigram] = 1
        
    # Trigrams
    if i < len(words)-2:
        trigram = words[i] + ' ' + words[i+1] + ' ' + words[i+2]
        if trigram in trigrams:
            trigrams[trigram] += 1
        else:
            trigrams[trigram] = 1
# Sort the dictionaries by the number of occurrences
sorted_unigrams = sorted(unigrams.items(), key=lambda x: x[1], reverse=True)
sorted_bigrams = sorted(bigrams.items(), key=lambda x: x[1], reverse=True)
sorted_trigrams = sorted(trigrams.items(), key=lambda x: x[1], reverse=True)
# Write the results to a text file
with open('results.txt', 'w') as f:
    f.write("Most common unigrams:\n")
    for unigram, count in sorted_unigrams[:10]:
        f.write(unigram + ": " + str(count) + "\n")
    f.write("\nMost common bigrams:\n")
    for bigram, count in sorted_bigrams[:10]:
        f.write(bigram + ": " + str(count) + "\n")
    f.write("\nMost common trigrams:\n")
    for trigram, count in sorted_trigrams[:10]:
        f.write(trigram + ": " + str(count) + "\n")


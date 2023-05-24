import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pytrends.request import TrendReq
import pandas as pd
import json


# set the website URL to crawl
url = ""

# optional list of keywords to research instead of crawling website
keyword_list = ['visuell identitet', 'branding', 'grafisk profil']

common_keywords = []
 
if url:


    # include regular text content
    include_content = True

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
    filtered_words = [word for word in words if not word in stop_words and len(word) > 4]

    # count the frequency of each word using a Python dictionary
    word_counts = Counter(filtered_words)

    # sort the dictionary by frequency in descending order
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # output the top 10 words with the highest frequency
    n = 10
    common_keywords = [word[0] for word in sorted_words[:n]]
    print("potential keywords for SEO:", common_keywords)

    df = pd.DataFrame(sorted_words, columns =['Keyword', 'Count'])
    df.to_excel('keywords.xlsx', index=False)   

    with open('keywords.txt', 'w', encoding='utf-8') as f:
        for line in filtered_words:
            f.write(line)
            f.write('\n')


        #Open the text file and read its contents into a list of words
    with open('keywords.txt', 'r') as f:
        words = f.read().split()

    #Use a regular expression to remove any non-alphabetic characters from the words
    # words = [re.sub(r'[^a-zA-Z]', '', word) for word in words]

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
    with open('grams.txt', 'w') as f:
        f.write("Most common unigrams:\n")
        for unigram, count in sorted_unigrams[:10]:
            f.write(unigram + ": " + str(count) + "\n")
        f.write("\nMost common bigrams:\n")
        for bigram, count in sorted_bigrams[:10]:
            f.write(bigram + ": " + str(count) + "\n")
        f.write("\nMost common trigrams:\n")
        for trigram, count in sorted_trigrams[:10]:
            f.write(trigram + ": " + str(count) + "\n")


common_keywords.extend(keyword_list)

# def get_autocomplete_suggestions(keyword):
#     suggestions = search(keyword, num_results=10, lang="no")
#     return suggestions

def get_related_queries(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='NO', gprop='')
    related_queries = pytrends.related_queries()
    if related_queries.get(keyword):
        return related_queries[keyword]['top']
    return None

def get_suggestions(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo='NO', gprop='')
    suggestions = pytrends.suggestions(keyword)
    if suggestions:
        return suggestions
    return None

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def get_autocomplete_suggestions(keyword):
    response = requests.get(f'http://google.com/complete/search?client=chrome&q={keyword}', headers=headers)
    suggestions = json.loads(response.text)[1]
    return suggestions

# google_autocomplete_suggestions = {}
pytrends_related_queries = {}
pytrends_suggestions = {}
autocomplete_suggestions = {}

for keyword in common_keywords:
    pytrends_related_queries[keyword] = get_related_queries(keyword) 
    pytrends_suggestions[keyword] = get_suggestions(keyword) 
    autocomplete_suggestions[keyword] = get_autocomplete_suggestions(keyword)

# # Convert the generators in google_autocomplete_suggestions to lists
# google_autocomplete_suggestions = {k: pd.DataFrame(v, columns=[k]) for k, v in google_autocomplete_suggestions.items()}

# # Concatenate the DataFrames along the column axis
# df = pd.concat(google_autocomplete_suggestions.values(), axis=1)
# df.to_excel('google_autocomplete_suggestions.xlsx', index=False)


# Flatten the pytrends suggestions dict into a list
list_of_dicts = []
for key, values in pytrends_suggestions.items():
    if values is not None:
        for value in values:
            value['key'] = key  # Add the original key into the dict
            list_of_dicts.append(value)

# Convert the list into a DataFrame, and then an excel file
df = pd.DataFrame.from_records(list_of_dicts)
df.to_excel('pytrends_keyword_suggestions.xlsx', index=False)

# Flatten the autocomplete suggestions and convert it to a DataFrame
rows = [(key, value) for key in autocomplete_suggestions for value in autocomplete_suggestions[key]]
df = pd.DataFrame(rows, columns=['Keyword', 'Suggestion'])
# Save the DataFrame to an Excel file
df.to_excel('autocomplete_suggestions.xlsx', index=False)

# with open('google_autocomplete.txt', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(google_autocomplete_suggestions))
try:
    df = pd.concat(pytrends_related_queries.values(), axis=1)
    df.to_excel('pytrends_related_queries.xlsx', index=False)
except ValueError:
    print("no related queries found")

# with open('pytrends_suggestions.txt', 'w', encoding='utf-8') as f:
#     f.write(json.dumps(pytrends_suggestions))




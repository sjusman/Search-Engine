# Search-Engine
Create a complete search engine by building search index off of crawled data that includes downloaded content of UCI's ICS web pages

buildIndexUpdated.py is designed to create the inverted index after tokenizing and stemming text using NLTK RegExpTokenizer and NLTK PorterStemmer
corpus.py is responsible for handling corpus related functionalities such as mapping a URL to its local file name 
gui.py is the GUI for the search engine that loads search.ui
invertedindex.json is the result of creating the inverted index using functions in buildIndexUpdated.py
length_dict.json stores the information of how many words there is in a corpus
main.py is the main file that creates corpus, creates the index, executes page ranking and tests some queries 
pageranking.py handles ranking the top results of a query by using TF-IDF
result.ui
search.ui
bookkeeping.json maintains the list of all URLs that have been crawled
WEBPAGES_RAW_ZIP contains the downloaded content of the ICS web pages

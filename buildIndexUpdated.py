from collections import defaultdict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
import json
import os
import lxml
import unicodedata
import math
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.stem import *
import json

# The corpus directory name
WEBPAGES_RAW_NAME = "WEBPAGES_RAW2"
# The corpus JSON mapping file
JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping2.json")

class invertedIndex:
    '''
    This class is designed to create our inverted index in the following format:
    {'token': {docID: tf}} where...
    token = the tokenized and stemmed word collected from the file.
    docID = folder/file name in WEBPAGES_RAW
    tf = term frequency in the document.
    Run this once to create the inverted index.
    '''
    def __init__(self, corpus):
        '''
        Initialize the class variables.
        corpus = dictionary with url and file location
        json_file = json file containing URL/doc ID (bookkeeping.json in our case)
        self.corpus = corpus counter to make sure we are iterating through all files.
        '''
        self.corpus = corpus
        self.words = {}
        self.length_dict = {}
        self.all_files = []

    def tokenize_file(self, doc):
        '''
        Opens the document, tokenizes and stems text, creates a
        dictionary in the following format:
        {token: {docID: token_freq}}.
        To gather text from file we used BeautifulSoup.
        To tokenize the file we used nltk RegexpTokenizer.
        To stem words we used nltk PortStemmer.
        '''
        #opening, reading, and closing file
        file = open(os.path.join(".", WEBPAGES_RAW_NAME, doc), encoding='utf8')
        data = file.read()
        file.close()

        #creating objects to help read, tokenize, and stem the words
        bs = BeautifulSoup(data,"lxml")
        #separate a sentence into words without punctuation using r'\w+'
        tokenizer = RegexpTokenizer(r'\w+')
        #create stemmer to remove morphological affixes from words, leaving only word stem
        stemmer = PorterStemmer()

        #initializing local variables
        tag_text = ""
        tokens = {}
        tags = ["html"]
        word_list = []
        word_counter = 0
        token_dict = {}

        #retrieveing text, tokeninzing/stemming text
        tag_text = u' '.join([i.text for i in bs.find_all("html")])
        word_list = tokenizer.tokenize(",".join([stemmer.stem(tt) for tt in tag_text.split(" ")]))

        #adding each word into the inverted index.
        #for each posting, include (docID: tf)
        for word in word_list:  
            if word not in self.words.keys():
                self.words[word] = {}
                self.words[word][doc] = 1
            else:
                if doc not in self.words[word].keys():
                    self.words[word][doc] = 1
                else:
                    self.words[word][doc]+=1
            word_counter += 1
            
        self.length_dict[doc] = word_counter

        return self.words

    def create_index(self):
        for file in self.corpus:
            self.tokenize_file(file)
        self.dump_data('invertedIndex')
        print("Inverted index dumped into json file")
        self.dump_data('length_dict')
        print("Length dict dumped into json file")
        print("Documents iterated:", len(self.corpus))

    def dump_data(self, output_file):
        with open(output_file, 'w') as outfile:
            json.dump(self.words, outfile)


    def get_length_dict(self):
        '''
        Returns the dictionary containing the number of words in each document.
        '''
        return self.length_dict

    



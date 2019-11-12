from collections import defaultdict
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
import os
import lxml
import unicodedata
import math
from nltk.tokenize import RegexpTokenizer
import nltk
from nltk.stem import *
from math import *

#import buildIndex

WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")


class pageRanking:
    '''
    This class handles ranking the top results.
    '''

    def __init__(self):
        '''
        Open both invertindex.json and length_dict.json adn store into class variables.
        The two files were dumped using PickleDump after creating the index (in invertedIndex class).
        '''
        with open('invertedindex.json') as json_file:
            self.invertedIndex = json.load(json_file)
        self.corpus = 0
        with open('length_dict.json') as json_file2:
            self.length_dict = json.load(json_file2)
        self.tf_dict = {}

    def read_file(self):
        with open(JSON_FILE_NAME) as f:
            try:
                data = json.load(f)
            except ValueError:
                    data = {}
        for file in data:
            self.corpus += 1
    
    def stem_query(self, q):
        '''
        Stems the query, returns stemmed query.
        '''
        stemmer = PorterStemmer()
        stem = stemmer.stem(q)
        return stem

    def normalize_tf(self, stemmed_query):
        '''
        Normalizes the term frequency using the following formula:
            # of occurences in doc
            ----------------------
            # of words in doc
        '''
        tf_dict = {}
        for term in self.invertedIndex:
            if stemmed_query == term:
                tf_dict[stemmed_query] = {}
                for doc in self.invertedIndex[term].keys():
                    tf_dict[stemmed_query][doc] = self.invertedIndex[stemmed_query][doc] / self.length_dict[doc]

        return tf_dict

    def calculate_tfidf(self, stemmed_query):
        '''
        Calculate tf-idf using the following formula:
            tf*idf
        To get idf we did the following:
            length of corpus
            ----------------
            '''
        tf_idf_dict = {}
        tf = self.normalize_tf(stemmed_query)
        for doc in tf[stemmed_query]:
            idf = self.corpus / len(self.invertedIndex[stemmed_query])
            tf_idf = idf * tf[stemmed_query][doc]
            tf_idf_dict[doc] = tf_idf
        return tf_idf_dict
    
    def top_ranking_pages(self, q):
        top_pages = []
        stemmed = self.stem_query(q)
        result = self.calculate_tfidf(stemmed)
        sorted_result = sorted(result, key = result.get, reverse = True)
        for doc in sorted_result[:20]:
            top_pages.append(doc)
        return top_pages

    def get_query(self, q):
        query = q.split(" ")
        for q in query:
            if q not in self.invertedIndex:
                return []
        if len(query) == 1:
            return self.top_ranking_pages(query[0])
        if len(query) == 2:
            top_pages = []
            combined_tfidf ={}
            word1 = query[0]
            word2 = query[1]
            word1_tfidf = self.calculate_tfidf(self.stem_query(word1))
            word2_tfidf = self.calculate_tfidf(self.stem_query(word2))
            
            for doc in word1_tfidf:
                if doc in word2_tfidf:
                    combined_tfidf[doc] = (word1_tfidf[doc] + word2_tfidf[doc])*100
                else:
                    combined_tfidf[doc] = word1_tfidf[doc]
            for doc in word2_tfidf:
                if doc not in combined_tfidf:
                    combined_tfidf[doc] = word2_tfidf[doc]
            sorted_result = sorted(combined_tfidf, key = combined_tfidf.get, reverse = True)
            for doc in sorted_result[:20]:
                top_pages.append(doc)

        return top_pages


    def get_top_urls(self, top_pages, corpus):
        '''
        Returns the URLs for the top ranked pages (instead of the docID) in a list.
        top_pages = list of the top_pages docIDs
        url_file_map = dictionary with url mapped to docID
        '''
        top_urls = {}
        
        for page in top_pages:
            url = corpus.get_file_url_map()[page]
            file = open(os.path.join(".", "WEBPAGES_RAW", page), encoding='utf8')
            data = file.read()
            bs = BeautifulSoup(data, "lxml")
            snippet = u' '.join([i.text for i in bs.find_all("title")])
            if (snippet == ""):
                snippet = "Untitled page"
            #print(page, snippet)
            top_urls[page] = (url, snippet)

        #print(top_urls)
        return top_urls

    def format_top_urls(self, top_urls):
        result = ""
        count = 1
        hyperlink_format = '<a href="{link}">{text}</a>'
        for doc in top_urls:
            hyperlink = hyperlink_format.format(link=top_urls[doc][0], text=top_urls[doc][0])
            result += '{n}. {url}<br>{snippet}<br><br>'.format(n=count, url=hyperlink, snippet=top_urls[doc][1])
            count += 1
        #print(result)
        return result

    def print_list(self, top_urls):
        '''
        Used to format list for printing the test output file.
        '''
        result = ""
        counter = 1
        for n in top_urls:
            result += '{n}. {url}\n'.format(n=counter, url=top_urls[n][0])
            counter += 1
        return result
            

    def print_output(self, corpus):
        results = ""
        f = open('output.txt', 'w+')
        index_size = str(round(os.path.getsize('invertedindex.json')/1024)) + " KB"
        results1 = "Number of documents: " + str(self.corpus) + "\nNumber of unique words: " + str(len(self.invertedIndex)) + "\nInverted Index size on disk: " + index_size 

        # used for formatting
        n1 = len(set(self.invertedIndex[self.stem_query("Informatics")].keys()))
        top1 = self.print_list(self.get_top_urls(self.get_query("Informatics"), corpus))
        n2 = len(set(self.invertedIndex[self.stem_query("Mondego")]))
        top2 = self.print_list(self.get_top_urls(self.get_query("Mondego"), corpus))
        n3 = len(set(self.invertedIndex[self.stem_query("Irvine")]))
        top3 = self.print_list(self.get_top_urls(self.get_query("Irvine"), corpus))
        n4 = len((set(self.invertedIndex[self.stem_query('artificial')].keys())).union(set(self.invertedIndex[self.stem_query("intelligence")].keys())))
        top4 = self.print_list(self.get_top_urls(self.get_query("artifical intelligence"), corpus))
        n5 = len((set(self.invertedIndex[self.stem_query('computer')].keys())).union(set(self.invertedIndex[self.stem_query("science")].keys())))
        top5 = self.print_list(self.get_top_urls(self.get_query("computer science"), corpus))
        results2 = 'Informatics = {n1} URLs\n{top1}\n\nMondego = {n2} URLs\n{top2}\n\nIrvine = {n3} URLS\n{top3}\n\nartificial intelligence = {n4} URLs\n{top4}\n\ncomputer science = {n5} URLs\n{top5}'.format(
            n1=n1, top1=top1, n2=n2, top2=top2, n3=n3, top3=top3, n4=n4, top4=top4, n5=n5, top5=top5)

        results += results1 + '\n' + results2

        f.write(results)
        f.close()
            
   
        
                              
        

        



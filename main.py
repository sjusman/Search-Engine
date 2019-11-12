from corpus import Corpus
from buildIndexUpdated import invertedIndex
from pageranking import pageRanking

def main():
    '''
    Main function of Project 3
    '''
    #create corpus
    corpus = Corpus()
    
    #local variables
    #urls = corpus.get_url_list()
    corpus_docIDs = corpus.get_docID_list()

    #creating index
    #inverted_index = invertedIndex(corpus_docIDs)
    #inverted_index.create_index()

    #query and ranking
    fileRanking = pageRanking()
    fileRanking.read_file()
    top_docs = fileRanking.get_query("artficial intelligence")
    top_urls = fileRanking.get_top_urls(top_docs, corpus)
    fileRanking.format_top_urls(top_urls)
    fileRanking.print_output(corpus)
    

main()

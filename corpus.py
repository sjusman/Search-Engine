import json
import os
from urllib.parse import urlparse

class Corpus:
    """
    This class is responsible for handling corpus related functionalities like mapping a url to its local file name
    """

    # The corpus directory name
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    # The corpus JSON mapping file
    JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")

    def __init__(self):
        self.file_url_map = json.load(open(self.JSON_FILE_NAME), encoding="utf-8")
        self.url_file_map = dict()
        for key in self.file_url_map:
            self.url_file_map[self.file_url_map[key]] = key
            


    def get_file_name(self, url):
        """
        Given a url, this method looks up for a local file in the corpus and, if existed, returns the file address. Otherwise
        returns None
        """
        url = url.strip()
        parsed_url = urlparse(url)
        url = url[len(parsed_url.scheme) + 3:]
        if url in self.url_file_map:
            addr = self.url_file_map[url].split("/")
            dir = addr[0]
            file = addr[1]
            return os.path.join(".", self.WEBPAGES_RAW_NAME, dir, file)
        return None

    def get_url_map(self):
        '''
        Returns self.url_file_map
        '''
        return self.url_file_map


    def get_url_list(self):
        '''
        Returns list of urls from url_file_map
        '''
        return list(self.url_file_map.keys())

    def get_docID_list(self):
        '''
        Return list of docIDs from url_file_map
        '''
        return list(self.url_file_map.values())

    def get_file_url_map(self):
        return self.file_url_map


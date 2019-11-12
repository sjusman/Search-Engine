import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from pageranking import pageRanking
from corpus import Corpus
from buildIndexUpdated import invertedIndex
    
class SearchEngine(QDialog):
    def __init__(self):
        super(SearchEngine,self).__init__()
        loadUi('search.ui', self)
        self.setWindowTitle('Search Engine')
        self.searchBtn.clicked.connect(self.on_searchBtn_clicked)
        
    @pyqtSlot()    
    def on_searchBtn_clicked(self):
        self.query = self.lineEdit.text()
        if self.query == "":
            display_text = "No results for a blank query"
        elif len(fileRanking.get_query(self.query)) == 0:
            display_text = "No results found."
        else:
            top_docs = fileRanking.get_query(self.query)
            display_text = fileRanking.format_top_urls(fileRanking.get_top_urls(top_docs, corpus))
        self.textBrowser.setText(display_text)
        
if __name__ == '__main__':
    corpus = Corpus()
    corpus_docIDs = corpus.get_docID_list()
    fileRanking = pageRanking()
    fileRanking.read_file()
    app = QApplication(sys.argv)
    widget = SearchEngine()
    widget.show()
    sys.exit(app.exec_())

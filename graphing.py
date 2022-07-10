from operator import truediv
from qtstrap import *
from parser import Parser
from PySide2.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objects import Figure, Pie
import plotly


class Graph(QWebEngineView):
    
    infile_changed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAcceptDrops(True)
        self.parser = Parser()
        self.html = ''
        self._update_graph()

    def _update_data(self, infile):
        self.parser.infile = infile
        self.parser.load_html()
        self.parser.parse_data()

    def _update_graph(self):
        self.html = "<html><body>" 

        if self.parser.infile:
            graph_data = self.parser.data['categories']
            labels = list(graph_data.keys())
            values = list(graph_data.values())

            fig = Figure(data=[Pie(labels=labels, values=values)])

            self.html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn') 
            # TODO: offline include_plotlyjs values don't seem to work. 'cdn' requires an internet connection. 

        self.html += '</body></html>'
        self.setHtml(self.html)

    def update(self, infile):
        self._update_data(infile)
        self._update_graph()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            fname = event.mimeData().urls()[0].url()
            infile = fname.replace('file://', '')
            self.infile_changed.emit(infile)
            self.update(infile)
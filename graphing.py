from qtstrap import *
from bs4 import BeautifulSoup
from parser import Parser
from PySide2.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objects import Figure, Pie
import plotly


class BaseEngineView(QWebEngineView):

    infile_changed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setMinimumHeight(675)
    
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


class FileViewer(BaseEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html = ''

    def update(self, infile):
        with open(infile) as file:
            soup = BeautifulSoup(file, 'html.parser')
            self.html = str(soup)
            self.setHtml(self.html)
        

class PieChart(BaseEngineView):
    
    from piechart import parse
    parser = Parser(parse)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._update_graph()

    def _update_data(self, infile):
        self.parser.infile = infile
        self.parser.load_html()

    def _update_graph(self):
        self.html = '<html><body>' 

        if self.parser.infile:

            labels = self.parser.data['labels']
            values = self.parser.data['values']
            text = self.parser.data['text']
            title = self.parser.data['title']

            self.fig = Figure([Pie(labels=labels, values=values, text=text, textfont_size=12,textposition='outside')])
            self.fig.update_layout(title=title, 
                                   font=dict(size=10), 
                                   legend=dict(orientation='h',
                                   yanchor="top", 
                                   xanchor="right"))
            self.fig.update_traces(hovertemplate="%{label}<br>%{value} pts<extra></extra>")

            self.html += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn') 

        self.html += '</body></html>'
        self.setHtml(self.html)

    def save_image(self, fname):
        if self.fig:
            self.fig.write_image(f'temp/{fname}')

    def update(self, infile):
        self._update_data(infile)
        self._update_graph()


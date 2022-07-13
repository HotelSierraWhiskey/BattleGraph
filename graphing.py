from operator import truediv
from qtstrap import *
from parser import Parser
from PySide2.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objects import Figure, Pie
import plotly



class BaseGraph(QWebEngineView):

    infile_changed = Signal(str)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
    
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


class PieChart(BaseGraph):
    
    from piechart import parse
    parser = Parser(parse)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setMinimumHeight(675)
        self.setAcceptDrops(True)
        self._update_graph()

    def _update_data(self, infile):
        self.parser.infile = infile
        self.parser.load_html()

    def _update_graph(self):
        self.html = '<html><body>' 

        if self.parser.infile:
            labels = list(self.parser.data['categories'].keys())
            values = []
            text = []
            for i in labels:
                values.append(self.parser.data['categories'][i]['pts'])
                text.append(self.parser.data['categories'][i]['units'])

            title = self.parser.data['title']

            pie = Pie(labels=labels, values=values, text=text, textfont_size=12, textposition='outside')

            self.fig = Figure([pie])
            self.fig.update_layout(title=title, font=dict(size=10), legend=dict(orientation='h', yanchor="top", xanchor="right"))

            self.html += plotly.offline.plot(self.fig, output_type='div', include_plotlyjs='cdn') 

            # TODO: other include_plotlyjs values don't seem to work. 'cdn' works but requires an internet connection.
            # the html produced by offline options (when output_type='file') will render plotly graphs 
            # when loaded by a browser, but will fail to load in a QWebEngine. Or something. 

        self.html += '</body></html>'
        self.setHtml(self.html)

    def save_image(self, fname):
        if self.fig:
            self.fig.write_image(f'temp/{fname}')

    def update(self, infile):
        self._update_data(infile)
        self._update_graph()



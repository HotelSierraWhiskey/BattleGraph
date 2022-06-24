from qtstrap import *
from parser import Parser
from PySide2.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objects import Figure, Pie
import plotly
import plotly.express as px

import pandas as pd

import numpy as np


class Graph(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser = Parser()

        self.fig = None

        self.html = ''

        self.update_graph()

        self.setHtml(self.html)

    def update_data(self, infile):
        self.parser.infile = infile
        self.parser.load_html()
        self.parser.parse_data()

    def update_graph(self):
        self.html = '<html><body>'

        if self.parser.infile:
            graph_data = self.parser.data['categories']
            labels = list(graph_data.keys())
            values = list(graph_data.values())

            fig = Figure(data=[Pie(labels=labels, values=values)])

            self.html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')

        self.html += '</body></html>'

        self.setHtml(self.html)

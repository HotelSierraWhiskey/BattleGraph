from qtstrap import *
from PySide2.QtWebEngineWidgets import QWebEngineView
from plotly.graph_objects import Figure, Scatter
import plotly

import numpy as np


class Graph(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        x = np.arange(1000)
        y = x**2

        fig = Figure(Scatter(x=x, y=y))

        html = '<html><body>'
        html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
        html += '</body></html>'

        self.setHtml(html)
"""
Jiajie Lin
 DS 3500 Box and Whisker
"""

import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import matplotlib.pyplot as plt

pio.renderers.default = 'browser'

def make_box_and_whisker(data):
    fig, ax = plt.subplots()
    ax.boxplot(data)

    return fig


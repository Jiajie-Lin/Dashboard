"""
Jiajie Lin
Homework 3
Description: Make a simple easy to use dashboard
"""
import panel as pn

from homework3_api import LeagueAPI
import sankey as sk
import pandas as pd
import matplotlib.pyplot as plt


# Loads javascript dependencies and configures Panel (required)
pn.extension()


# Initialize the API!
api = LeagueAPI()
api.load_league("cleaned_league.csv")

#dataset
data_set = pd.read_csv('cleaned_league.csv')

# WIDGET DECLARATIONS
switch = pn.widgets.Switch(name='Wins')
radio_group = pn.widgets.RadioButtonGroup(
    name = 'Radio Button', options = ['Win', 'Loss'], value ='Win', button_type = 'success')


# Search Widgets

#Button Widget


# Plotting widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1000)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=600)

# CALLBACK FUNCTIONS
def getplot(tier,action,width,height):
    local = api.extract_local_network(tier,action)
    fig =  sk.make_sankey(local,tier,action,vals='player_count', width = width, height = height)
    return fig

def bk(action):
    local = api.bk(action)
    return local

# CALLBACK BINDINGS (Connecting widgets to callback functions)

    #sankey
plot = pn.bind(getplot,'tier', 'losses_SD', width= width, height= height)
plot2 = pn.bind(getplot,'tier', 'wins_SD', width = width, height = height)

    #box and whisker
plot3 = pn.bind(bk,'wins')
plot4 = pn.bind(bk,'losses')

def switch_plot(win_status):
    if win_status == 'Win':
        return plot2
    else:
        return plot


dynamic_plot = pn.bind(switch_plot, win_status=radio_group)

def switch_plot_box_whisker(win_status):
    if win_status == 'Win':
        return plot3
    else:
        return plot4

dynamic_box_whisker = pn.bind(switch_plot_box_whisker, win_status = radio_group)


# DASHBOARD WIDGET CONTAINERS ("CARDS")
card_width = 320

search_card = pn.Card(
    pn.Column(
        # Widget 1
        radio_group
        # Widget 2
        # Widget 3
    ),
    title="Customization", width=card_width, collapsed=False
)

boxplot_tab = pn.Column(
    radio_group,
    dynamic_box_whisker
)

plot_card = pn.Card(
    pn.Column(
        # Widget 1
        width,
        # Widget 2
        height
        # Widget 3
    ),

    title="Plot", width=card_width, collapsed=False
)


# LAYOUT
layout = pn.template.FastListTemplate(
    title="League of Legends Win Rate",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Data", None),  # Replace None with callback binding
            ('Sankey', dynamic_plot), # Replace None with callback binding
            ('Box $ Whisker',dynamic_box_whisker),
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#8B008B',
    background_color = '#DA70D6'


).servable()

layout.show()

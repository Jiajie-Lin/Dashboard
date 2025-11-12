"""
Jiajie Lin
Description: Make a simple easy to use dashboard
"""
#imports
import panel as pn
from bmw_api import BMWAPI
from datetime import datetime
import graphs as graphs
import Read_ME as read

# Loads javascript dependencies and configures Panel (required)
pn.extension()



# Initialize the API!
api = BMWAPI()
api.load_data('BMW sales data (2010-2024) (1).csv')


#data set
data_set = api.bmw

#Read Me
read_me = read.read_me()

# WIDGET DECLARATIONS


# Search Widgets


# Plotting widgets
#width and height for sankey diagram
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1000)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=600)

#takes in the targets and sources for sankey
#attribute = target
#attribute 2 = source

attribute = pn.widgets.Select(name = 'Att 1/Left', options = api.get_attributes(), value = 'Year')
attribute2 = pn.widgets.Select(name = 'Att 2/Right', options = api.get_attributes(), value = 'Color')


#year slider for box and whiskers
year = pn.widgets.DateSlider(name = 'Year Slider',
                             start = datetime(2010,1,1),
                             end = datetime(2024,1,1),
                             value = datetime(2010,1,1),
                             format = '%Y'
)

#buttons for box and whisker each with a different color
Engine_Size_L = pn.widgets.Button(name = "Engine_Size_L", button_type = 'primary')
Mileage_KM = pn.widgets.Button(name = 'Mileage_KM',button_type = 'success')
Sales_Volume = pn.widgets.Button(name = 'Sales_volume', button_type = 'warning')
Price_USD = pn.widgets.Button(name = 'Price_USD', button_type = 'danger')

#all of the columns looked at by box and whisker
Key_Sales_Indicators = ['Engine_Size_L','Mileage_KM', 'Sales_Volume', "Price_USD"]

#used in callback to graph the specific column
current_attribute = pn.widgets.TextInput(value='Engine_Size_L')

# CALLBACK FUNCTIONS
#makes the sankey
def getplot(att1,att2,width,height):
    local = api.extract_local_network(att1,att2)
    fig = graphs.make_sankey(local, att1, att2, vals = 'Count', width = width, height = height)
    return fig

#makes the box and whisker
def box_whisker(year_value,att1):
    year_int = year_value.year
    local = api.single(year_int,att1)
    fig = graphs.make_box_and_whisker(local)
    fig.axes[0].set_title(f'{att1} - {year_int}')

    return fig

#whiches the value of current attribute when clicking the buttons
def on_engine_click(Enginze_Size_l):
    current_attribute.value = 'Engine_Size_L'

def on_mileage_click(Mileage_KM):
    current_attribute.value = 'Mileage_KM'

def on_sales_click(Sales_Volume):
    current_attribute.value = 'Sales_Volume'

def on_price_click(Price_USD):
    current_attribute.value = 'Price_USD'

#response to clicking the buttons
Engine_Size_L.on_click(on_engine_click)
Mileage_KM.on_click(on_mileage_click)
Sales_Volume.on_click(on_sales_click)
Price_USD.on_click(on_price_click)

# CALLBACK BINDINGS (Connecting widgets to callback functions)

#sankey plot binding
plot = pn.bind(getplot, attribute, attribute2, width = width, height = height)

#box and whisker plot binding
plot2 = pn.bind(box_whisker, year, current_attribute)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        # Widget 1
        attribute,
        # Widget 2
        attribute2,
        # Widget 3
    ),
    title="Search", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        # Widget 1
        width,
        # Widget 2
        height
        # Widget 3
    ),

    title="Plot", width=card_width, collapsed=True
)

Key_Sales = pn.Card(
    pn.Column(
        #widget 1
        year,
        #widget 2
        Engine_Size_L,
        # widget 3
        Mileage_KM,
        # widget 4
        Price_USD,
        # widget 5
        Sales_Volume,
    ),
    title = 'Box & Whisker'
)



# LAYOUT

layout = pn.template.FastListTemplate(
    title="BMW Sales",
    sidebar=[
        search_card,
        plot_card,
        Key_Sales,

    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            #tabs 0 for data,
            ("Data", None),  # Replace None with callback binding
            ('Read Me', read_me),
            #tab 1 for sankey
            ("Sankey", plot),
            #tab 2 for box and whisker
            ('Box $ Whisker', plot2),

            active= 1  # Which tab is active by default?
        )

    ],
    header_background='#7F007F',
    background_color ='#B300B3'

).servable()

layout.show()

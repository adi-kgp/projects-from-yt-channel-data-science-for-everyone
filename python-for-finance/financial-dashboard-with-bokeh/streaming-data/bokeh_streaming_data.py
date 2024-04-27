# Streaming Data (Generate fake data)
# Digital Ocean - server app

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select
from bokeh.layouts import layout
from bokeh.plotting import figure
from datetime import datetime
from math import radians # rotate axis ticks
import numpy as np

# Create Figure
f = figure(x_axis_type="datetime", width=900, height=350)

# generate data
def create_value():
    draw = np.random.randint(0,2, size=200)
    steps = np.where(draw>0,1, -1)
    walk = steps.cumsum() # [-1,1]
    return walk[-1]

# Create data source
source = ColumnDataSource(dict(x=[], y=[]))

f.circle(x="x", y="y", color="firebrick", line_color="firebrick", source=source)
f.line(x="x", y="y", source=source)

# Create a Periodic function
def update():
    new_data = dict(x=[datetime.now()], y=[create_value()])
    source.stream(new_data, rollover=200)
    f.title.text = "Now Streaming %s Data" % select.value

# Callback function
def update_intermed(attrname, old, new):
    source.data = dict(x=[], y=[])
    update()

date_pattern = ["%Y-%m-%d\n%H:%M:%S"]

f.xaxis.formatter = DatetimeTickFormatter(
    seconds=date_pattern,
    minsec = date_pattern,
    minutes = date_pattern,
    hourmin = date_pattern,
    hours = date_pattern,
    days = date_pattern,
    months = date_pattern,
    years = date_pattern,
)

f.xaxis.major_label_orientation=radians(80)
f.xaxis.axis_label = "Date"
f.yaxis.axis_label = "Value"

# Create selection widget
options = [("stock1", "Stock One"), ("stock2", "Stock Two")]
select = Select(title="Market Name", value="stock1", options=options)
select.on_change("value", update_intermed)

# Configure the layout
lay_out = layout([[f], [select]])
curdoc().theme = "dark_minimal"
curdoc().title = "Streaming Stock Data Example"
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 500)

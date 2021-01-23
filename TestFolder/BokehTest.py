from bokeh.models import HoverTool, Legend
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import bokeh.plotting
import bokeh.layouts

import datetime
import numpy as np
import bokeh.models
from bokeh.models import ColumnDataSource, Grid, Line, LinearAxis, Plot
from bokeh.models.markers import marker_types

import DownloadData

age, year_week, data = DownloadData.incidence()
np_data = np.array(data)

np_data[np_data == None] = 0

data = np_data

np.savetxt('age.txt',age,fmt="%s")
np.savetxt('year_week.txt',year_week,fmt="%s")
np.savetxt('data.txt',np_data,fmt="%s")


age = np.genfromtxt('age.txt', dtype='str')
year_week = np.genfromtxt('year_week.txt', dtype='str')
data = np.loadtxt('data.txt')


def yw2datetime(yw):
    if isinstance(yw, (list, np.ndarray)):
        return [yw2datetime(i) for i in yw]
    yw_int = [int(i) for i in yw.split('-KW')]
    weekday = datetime.datetime(yw_int[0], 1, 1).weekday()
    if weekday <= 3:  # Thursday
        date_diff = 1 - weekday
    else:
        date_diff = 8 - weekday
    if date_diff > 0:
        return datetime.datetime(yw_int[0], 1, date_diff) + datetime.timedelta(weeks=yw_int[1] - 1, days=6)
    else:
        return datetime.datetime(yw_int[0] - 1, 12, 31 + date_diff) + datetime.timedelta(weeks=yw_int[1] - 1, days=6)


# output to static HTML file
output_file("lines.html")
# create a new plot with a title and axis labels

hover_tool = HoverTool(
    tooltips=[
        ('Altersgruppe', "$name"),
        ("Datum", "$x"),
        ("Inzidenz", "$y"),
    ],
    formatters={
        '$x': 'datetime',
    },
    mode='vline'
)

p1 = figure(title="Inzidenz nach Altersgruppen", x_axis_type='datetime', x_axis_label='Datum', y_axis_label='Inzidenz',
            tools='pan,wheel_zoom,box_zoom,reset')
p1.sizing_mode = "stretch_both"
label = bokeh.models.Label(x=3,y=3,x_units='screen',y_units='screen',text='Some Stuff')
p1.add_layout(label)
p1.xaxis[0].formatter = bokeh.models.DatetimeTickFormatter() # PrintfTickFormatter(format="%d.%m.%Y")
# hover = p1.select(dict(type=HoverTool))
p1.add_tools(HoverTool(
    tooltips=[
        ("Alter", "@desc"),
        ("Datum", "@x_list{%d.%m.%Y}"),
        ("Inzidenz", "@y_list"),
    ],
    formatters={'@x_list': 'datetime', },
))

# hover.tooltips = [
#    ("Alter", "@desc"),
#    ("Datum", "@x"),
#    ("Inzidenz", "@y"),
# ]
# hover.mode = 'vline'
# hover.formatters = {'@x':'datetime',}
cmap_colors = np.zeros([3, len(age)])

print(np.linspace(0, 1, 4))

cmap_colors[0] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([17.6, 19.2, 83.1, 83.1]) / 100 * 255)
cmap_colors[1] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([66.7, 30.2, 22, 62.7]) / 100 * 255)
cmap_colors[2] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([17.6, 55.7, 22, 22]) / 100 * 255)

cmap_colors = cmap_colors.astype(np.uint8)

legend_list = []

print(marker_types)

marker_list = [m_type for m_type in marker_types]
marker_selector = [0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25]


for i in range(len(age)):
    if age[i]=='Gesamt':
        line_color = (0,0,0)
        line_width = 2
    else:
        line_color = tuple(cmap_colors[:, i])
        line_width = 1
    muted_alpha = .1
    source = ColumnDataSource(data=dict(
        x_list=list(yw2datetime(year_week)),
        y_list=list(data[i][:]),
        desc=[age[i] for x in range(len(year_week))],
        col=[line_color for x in year_week]
    ))
    li = p1.line(x="x_list", y="y_list", line_color=line_color, line_width=line_width, line_alpha=1, source=source, muted_alpha=muted_alpha)
    #gly = bokeh.models.X(x="x", y="y", size=10, line_color=line_color, line_width=2, fill_color=None)
    #gly_p1 = p1.add_glyph(source, gly)
    sca = p1.scatter(x="x_list", y="y_list", source=source,muted_alpha=muted_alpha)
    #sca.glyph.marker=marker_list[i]
    #legend_list.append((age[i], [li]))
    sca.glyph.marker = marker_list[marker_selector[i]]
    sca.glyph.line_color = line_color
    sca.glyph.fill_color=None
    sca.glyph.size = 8
    legend_list.append((age[i], [li, sca]))
leg = Legend(items=legend_list, location=(0, 0))
leg.location = "top_left"
leg.click_policy = "mute"
leg.orientation = "horizontal"
p1.add_layout(leg, 'above')
p2 = figure(title="simple line example", x_axis_label='x', y_axis_label='y', x_range=p1.x_range)
p2.line(yw2datetime(year_week), data[i][:], legend_label='None')
p2.sizing_mode = "stretch_both"
# p1.multi_line(yw2datetime(year_week[:]),np.transpose(data, (2, 3, 0, 1)))
column = bokeh.layouts.column([p1])#, p2])
column.sizing_mode = "stretch_both"

# show the results

show(column)

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.models.markers import marker_types
import bokeh.layouts
import datetime
import numpy as np

import DownloadData

age, year_week, data = DownloadData.incidence()
np_data = np.array(data)

np_data[np_data == None] = 0

data = np_data

np.savetxt('age.txt', age, fmt="%s")
np.savetxt('year_week.txt', year_week, fmt="%s")
np.savetxt('data.txt', np_data, fmt="%s")

age = np.genfromtxt('age.txt', dtype='str')
year_week = np.genfromtxt('year_week.txt', dtype='str')
data = np.loadtxt('data.txt')

data, interp = DownloadData.extrapolateLastWeek(year_week, data)
print('Extrapolated last DataPoint: ', interp)


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
label = bokeh.models.Label(x=3, y=3, x_units='screen', y_units='screen',
                           text='Stand: ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") +
                                '; Quellen: Fallzahlen - Robert Koch-Institut: SurvStat@RKI 2.0, https://survstat.rki.de;' +
                                ' Bevölkerung: https://www-genesis.destatis.de/ 12411-0005 31.12.2019',
                           text_font_size='8pt')
#
p1.add_layout(label)
p1.xaxis[0].formatter = bokeh.models.DatetimeTickFormatter()  # PrintfTickFormatter(format="%d.%m.%Y")

cmap_colors = np.zeros([3, len(age)])

cmap_colors[0] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([17.6, 19.2, 83.1, 83.1]) / 100 * 255)
cmap_colors[1] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([66.7, 30.2, 22, 62.7]) / 100 * 255)
cmap_colors[2] = np.interp(np.linspace(0, 1, len(age)), np.linspace(0, 1, 4),
                           np.array([17.6, 55.7, 22, 22]) / 100 * 255)

cmap_colors = cmap_colors.astype(np.uint8)

marker_list = [m_type for m_type in marker_types]
marker_selector = [0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15,
                   16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25,
                   0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15,
                   16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25,
                   0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15,
                   16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25,
                   0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25]

glyph_list = []

for i in range(len(age)):
    if age[i] == 'Gesamt':
        line_color = (0, 0, 0)
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
    if interp:
        li = p1.line(source.data['x_list'][:-1], source.data['y_list'][:-1], line_color=line_color,
                     line_width=line_width,
                     line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i])
        li2 = p1.line(source.data['x_list'][-2:], source.data['y_list'][-2:], line_color=line_color,
                      line_width=line_width,
                      line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i], line_dash=[3, 3])
    else:
        li = p1.line(source.data['x_list'], source.data['y_list'], line_color=line_color, line_width=line_width,
                     line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i])
    sca = p1.scatter(x="x_list", y="y_list", source=source, muted_alpha=muted_alpha, legend_label=age[i])
    sca.glyph.marker = marker_list[marker_selector[i]]
    sca.glyph.line_color = line_color
    sca.glyph.fill_color = None
    sca.glyph.size = 8
    glyph_list.append(sca)
p1.add_tools(HoverTool(
    renderers=glyph_list,
    tooltips=[
        ("Alter", "@desc"),
        ("Datum", "@x_list{%d.%m.%Y}"),
        ("Inzidenz", "@y_list{0}"),
    ],
    formatters={'@x_list': 'datetime', },
))

p1.legend.location = "top_left"
p1.legend.click_policy = "mute"
p1.legend.orientation = "horizontal"
column = bokeh.layouts.column([p1])  # , p2])
column.sizing_mode = "stretch_both"


show(column)

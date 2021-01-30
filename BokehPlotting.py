from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
import bokeh.layouts
import datetime
import numpy as np
import DownloadData


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


def get_cmap(num):
    cmap_colors = np.zeros([3, num])

    cmap_colors[0] = np.interp(np.linspace(0, 1, num), np.linspace(0, 1, 4),
                               np.array([17.6, 19.2, 83.1, 83.1]) / 100 * 255)
    cmap_colors[1] = np.interp(np.linspace(0, 1, num), np.linspace(0, 1, 4),
                               np.array([66.7, 30.2, 22, 62.7]) / 100 * 255)
    cmap_colors[2] = np.interp(np.linspace(0, 1, num), np.linspace(0, 1, 4),
                               np.array([17.6, 55.7, 22, 22]) / 100 * 255)
    return cmap_colors.astype(np.uint8)


def getmarker():
    marker_list = [m_type for m_type in bokeh.models.markers.marker_types]
    marker_selector = [0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14,
                       15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21,
                       24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6,
                       8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16,
                       12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25,
                       0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14,
                       15, 16, 12, 21, 24, 25, 0, 1, 6, 8, 14, 15, 16, 12, 21, 24, 25]
    return marker_list, marker_selector

def remove_none(item):
    item = np.array(item)
    item[item==None] = 0
    return item

def plot_data(p,age,year_week,data,collect_data=False,incidence=True):
    data = remove_none(data)
    data, interp = DownloadData.extrapolateLastWeek(year_week, data, collect_data=collect_data)
    p.sizing_mode = "stretch_both"
    p.xaxis[0].formatter = bokeh.models.DatetimeTickFormatter()  # PrintfTickFormatter(format="%d.%m.%Y")
    cmap_colors = get_cmap(len(age))

    marker_list, marker_selector = getmarker()

    glyph_list = []

    for i in range(len(age)):
        if age[i] == 'Gesamt':
            line_color = (0, 0, 0)
            line_width = 2
            time, count = DownloadData.get_total(incidence=incidence)
            source = ColumnDataSource(data=dict(
                x_list=time,
                y_list=list(count),
                desc=[age[i] for x in time],
                col=[line_color for x in time]
            ))
        else:
            line_color = tuple(cmap_colors[:, i])
            line_width = 1
            source = ColumnDataSource(data=dict(
                x_list=list(yw2datetime(year_week)),
                y_list=list(data[i][:]),
                desc=[age[i] for x in year_week],
                col=[line_color for x in year_week]
            ))
        muted_alpha = .1

        if interp:
            li = p.line(source.data['x_list'][:-1], source.data['y_list'][:-1], line_color=line_color,
                         line_width=line_width,
                         line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i])
            li2 = p.line(source.data['x_list'][-2:], source.data['y_list'][-2:], line_color=line_color,
                          line_width=line_width,
                          line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i], line_dash=[3, 3])
        else:
            li = p.line(source.data['x_list'], source.data['y_list'], line_color=line_color, line_width=line_width,
                         line_alpha=1, muted_alpha=muted_alpha, legend_label=age[i])
        sca = p.scatter(x="x_list", y="y_list", source=source, muted_alpha=muted_alpha, legend_label=age[i])
        sca.glyph.marker = marker_list[marker_selector[i]]
        sca.glyph.line_color = line_color
        sca.glyph.fill_color = None
        sca.glyph.size = 8
        glyph_list.append(sca)
    if incidence:
        incidence_cases = "Inzidenz"
    else:
        incidence_cases = "Fallzahlen"
    p.add_tools(HoverTool(
        renderers=glyph_list,
        tooltips=[
            ("Alter", "@desc"),
            ("Datum", "@x_list{%d.%m.%Y}"),
            ("Inzidenz", "@y_list{0}"),
        ],
        formatters={'@x_list': 'datetime', },
    ))

    p.legend.location = "top_left"
    p.legend.click_policy = "mute"
    p.legend.orientation = "horizontal"
    return p

def x_bounds(year_week):
    yw_dat = yw2datetime(year_week)
    return [yw_dat[0]-datetime.timedelta(weeks=1), yw_dat[-1]+datetime.timedelta(weeks=1)]

def __init__():
    age, year_week, data, abs_data = DownloadData.incidence(True)

    x_bound = x_bounds(year_week)

    output_file("lines.html")

    p1 = figure(title="Inzidenz nach Altersgruppen", x_axis_type='datetime', x_axis_label='Datum',
                y_axis_label='Inzidenz',
                tools='pan,wheel_zoom,box_zoom,reset')
    p2 = figure(title="Fallzahlen nach Altersgruppen", x_axis_type='datetime', x_axis_label='Datum',
                y_axis_label='Fallzahl',
                tools='pan,wheel_zoom,box_zoom,reset')
    p1 = plot_data(p1, age, year_week, data, collect_data=True, incidence=True)
    p2 = plot_data(p2, age, year_week, abs_data, incidence=False)
    p1.x_range=bokeh.models.Range1d(x_bound[0],x_bound[1])
    p2.x_range=p1.x_range

    date_range_slider = bokeh.models.DateRangeSlider(value=(x_bound[0],x_bound[1]),
                                        start=x_bound[0], end=x_bound[1])
    def update_xrange(p):
        return bokeh.models.CustomJS(args=dict(p=p), code="""
                var a = cb_obj.value;
                p.x_range.start = a[0];
                p.x_range.end = a[1];
            """)



    date_range_slider.js_on_change('value', update_xrange(p1))
    #date_range_slider.js_on_change('value', update_xrange(p2))

    tab1 = bokeh.models.Panel(child=p1, title="Inzidenz")
    tab2 = bokeh.models.Panel(child=p2, title="Fallzahl")


    sub_text = bokeh.models.Div(text='<p style="font-size:10px">Stand: ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") +
                                     '; Quellen: <a href="https://survstat.rki.de">Fallzahlen - Robert Koch-Institut: SurvStat@RKI 2.0</a>;' +
                                     ' <a href="https://www-genesis.destatis.de/genesis//online?operation=table&code=12411-0005&bypass=true&'
                                     'levelindex=0&levelid=1611832679336">Bevölkerung - Statistisches Bundesamt (Destatis), 12411-0005 31.12.2019</a><br>'
                                     '<a href="https://github.com/timkalkus/RKI_Covid_Age">Github-Seite</a> des Tools</p>')

    column = bokeh.layouts.column([bokeh.models.Tabs(tabs=[tab1, tab2]),date_range_slider, sub_text])
    column.sizing_mode = "stretch_both"
    show(column)


__init__()

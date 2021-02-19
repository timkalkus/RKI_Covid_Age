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

def plot_data(p,age,year_week,data,collect_data=False,incidence=True,procentual=False):
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
            if procentual:
                time_diff = 7
                time = time[time_diff:]
                count = calculate_procentual(count,time_diff)
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
        if age[i] == 'Gesamt':
            sca = p.scatter(x="x_list", y="y_list", source=source, alpha=0, muted_alpha=0, legend_label=age[i])
        else:
            sca = p.scatter(x="x_list", y="y_list", source=source, muted_alpha=muted_alpha, legend_label=age[i])
        sca.glyph.marker = marker_list[marker_selector[i]]
        sca.glyph.line_color = line_color
        sca.glyph.fill_color = None
        sca.glyph.size = 8
        glyph_list.append(sca)
    procent=""
    if incidence:
        incidence_cases = "Inzidenz"
    else:
        incidence_cases = "Fallzahlen"
    if procentual:
        incidence_cases = "Unterschied"
        procent = "%"
    p.add_tools(HoverTool(
        renderers=glyph_list,
        tooltips=[
            ("Alter", "@desc"),
            ("Datum", "@x_list{%d.%m.%Y}"),
            (incidence_cases, "@y_list{0}"+procent),
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


def align_arrays(x_list,y_list, extend_values=False):
    x_total=np.unique(np.concatenate(x_list))
    y_return=[]
    for x,y in zip(x_list,y_list):
        _, indices,_ = np.intersect1d(x_total,x,return_indices=True)
        y_new=np.zeros(np.shape(x_total))
        y_new[indices]=y
        if extend_values:
            #y_new[:indices[0]]=y_new[indices[0]]
            y_new[indices[-1]+1:]=y_new[indices[-1]]
        y_return.append(y_new)
    return x_total, y_return


def plot_sum(p):
    p.sizing_mode = "stretch_both"
    p.xaxis[0].formatter = bokeh.models.DatetimeTickFormatter()  # PrintfTickFormatter(format="%d.%m.%Y")
    total_date, total_count = DownloadData.get_total(incidence=False,smooth=False)
    vac_date, vac_first, vac_second = DownloadData.get_vaccination_data()
    x,y_list = align_arrays([total_date,vac_date,vac_date],[total_count,vac_first,vac_second],True)
    y_list[0] = np.cumsum(y_list[0])
    y_list[1] = np.cumsum(y_list[1])
    y_list[2] = np.cumsum(y_list[2])
    names = ['Zweite Impfung','Erste Impfung','Infizierte']
    source = ColumnDataSource(data=dict(
        x_list=x,
        y_list=y_list[0]+y_list[1]+y_list[2],
        infected=y_list[0],
        vax_first=y_list[1],
        vax_second=y_list[2],
    ))
    #for i in range(3):
    #    p.line(x,y_list[i],legend_label=names[i])
    #p.line(x=list(range(len(x)-1)),y=x[1:]-x[:-1],legend_label='123')
    p.varea_stack(['vax_second', 'vax_first', 'infected'], x='x_list', source=source, legend_label=names,
                   color=[(50, 50, 200), (50, 200, 50), (200, 50, 50)])
    glyph = p.line(x='x_list', y='y_list', source=source, alpha=0)
    five_percentile = np.max([np.floor(np.max(y_list[0]+y_list[1]+y_list[2])/(DownloadData.count_age('Gesamt')*0.05)),1])

    p.line(x=[x[0], x[-1]], y=[DownloadData.count_age('Gesamt')*0.05*five_percentile, DownloadData.count_age('Gesamt')*0.05],
           line_width=2, legend_label='{:}% Bevölkerung'.format(5*five_percentile), line_dash=[3, 3])
    p.legend.location = "top_left"
    #p.legend.click_policy = "mute"
    p.legend.orientation = "horizontal"
    p.add_tools(HoverTool(
        renderers=[glyph],
        tooltips=[
            ("Datum", "@x_list{%d.%m.%Y}"),
            ("Infektionen", "@infected{0}"),
            ("Erste Impfung", "@vax_first{0}"),
            ("Zweite Impfung", "@vax_second{0}"),
        ],
        formatters={'@x_list': 'datetime', },
        mode='vline',
    ))
    return p

def calculate_procentual(data,diff=1):
    with np.errstate(all='ignore'):
        if np.ndim(data) == 1:
            return_value = (data[diff:] - data[:-diff]) / data[:-diff] * 100
        else:
            return_value = (data[:, diff:] - data[:, :-diff]) / data[:, :-diff] * 100
    #return_value[return_value == None] = 0
    np.nan_to_num(return_value, copy=False, nan=0, posinf=0, neginf=0)
    return return_value



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
    p3 = figure(title="Prozentualer Unterschied zur Vorwoche", x_axis_type='datetime', x_axis_label='Datum',
                y_axis_label='Unterschied zur Vorwoche in %',
                tools='pan,wheel_zoom,box_zoom,reset')
    p4 = figure(title="Infektion und Impfung - Kumulativ", x_axis_type='datetime', x_axis_label='Datum',
                y_axis_label='Personen',
                tools='pan,wheel_zoom,box_zoom,reset')
    p1 = plot_data(p1, age, year_week, data, collect_data=True, incidence=True)
    p2 = plot_data(p2, age, year_week, abs_data, incidence=False)

    p3 = plot_data(p3,age,year_week[1:],calculate_procentual(data), incidence=False, procentual=True)
    p4 = plot_sum(p4)
    p1.x_range = bokeh.models.Range1d(x_bound[0],x_bound[1])
    p4.x_range = p3.x_range = p2.x_range = p1.x_range

    p3.y_range = bokeh.models.Range1d(-100, 100)

    time, count = DownloadData.get_total(incidence=False)

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
    tab3 = bokeh.models.Panel(child=p3, title="Prozentuale Veränderung")
    tab4 = bokeh.models.Panel(child=p4, title="Kumulativ")

    sub_text = bokeh.models.Div(text='<p style="font-size:10px">Stand: ' + datetime.datetime.now().strftime("%d.%m.%Y %H:%M") +
                                     '; Quellen: <a href="https://survstat.rki.de">Fallzahlen Altersgruppen - Robert Koch-Institut: SurvStat@RKI 2.0</a>; '
                                     '<a href="https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0">Fallzahlen Gesamt - Robert Koch-Institut (RKI), dl-de/by-2-0</a>; '
                                     '<a href="https://www-genesis.destatis.de/genesis//online?operation=table&code=12411-0005&bypass=true&'
                                     'levelindex=0&levelid=1611832679336">Bevölkerung - Statistisches Bundesamt (Destatis), 12411-0005 31.12.2019</a>; '
                                     '<a href="https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv">Impfdaten - impfdashboard.de</a>;<br>'
                                     '<a href="https://github.com/timkalkus/RKI_Covid_Age">Github-Seite</a> des Tools</p>')

    column = bokeh.layouts.column([bokeh.models.Tabs(tabs=[tab1, tab2, tab3, tab4]),date_range_slider, sub_text])
    column.sizing_mode = "stretch_both"
    show(column)


__init__()

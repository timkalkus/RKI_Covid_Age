from bokeh.plotting import figure, output_file, show
import bokeh.plotting
import bokeh.layouts
import DownloadData
import datetime
import numpy as np

"""

age, year_week, data = DownloadData.clean_fetch()
np_data = np.array(data)
#print(data)
np_data[np_data==None]=0
#print(np_data)
data = np_data

np.savetxt('age.txt',age,fmt="%s")
np.savetxt('year_week.txt',year_week,fmt="%s")
np.savetxt('data.txt',np_data,fmt="%s")

"""

age = np.genfromtxt('age.txt',dtype='str')
year_week = np.genfromtxt('year_week.txt',dtype='str')
data = np.loadtxt('data.txt')

#print(age)
#print(year_week)
#print(data)


def yw2datetime(yw):
    if isinstance(yw,(list,np.ndarray)):
        return [yw2datetime(i) for i in yw]
    yw_int = [int(i) for i in yw.split('-KW')]
    weekday = datetime.datetime(yw_int[0],1,1).weekday()
    if weekday<=3: # Thursday
        date_diff=1-weekday
    else:
        date_diff=8-weekday
    if date_diff > 0:
        return datetime.datetime(yw_int[0],1,date_diff)+datetime.timedelta(weeks=yw_int[1]-1,days=6)
    else:
        return datetime.datetime(yw_int[0]-1,12,31+date_diff)+datetime.timedelta(weeks=yw_int[1]-1,days=6)

# output to static HTML file
output_file("lines.html")
# create a new plot with a title and axis labels
p1 = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
p1.sizing_mode = "stretch_both"

cmap_colors=np.zeros([3,len(age)])

print(np.linspace(0,1,4))

cmap_colors[0] = np.interp(np.linspace(0,1,len(age)),np.linspace(0,1,4),np.array([17.6, 19.2, 83.1, 83.1])/100*255)
cmap_colors[1] = np.interp(np.linspace(0,1,len(age)),np.linspace(0,1,4),np.array([66.7, 30.2, 22, 62.7])/100*255)
cmap_colors[2] = np.interp(np.linspace(0,1,len(age)),np.linspace(0,1,4),np.array([17.6, 55.7, 22, 22])/100*255)

cmap_colors = cmap_colors.astype(np.uint8)

# add a line renderer with legend and line thickness
#p1.line(x, y, legend_label="Temp.", line_width=2)
for i in range(len(age)):
    p1.line(yw2datetime(year_week), data[i][:],line_color=tuple(cmap_colors[:,i]),legend_label=age[i])

p1.legend.location = "top_left"
p1.legend.click_policy="hide"
p1.legend.orientation = "horizontal"
p2 = figure(title="simple line example", x_axis_label='x', y_axis_label='y',x_range=p1.x_range)
p2.sizing_mode = "stretch_both"
#p1.multi_line(yw2datetime(year_week[:]),np.transpose(data, (2, 3, 0, 1)))
column = bokeh.layouts.column([p1, p2])
column.sizing_mode = "stretch_both"

# show the results

show(column)

from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models import LabelSet,ranges
from cmath import pi
import json

with open('election.json') as data_file:
    data = json.load(data_file)

top = []
colors = []
names = []

minorityTop = 0
for i in data:
    if(i.get('share') < 1):
        minorityTop += i.get('share')
        continue
    top.append(i.get('share'))
    colors.append(i.get('color'))
    names.append(i.get('short'))

top.append(minorityTop)
names.append('Minority')
colors.append('black')
x = range(0, len(top))

source = ColumnDataSource(dict(x=x,y=top, color=colors, names=names))

plot = figure(title = 'Výsledky voleb 2017',
              x_axis_label = 'Politické strany',
              y_axis_label = 'Počet hlasů',
              )

labels = LabelSet(x='x', y='y', text='y', level='glyph',
        x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')

plot.vbar(source=source,x='x',top='y',bottom=0,width=1, color='color')
plot.add_layout(labels)

show(plot)




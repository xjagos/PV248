from bokeh.plotting import figure, show, ColumnDataSource
import io
from bokeh.models import LabelSet,ranges
from cmath import pi
import json

with io.open('election.json') as data_file:
    data = json.load(data_file)

top = [0]
colors = []
names = []

minorityTop = 0
for i in data:
    if(i.get('share') < 1):
        minorityTop += i.get('share')
        continue
    top.append(i.get('share'))
    colors.append(i.get('color'))
    lbl = "{} {}%".format(i.get('short'),str(i.get('share')))
    names.append(lbl)

top.append(minorityTop)
names.append("Minority {}%".format(minorityTop - minorityTop % 0.01))
colors.append('black')
x = range(0, len(top))

percents = []
sum = 0
for t in top:
    sum += (t/100)
    percents.append(sum)

src = ColumnDataSource(data={
    'start':[p*2*pi for p in percents[:-1]],
    'end':[p*2*pi for p in percents[1:]],
    'color':colors,
    'label': names,
    'value': percents[:-1]
})

p = figure(x_range=(-1,1), y_range=(-1,1))

p.wedge(x=0, y=0, radius=1,
        start_angle='start',
        end_angle='end',
        color='color',
        legend='label',
        source=src)


show(p)






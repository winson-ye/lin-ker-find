from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from matplotlib.lines import Line2D as li2d

class LineBuilder:
    def __init__(self, line):
        line.set_data([], [])
        self.line = line
        self.xs = list()
        self.ys = list()
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        print('click', event)
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

    def finish(self, event):
        self.xs.append(self.xs[0])
        self.ys.append(self.ys[0])
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        self.line.figure.canvas.mpl_disconnect(self.cid)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click done when finished creating polygon')
plt.subplots_adjust(bottom=0.2)

axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
bdone = Button(axdone, 'Done')

line, = ax.plot([0], [0], marker = 'o')  # empty line
linebuilder = LineBuilder(line)
bdone.on_clicked(linebuilder.finish)

plt.show()
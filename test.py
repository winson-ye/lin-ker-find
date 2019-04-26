import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import *
from matplotlib.widgets import Button


class LineBuilder:
    def __init__(self, line):
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

    def _finish(self, event):
        self.xs.append(self.xs[0])
        self.ys.append(self.ys[0])
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        self.line.figure.canvas.mpl_disconnect(self.cid)
        """
        connect the polygon back to the first point.
        """


def main():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click done to create your polygon')
    plt.subplots_adjust(bottom=0.2)

    axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
    bdone = Button(axdone, 'Done')

    line, = ax.plot([], [], marker = 'o')
    linebuilder = LineBuilder(line)
    bdone.on_clicked(linebuilder._finish)

    x = [20, 40, 20, 20]
    y = [20, 40, 40, 20]

    #ax.fill(x, y, alpha=0.5)
    ax.set_ylim([0, 100])
    ax.set_xlim([0, 100])

    #ax.plot(x, y, marker = 'o')

    #for xs in x:
    #    for ys in y:
    #        ax.annotate('hi', xy=(xs, ys), xytext=(xs + 10, ys + 10), arrowprops=dict(facecolor='black'))

    #p = Polygon([(20, 20), (40, 40), (20, 40), (20, 20)])
    #p.set_label('triangle')
    #p.set_alpha(0.2)
    #p.set_color('r')
    #ax.annotate('hi', horizontalalignment='center')
    #plt.pause(5)
    #ax.add_patch(p)

    #ax.annotate('hi', xy=(20, 20), xytext=(30, 30), arrowprops=dict(facecolor='black'))

    #ax.set_title('hi')


    plt.show()

    '''
    testing code for point representations
    print(linebuilder.xs, "\n", linebuilder.ys)
    '''

    lst = []
    for x,y in zip(linebuilder.xs, linebuilder.ys):
        lst.append((x, y))
    P = Polygon(lst)
    print(P.get_xy())


    '''
    testing code for filling regions
    x = [0, 1, 2, 1]
    y = [1, 2, 1, 0]

    ax.fill(x, y, alpha=0.5)
    ax.set_ylim([0, 0.5])
    ax.set_xlim([0, 0.5])
    '''


if __name__ == '__main__':
    main()

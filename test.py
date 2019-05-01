import matplotlib.pyplot as plt
from Classes import *

XLIM = [0, 100]
YLIM = [0, 100]

fig = plt.figure()
ax = fig.add_subplot(111)

def main():

    #need some way to store original input polygon
    shape = getInputPoly()

    ker = Polygon([(0, 0), (50, 50), (100, 0)])

    plotA(ax, (ker, 1), Node((0, 0)), Node((100, 0)), 1, shape)

def getInputPoly():

    plt.ion()
    plt.show()

    ax.set_title('click done to create your polygon')
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    plt.subplots_adjust(bottom=0.2)

    axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
    bdone = Button(axdone, 'Done')

    line, = ax.plot([], [], marker = 'o')
    linebuilder = LineBuilder(line)
    bdone.on_clicked(linebuilder._finish)

    input("Press [enter] to finalize polygon.\n")

    ax.cla()
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)

    lst = []
    for x,y in zip(linebuilder.xs, linebuilder.ys):
        lst.append((x, y))

    p = Polygon(lst)

    ax.add_patch(p)

    input("Press [enter] to continue.\n")

    return p

def plotA(ax, ker_tup, F, L, i, poly):
    if type(ker_tup) != tuple:
        raise TypeError(ker_tup)

    k = ker_tup[0]

    if ker_tup[1] == -1:
        k = ker_tup[0].set_visible(False)

    ax.cla()
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    k.set_alpha(0.3)
    k.set_color('r')
    
    ax.add_patch(poly)
    ax.add_patch(k)
    
    ax.set_title("drawing K" + str(i))

    if type(F) != Lambda:
        ax.plot(F.coords[0], F.coords[1], marker='o', label='F[' + str(i) + ']', markersize=14)

    if type(L) != Lambda:
        ax.plot(L.coords[0], L.coords[1], marker='o', label='L[' + str(i) + ']', markersize=14)

    ax.legend(loc='upper left')

    input("Press [enter] to continue.")

if __name__ == '__main__':
    main()
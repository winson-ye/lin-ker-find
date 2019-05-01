import matplotlib.pyplot as plt
from classes2 import *
import pdb
import math


XLIM = [0, 100]
YLIM = [0, 100]

fig = plt.figure()
ax = fig.add_subplot(111)

#triangle
#P = StructuredPoly([(0,0), (10,10), (0,20), (20,10), (0,0)])

#chomper
#P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 4), (2, 6), (10, 8), (10, 10), (0, 10)])

#star
P = StructuredPoly([(0, 50), (30, 70), (50, 100), (70, 70), (100, 50), (70, 30), (50, 0), (30, 30), (0, 50)])

# P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 2), (2, 8), (10, 8), (10, 10), (0, 10)])



def getInputPoly():
    ax.set_title('click done to create your polygon')
    plt.subplots_adjust(bottom=0.2)

    axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
    bdone = Button(axdone, 'Done')

    line, = ax.plot([], [], marker = 'o')
    linebuilder = LineBuilder(line)
    bdone.on_clicked(linebuilder._finish)
    plt.show()

    lst = []
    for x,y in zip(linebuilder.xs, linebuilder.ys):
        lst.append((x, y))
    return StructuredPoly(lst)




def getKernel(P):
    poly = [tuple(x) for x in P.polygon.get_xy()]
    angle = P.flex_dictionary
    #pdb.set_trace()

    list_of_vertices = poly
    if angle[list_of_vertices[0]] == -1:
        # If so, make a K_0
        initial_node = Node(list_of_vertices[0])
        head_lambda = Lambda((list_of_vertices[1][0] - list_of_vertices[0][0], list_of_vertices[1][1] - list_of_vertices[0][1]))
        tail_lambda = Lambda((list_of_vertices[0][0] - list_of_vertices[-2][0], list_of_vertices[0][1] - list_of_vertices[-2][1]))

        '''
        head_lambda.next = initial_node
        head_lambda.prev = None

        initial_node.next = tail_lambda
        initial_node.prev = head_lambda

        tail_lambda.next = None
        tail_lambda.prev = initial_node
        '''

        P.K.addHead(head_lambda)
        P.K.addTail(tail_lambda)
        P.K.addNode(head_lambda, initial_node, tail_lambda)
        P.F = head_lambda
        P.L = tail_lambda
        #return P.k

    else:
        return poly

    for i in range(1, len(poly) - 2):
        #pdb.set_trace()
        if angle[poly[i]] == -1:
            result = _reflex(i, P)
        elif angle[poly[i]] == 1:
            result = _convex(i, P)

        if result == -1:
            return Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)]).get_xy()

    return P.K #JeffsAlgorithm(ker[len(poly) - 2])




def _reflex(i, StrP):
    P = [tuple(x) for x in StrP.polygon.get_xy()]

    edge = (P[i+1][0] - P[i][0], P[i+1][1] - P[i][1])
    new_vertex = Node(P[i+1])
    new_lambda = Lambda(edge)
    new_lambda.next, new_vertex.prev = new_vertex, new_lambda

    #pdb.set_trace()

    if ccw(new_vertex, move(new_vertex, StrP.F), new_lambda) != 1:
        pointer1, K_edge_int = StrP.F, None
        while pointer1 != StrP.L and K_edge_int == None:
            K_edge_int = findIntersection(pointer1, pointer1.next, new_lambda, new_vertex)
            pointer1 = pointer1.next

        if K_edge_int == None:
            return -1

        wprime = Node(K_edge_int)

        pointer2, K_edge_int = StrP.F, None
        while pointer2 != StrP.K.getHead() and K_edge_int == None:
            K_edge_int = findIntersection(pointer2.prev, pointer2, new_lambda, new_vertex)
            pointer2 = pointer2.prev

        #pdb.set_trace()
        H_slope, T_slope = slope(StrP.K.head, StrP.K.head.next), slope(StrP.K.tail.prev, StrP.K.tail)
        edge_slope = slope(new_lambda, new_vertex)
        c = StrP.K.tail[0] * StrP.K.head[1] - StrP.K.head[0] * StrP.K.tail[1]
        t = StrP.K.tail[0] * new_lambda[1] - StrP.K.tail[1] * new_lambda[0]
        s = StrP.K.head[0] * new_lambda[1] - StrP.K.head[1] * new_lambda[0]

        if K_edge_int != None:
            wdprime = Node(K_edge_int)
            StrP.K.addNode(pointer2, wdprime, pointer1)
            StrP.K.addNode(wdprime, wprime, pointer1)

        elif c * t >= 0 and c * s >= 0:
            StrP.K.addNode(pointer2, wprime, pointer1)
            StrP.K.addNode(None, new_lambda, wprime)
            pdb.set_trace()
            wdprime = None

        else:
            pointer3, K_edge_int = StrP.K.tail, None
            while K_edge_int != None:
                K_edge_int = findIntersection(pointer3.prev, pointer3, new_lambda, new_vertex)
                pointer3 = pointer3.prev

            wdprime = Node(K_edge_int)
            StrP.K.addNode(pointer3, wdprime, pointer1)
            StrP.K.addNode(wdprime, wprime, pointer1)
            StrP.K.setHead(wprime)
            StrP.K.setTail(wdprime)
            StrP.K.makeCircular()

        if wdprime == None:
            StrP.F = new_lambda
        else:
            StrP.F = wdprime

    else:
        pointer4 = StrP.F
        F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
        while F_pt_order == 1:
            F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
            pointer4 = pointer4.next
        StrP.F = pointer4

    pointer5, L_pt_order = StrP.L, 0
    while pointer5 != StrP.K.tail and L_pt_order == -1:
        L_pt_order = ccw(new_vertex, pointer5.prev, pointer5)
        pointer5 = pointer5.next

    StrP.L = pointer5

    return 1




def _convex(i, StrP):
    P = [tuple(x) for x in StrP.polygon.get_xy()]

    edge = (P[i+1][0] - P[i][0], P[i+1][1] - P[i][1])
    new_vertex = Node(P[i])
    new_lambda = Lambda(edge)
    new_lambda.prev, new_vertex.next = new_vertex, new_lambda

    if ccw(move(new_vertex, StrP.L), new_vertex, new_lambda) != 1:
        pointer1, K_edge_int = StrP.L, None
        while pointer1 != StrP.F and K_edge_int == None:
            K_edge_int = findIntersection(pointer1.prev, pointer1, new_vertex, new_lambda)
            pointer1 = pointer1.prev

        if K_edge_int == None:
            return -1

        wprime = Node(K_edge_int)

        pointer2, K_edge_int = StrP.L, None
        while pointer2 != StrP.K.tail and K_edge_int == None:
            K_edge_int = findIntersection(pointer2, pointer2.next, new_vertex, new_lambda)
            pointer2 = pointer2.next

        H_slope, T_slope = slope(StrP.K.head, StrP.K.head.next), slope(StrP.K.tail.prev, StrP.K.tail)
        edge_slope = slope(new_vertex, new_lambda)
        c = StrP.K.tail[0] * StrP.K.head[1] - StrP.K.head[0] * StrP.K.tail[1]
        t = StrP.K.tail[1] * new_lambda[0] - StrP.K.tail[0] * new_lambda[1]
        s = StrP.K.head[1] * new_lambda[0] - StrP.K.head[0] * new_lambda[1]

        if K_edge_int != None:
            wdprime = Node(K_edge_int)
            StrP.K.addNode(pointer1, wprime, pointer1.next)
            StrP.K.addNode(wprime, wdprime, pointer2)

        elif c * t >= 0 and c * s >= 0:
            StrP.K.addNode(pointer1, wprime, pointer1.next)
            StrP.K.addNode(wprime, new_lambda, None)
            pdb.set_trace()
            wdprime = None

        else:
            pointer3, K_edge_int = StrP.K.head, None
            while K_edge_int == None:
                K_edge_int = findIntersection(pointer3, pointer3.next, new_vertex, new_lambda)
                pointer3 = pointer3.next

            wdprime = Node(K_edge_int)
            StrP.K.addNode(pointer1, wprime, pointer1.next)
            StrP.K.addNode(pointer3.prev, wdprime, pointer3)
            StrP.K.setHead(wdprime)
            StrP.K.setTail(wprime)
            StrP.K.makeCircular()

        if wdprime == None:
            region = findRegion(new_vertex, wprime, Node(P[i+1]))
            if region == 0:
                StrP.L = new_lambda

                pointer4 = StrP.F
                F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
                while F_pt_order == 1:
                    F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
                    pointer4 = pointer4.next
                StrP.F = pointer4

            elif region == 1:
                #pdb.set_trace()
                StrP.F = wprime
                StrP.L = new_lambda

        else:
            region = findRegion(wprime, wdprime, Node(P[i+1]))
            if region == -1:
                StrP.L = wdprime

                pointer4 = StrP.F
                F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
                while F_pt_order == 1:
                    F_pt_order = ccw(new_vertex, pointer4, pointer4.next)
                    pointer4 = pointer4.next
                StrP.F = pointer4

            elif region == 0:
                StrP.F = wprime
                StrP.L = wdprime

            elif region == 1:
                StrP.F = wprime

                pointer5, L_pt_order = wdprime, 0
                while pointer5 != StrP.K.tail and L_pt_order == -1:
                    L_pt_order = ccw(new_vertex, pointer5.prev, pointer5)
                    pointer5 = pointer5.next

                StrP.L = pointer5

        return 1




def main():
    #Q = getInputPoly()
    '''
    print(Q._pts)
    print(Q.polygon.get_xy())
    print(Q.flex_dictionary)
    '''
    print(getKernel(P))


if __name__ == '__main__':
    main()

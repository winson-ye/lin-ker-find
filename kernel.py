import matplotlib.pyplot as plt
from Classes import *
import pdb

'''
Plot input polygon to compute getKernel
'''

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


'''
Compute kernel of a polygon
Input: StructuredPoly
Output: Polygon (matplotlib.patches)
'''
def getKernel(P):
    ker = P.k_list
    poly = P.polygon
    angle = P.flex_dictionary
    F = P.F_list
    L = P.L_list

# Check if there exists a reflex angle
    list_of_vertices = poly.get_xy()
    if angle[tuple(list_of_vertices[0])] == -1:
    # If so, make a K_0
        initial_node = Node(list_of_vertices[0])
        head_lambda = Lambda((list_of_vertices[1][0] - list_of_vertices[0][0], list_of_vertices[1][1] - list_of_vertices[0][1]))
        tail_lambda = Lambda((list_of_vertices[0][0] - list_of_vertices[-2][0], list_of_vertices[0][1] - list_of_vertices[-2][1]))

        head_lambda.next = initial_node
        head_lambda.prev = None

        initial_node.next = tail_lambda
        initial_node.prev = head_lambda

        tail_lambda.next = None
        tail_lambda.prev = initial_node

        ker.append(K(head_lambda, tail_lambda))
        F.append(head_lambda)
        L.append(tail_lambda)

    else:
        return poly

# Iterate over vertices, handle reflex and convex angles
    poly = poly.get_xy()
    print(poly)
    #print(range(len(poly) - 1))
    for i in range(len(poly) - 2):
        #print(i)
        if angle[tuple(poly[i])] == -1:
            result = _reflex(i, poly, ker, F, L)
        elif angle[tuple(poly[i])] == 1:
            pdb.set_trace()
            result = _convex(i, poly, ker, F, L)

        if result == -1:
            return Polygon([])

        plotA(ax, JeffsAlgorithm(ker[i]), F[i], L[i], i)
        ax.cla()

        '''
        print("F[" + str(i) + "]:\n")
        print(F[i])
        print("L[" + str(i) + "]:\n")
        print(L[i])

        print("K[" + str(i) + "]:\n")
        x = ker[i].head
        while (not x == None) and (not x == ker[i].tail):
            print(x)
            x = x.next
        print(x)
        print("\n\n\n\n\n")
        '''

    return JeffsAlgorithm(ker[len(poly) - 2])








'''
Reflex angle helper function for getKernel
'''
def _reflex(i, P, K, F, L):
    e = (P[i+1][0]-P[i][0], P[i+1][1]-P[i][1])
    lamb = Lambda(e)
    v = Node(P[i+1])
    lamb.next = v

# F is on or to the right of halfline Lambda e v
    #print("ccw: ", ccw(P[i], P[i+1], F[i]))
    if ccw(P[i], P[i+1], F[i]) != 1:
        x, y = F[i], F[i]

        #print("x:\n", x)
        while x != L[i] and findIntersection(lamb, v, x, x.next) == None:
            #print("x:\n", x)
            x = x.next
        if x == L[i]:
            return -1
        wprime = Node(findIntersection(lamb, v, x, x.next))

        while y != K[i].getHead() and findIntersection(lamb, v, y, y.prev) == None:
            #print("y:\n", y)
            y = y.prev
        wdprime = None
        if y != K[i].getHead():
            wdprime = Node(findIntersection(lamb, v, y, y.prev))

# Currently using the same instance for K[i+1] and K[i]
        K.append(K[i])
        x, y = x.next, y.prev
        head, tail = K[i].head, K[i].tail

        if wdprime != None:
            y.next = wdprime
            x.prev = wprime
            wprime.next = x
            wdprime.next = wprime
            wdprime.prev = y
            wprime.prev = wdprime

        elif slope(tail.prev, tail) >= slope(P[i], P[i+1]) >= slope(head, head.next) or slope(head, head.next) >= slope(P[i], P[i+1]) >= slope(tail.prev, tail):
            x.prev = wprime
            wprime.prev = lamb
            lamb.next = wprime
            wprime.next = x
            K[i+1].head = lamb

        else:
            z = tail
            while findIntersection(z.prev, z, P[i], P[i+1]) == None:
                z = z.prev
            wdprime = Node(findIntersection(z.prev, z, P[i], P[i+1]))
            z = z.prev
            K[i+1].head = wprime
            K[i+1].tail = wdprime
            x.prev = wprime
            wprime.next = x
            z.next = wdprime
            wdprime.prev = z
            wprime.prev = wdprime
            wdprime.next = wprime

        print("wdprime: ", wdprime)
        if wdprime != None:
            F.append(wdprime)
        else:
            F.append(lamb)

# F is strictly on left
    else:
        K.append(K[i])
        F.append(F[i])
        while F[i+1] != K[i+1].tail and (ccw(P[i+1], F[i+1], F[i+1].next) == 1):
            F[i+1] = F[i+1].next

# Compute next L node in K
    L.append(L[i])
    if L[i] != K[i+1].tail:
        X = L[i].next
        print(type(X))
        while X != K[i+1].tail and (ccw(P[i+1], X, X.next) == -1 and X != L[i]):
            X = X.next
        if X != L[i]:
            L[i+1] = X

    return 1








'''
Convex angle helper function for getKernel
'''
def _convex(i, P, K, F, L):
    e = (P[i+1][0] - P[i][0], P[i+1][1] - P[i][1])
    lamb = Lambda(e)
    v = Node(P[i])
    lamb.prev = v
    v.next = lamb

    '''
    print("lamb:\n", lamb)
    print("v:\n", v)
    '''

# L is on or to the right of Lambda e v
    if not (ccw(v, Node(P[i+1]), L[i]) == 1):
        x = L[i]
        y = L[i]
        while (not x == F[i]) and (findIntersection(lamb, v, x, x.prev) == None):
            #print("x:\n", x)
            x = x.prev
        if x == F[i]:
            return -1

        wprime = Node(findIntersection(lamb, v, x, x.prev))
        while (not y == K[i].getTail()) and (findIntersection(lamb, v, y, y.next) == None):
            #print("y:\n", y)
            y = y.next

        wdprime = None
        if (not y == K[i].getTail()):
            wdprime = Node(findIntersection(lamb, v, y, y.next))
        K.append(K[i])
        x, y = x.prev, y.next
        head, tail = K[i+1].head, K[i+1].tail

        if not (wdprime == None):
            wprime.next = wdprime
            wdprime.prev = wprime
            x.next = wprime
            wprime.prev = x
            y.prev = wdprime
            wdprime.next = y

        elif slope(tail.prev, tail) >= slope(P[i], P[i+1]) >= slope(head, head.next) or slope(head, head.next) >= slope(P[i], P[i+1]) >= slope(tail.prev, tail):
            x.next = wprime
            wprime.prev = x
            wprime.next = lamb
            lamb.prev = wprime
            K[i+1].tail = lamb

        else:
        # Flip else case from reflex (on line 103 to 116)
        #2.1.1
            z = head
            while findIntersection(z.next, z, Node(P[i]), Node(P[i+1])) == None:
                z = z.next
            wdprime = Node(findIntersection(z.next, z, Node(P[i]), Node(P[i+1])))
            z = z.next
            K[i+1].tail = wprime
            K[i+1].head = wdprime
            x.next = wprime
            wprime.prev = x
            z.prev = wdprime
            wdprime.next = z
            wprime.next = wdprime
            wdprime.prev = wprime

        if not wdprime == None:
            region = findRegion(wprime, wdprime, Node(P[i+1]))
            if region == -1:
                # Follow reflex for F[i+1]
                F.append(F[i])
                #the below line has F[i+1].next being None
                while(ccw(P[i+1], F[i+1], F[i+1].next) == 1):
                    F[i+1] = F[i+1].next
                L.append(wdprime)

            elif region == 0:
                F.append(wprime)
                L.append(wdprime)

            elif region == 1:
                F.append(wprime)
                # Follow reflex for L[i+1] except scan ccw from wdprime
                L.append(wdprime)
                X = wdprime.next
                while(ccw(P[i+1], X, X.next) == -1 and X != wdprime):
                    X = X.next
                if X != L[i]:
                    L[i+1] = X

        else:
            region = findRegion(v, wprime, Node(P[i+1]))
            if region == 0:
                # Follow reflex for F[i+1]
                F.append(F[i])
                while(ccw(P[i+1], F[i+1], F[i+1].next) == 1):
                    F[i+1] = F[i+1].next

            elif region == 1:
                F.append(wprime)
            L.append(lamb)

    else:
        K.append(K[i])
        # Follow reflex for F[i+1]
        F.append(F[i])
        #print("F[" + str(i) + "]:\n", F[i])
        while(ccw(P[i+1], F[i+1], F[i+1].next) == 1):
            #print(type(F[i]))
            F[i+1] = F[i+1].next

        if type(K[i+1].head) == Lambda:
            L.append(L[i])

        else:
            # Follow reflex for L[i+1]
            L.append(L[i])
            X = L[i].next
            while(ccw(P[i+1], X, X.next) == -1 and X != L[i]):
                X = X.next
            if X != L[i]:
                L[i+1] = X

    return 1








def JeffsAlgorithm(K):
    # Construct the Polygon
    vertices_array = []

    if (type(K.head) == Lambda) and (type(K.tail) == Lambda):
        cur_node = K.head.next

        bounding_box_corners = [Node((0, 0)), Node((100, 0)), Node((100, 100)), Node((0, 100))]

        # Append coords of all non-lambda nodes to vertices_array
        while cur_node != K.tail:
            vertices_array.append(cur_node.coords)
            cur_node = cur_node.next


        # Find where the head and tail lambdas intersect the bounding box
        head_box_intersection = None
        tail_box_intersection = None

        for i in range(4):
            if head_box_intersection == None:
                head_box_intersection = findIntersection(bounding_box_corners[i % len(bounding_box_corners)], bounding_box_corners[(i + 1) % len(bounding_box_corners)], K.head.next, K.head)

            if tail_box_intersection == None:
                tail_box_intersection = findIntersection(bounding_box_corners[i % len(bounding_box_corners)], bounding_box_corners[(i + 1) % len(bounding_box_corners)], K.tail.prev, K.tail)

            if head_box_intersection != None and tail_box_intersection != None:
                break

        # Append where the tail intersects the bounding box
        vertices_array.append(tail_box_intersection)


        # Find which side of the bounding box that the tail lambda intersects
        corner_index = 0
        if tail_box_intersection[0] == 0:
            corner_index = 0

        elif tail_box_intersection[1] == 0:
            corner_index = 1

        elif tail_box_intersection[0] == 100:
            corner_index = 2

        elif tail_box_intersection[1] == 100:
            corner_index = 3


        while ccw(Node(head_box_intersection), Node(tail_box_intersection), bounding_box_corners[corner_index % len(bounding_box_corners)]) == 1:
            vertices_array.append(bounding_box_corners[corner_index % len(bounding_box_corners)].coords)
            corner_index += 1

        vertices_array.append(head_box_intersection)
        vertices_array.append(K.head.next.coords)

        return Polygon(vertices_array)

    elif not (type(K.head) == Lambda) and not (type(K.tail) == Lambda):
        # K is a cyclic doubly linked list, so read each node into a Polygon object
        cur_node = K.head

        while cur_node != K.tail:
            vertices_array.append(cur_node.coords)
            cur_node = cur_node.next

        vertices_array.append(K.tail.coords)
        vertices_array.append(K.head.coords)

        return Polygon(vertices_array)

    else:
        print("JeffsAlgorithm:   Inputted kernel has one Lambda, NOT POSSIBLE")
        return None




'''def plotPoint(ax, x, y, label):
    ax.plot(x, y, marker='o', color='b')
    ax.annotate(label, xy=(x, y), xytext=(x + 10, y + 10))
    input("Press [enter] to continue.")
'''

def plotA(ax, p, F, L, i):
    ax.set_xlim(XLIM)
    ax.set_ylim(YLIM)
    p.set_alpha(0.4)
    p.set_color('r')
    ax.add_patch(P.polygon)
    ax.add_patch(p)
    ax.set_title("drawing K" + str(i))
    ax.legend(loc='upper left')

    if type(F) != Lambda:
        ax.plot(F.coords[0], F.coords[1], marker='o', label='F[' + str(i) + ']')
        #x.annotate('F[' + str(i) + ']', xy=(F.coords[0], F.coords[1]), xytext=(F.coords[0]+10, F.coords[1]+10))
    if type(L) != Lambda:
        ax.plot(L.coords[0], L.coords[1], marker='o', label='L[' + str(i) + ']')
        #ax.annotate('L[' + str(i) + ']', xy=(L.coords[0], L.coords[1]), xytext=(L.coords[0]+10, L.coords[1]+10))

    plt.legend()

    input("Press [enter] to continue.")



def main():

    # P = getInputPoly()

    # P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 2), (2, 8), (10, 8), (10, 10), (0, 10)])
    #P = StructuredPoly([(0, 10), (0, 0), (10, 0), (10, 2), (2, 4), (2, 6), (10, 8), (10, 10), (0, 10)])
    #P = StructuredPoly([(0,0), (10,10), (0,20), (20,10), (0,0)])
    #P = StructuredPoly([0, 50], [30, 70], [50, 100], [70, 70], [100, 50], [70, 30], [50, 0], [30, 30])


    #print(P.flex_dictionary)
    #print(P.polygon.get_xy(), "\n")

    '''
    L = Lambda([1, 1])
    L.next = Node([1, 1])
    print(L)
    '''

    #print("ccw", ccw((2, 4), (2, 6), (10, 8)))

    plt.ion()
    plt.show()

    q = getKernel(P)
    #print(q.get_xy())



    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.2)
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])

    plotKi(ax, q, "K")
    plt.show()
    '''

    '''
    print(ccw([33.66935484, 32.78186275], [48.79032258, 44.73039216], [69.55645161, 45.95588235]))
    print(ccw([48.79032258, 44.73039216], [69.55645161, 45.95588235], [39.91935484, 75.06127451]))
    print(ccw([69.55645161, 45.95588235], [39.91935484, 75.06127451], [33.66935484, 32.78186275]))
    print(ccw([39.91935484, 75.06127451], [33.66935484, 32.78186275], [48.79032258, 44.73039216]))
    '''

    #print(P.polygon.get_xy())
    #print(P.flex_dictionary)

if __name__ == '__main__':
    main()

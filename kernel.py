import matplotlib.pyplot as plt
from Classes import *
from Global_Functions import *
from test.py import *


'''
Plot input polygon to compute getKernel
'''
def getInputPoly():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('click done to create your polygon')
    plt.subplots_adjust(bottom=0.2)

    axdone = plt.axes([0.81, 0.05, 0.1, 0.075])
    bdone = Button(axdone, 'Done')

    line, = ax.plot([], [], marker = 'o')
    linebuilder = LineBuilder(line)
    bdone.on_clicked(linebuilder._finish)

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

# Check if there exists a reflex angle
    list_of_vertices = poly.get_xy()
    if angle[list_of_vertices[0]] == -1:
    # If so, make a K_0
        initial_node = Node(first_point)
        tail_lambda = Lambda((list_of_vertices[0][0] - list_of_vertices[1][0], list_of_vertices[0][1] - list_of_vertices[1][1]))
        head_lambda = Lambda((list_of_vertices[0][0] - list_of_vertices[-2][0], list_of_vertices[0][1] - list_of_vertices[-2][1]))

        head_lambda.next = initial_node
        head_lambda.prev = None

        initial_node.next = tail_lambda
        initial_node.prev = head_lambda

        tail_lambda.next = None
        tail_lambda.prev = initial_node

        ker.append(K(head_lambda, tail_lambda))

    else:
        return poly

# Iterate over vertices, handle reflex and convex angles
    for i in range(len(poly) - 1):
        if angle[P[i]] == -1:
            result = _reflex(i, poly, ker, F, L)
            if result == -1:
                return Polygon([])
        elif angle[P[i]] == 1:
            _convex(i, poly, ker, F, L)


'''
Reflex angle helper function for getKernel
'''
def _reflex(i, P, K, F, L):
    e = (P[i+1][0]-P[i][0], P[i+1][1]-P[i][1])
    lamb = Lambda(e)
    lamb.next = P[i+1]

# F is on or to the right of halfline Lambda e v
    if ccw(P[i], P[i+1], F[i]) != 1:
        x, y = F[i], F[i]
        v = Node(P[i+1])
        lamb.next = v

        while x != L[i] and findIntersection(lamb, v, x, x.next) == None:
            x = x.next
        if x == L[i]:
            return -1
        wprime = Node(findIntersection(lamb, v, x, x.next))

        while y != K[i].getHead() and findIntersection(lamb, v, y, y.prev) == None:
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

        if wdprime != None:
            F.append(wdprime)
        else:
            F.append(lamb)

# F is strictly on left
    else:
        K.append(K[i])
        F.append(F[i])
        while(ccw(F[i+1].prev, F[i+1], F[i+1].next) == 1):
            F[i+1] = F[i].next

# Compute next L node in K
    L.append(L[i])
    X = L[i].next
    while(ccw(X.prev, X, X.next) == -1 and X != L[i]):
        X = X.next
    if X != L[i]:
        L[i+1] = X

    return 1


'''
Convex angle helper function for getKernel
'''
def _convex(i, P, K, F, L):
    pass



def JeffsAlgorithm(K):
    # Construct the Polygon 
    if (type(K.head) == Lambda) && (type(K.tail) == Lambda):
        return
    elif !(type(K.head) == Lambda) && !(type(K.tail) == Lambda):
        return
    else:
        print("JeffsAlgorithm:   Inputted kernel has one Lambda, NOT POSSIBLE")
        return None

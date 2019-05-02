import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
from matplotlib.widgets import Button
import pdb

XLIM = [0, 100]
YLIM = [0, 100]

class __BasicNode:
    def __init__(self):
        self.next = None
        self.prev = None

    def setNext(self, nxt):
        self.next = nxt
        return

    def setPrev(self, prev):
        self.prev = prev
        return

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev




class Node(__BasicNode):
    def __init__(self, coords):
        super().__init__();
        self.coords = coords

    def setCoords(self, coords):
        self.coords = coords
        return

    def getCoords(self):
        return self.coords

    def __getitem__(self, i):
        return self.coords[i]

    def __len__(self):
        return len(self.coords)

    def __eq__(self, other):
        if type(other) != Node:
            return False
        return self.coords == other.coords

    def __str__(self):
        # Class type
        class_type = str(type(self)) + "\n"

        # Coords
        coords = str(self.coords) + "\n"

        neighbors = "\n" + "Next:   " + str(type(self.next)) + "\nPrev: " + str(type(self.prev)) + "\n"

        return "--------------------\n" + class_type + coords + neighbors + "--------------------\n"




class Lambda(__BasicNode):
    def __init__(self, direction):
        super().__init__()
        self.direction = direction

    def setDirection(self, direction):
        self.direction = direction
        return

    def getDirection(self):
        return self.direction

    def __getitem__(self, i):
        return self.direction[i]

    def __len__(self):
        return len(self.direction)

    def __eq__(self, other):
        if type(other) != Lambda:
            return False
        if self.next == None:
            return self.direction == other.direction and self.prev.coords == other.prev.coords
        return self.direction == other.direction and self.next.coords == other.next.coords


    def __str__(self):
        # Class type
        class_type = str(type(self)) + "\n"

        # Head/tail lambda
        lambda_type = ""
        if self.next == None and type(self.prev) == Node:
            lambda_type += "Tail Lambda"

        elif type(self.next) == Node and self.prev == None:
            lambda_type += "Head Lambda"

        else:
            lambda_type += "Neither Head or Tail Lambda"

        lambda_type += "\n" + "Next:    " + str(type(self.next)) + "\nPrev: " + str(type(self.prev)) + "\n"


        # Direction
        direction = str(self.direction) + "\n"


        return "--------------------\n" + class_type + lambda_type + direction + "--------------------\n"




class K:
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def addHead(self, head):
        head.next = self.head

        if not self.head == None:
            self.head.prev = head

        self.head = head
        return

    def setHead(self, head):
        self.head = head
        return

    def addTail(self, tail):
        tail.prev = self.tail
        tail.next = None

        if not self.tail == None:
            self.tail.next = tail

        self.tail = tail
        return

    def setTail(self, tail):
        self.tail = tail
        return

    def addNode(self, before, node, after):
        if before == None:
            self.setHead(node)
        else:
            before.next = node
            node.prev = before

        if after == None:
            self.setTail(node)
        else:
            after.prev = node
            node.next = after
        return

    def makeCircular(self):
        self.tail.next = self.head
        self.head.prev = self.tail

    def getHead(self):
        return self.head

    def getTail(self):
        return self.tail

    def __str__(self):
        self.tail = self.head.prev
        pointer = self.head
        count = 1
        string = "\n"
        #pdb.set_trace()
        string += "Node " + str(count) + ":\n" + str(pointer) + "\n"
        count += 1
        pointer = pointer.next
        while pointer != self.tail and pointer != self.head:
            string += "Node " + str(count) + ":\n" + str(pointer) + "\n"
            count += 1
            pointer = pointer.next
            #pdb.set_trace()
        string += "Node " + str(count) + ":\n" + str(pointer) + "\n"
        return string




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




class StructuredPoly:
    def __init__(self, list_of_vertices = []):
        self._pts = self.orientVert(list_of_vertices)
        self.K = K(None, None)
        self.flex_dictionary = self.setFlex()
        self.polygon = Polygon(self._pts)
        self.F = None
        self.L = None


    def setFlex(self):



        '''
        Get an oriented list of vertices that will show me which way to walk around the polygon
        using orientVert
        '''

        oriented = self._pts
        flexes = dict()

        last = len(oriented)

        '''
        I want to go around oriented until I find start reflex vertex
        '''

        '''
        i = 0
        j = 1
        k = 2
        while not i == last:

            reflex_index = j
            if ccw(oriented[i % last], oriented[j % last], oriented[k % last]) == -1:
                #found starting reflex vertex
                break

            i += 1
            j += 1
            k += 1
        '''

        '''
        Now start labeling the vertices starting from reflex_index
        '''

        i = -1 % last
        j = 0 % last
        k = 1 % last

        while len(flexes) < len(oriented):
            #print("(", i, oriented[i], ") (", j,  oriented[j], ") (", k, oriented[k], ")", ccw(oriented[i], oriented[j], oriented[k]))
            if ccw(oriented[i], oriented[j], oriented[k]) == -1:
                #mark point j as reflex
                flexes[oriented[j]] = -1
            else:
                #mark point j as convex
                flexes[oriented[j]] = 1

            i = (i + 1) % last
            j = (j + 1) % last
            k = (k + 1) % last


        lst, added = [], dict()
        for v in range(len(self._pts)):
            if lst == []:
                if  flexes[oriented[v]] == -1:
                    lst.append(oriented[v])
                    added.update({oriented[v]: 1})
                else:
                    added.update({oriented[v]: 0})
            else:
                lst.append(oriented[v])
                added.update({oriented[v]: 1})

        for v in range(len(self._pts)):
            if added[oriented[v]] == 0:
                lst.append(oriented[v])
                added[oriented[v]] = 1

        self._pts = lst


        return flexes

    def orientVert(self, list_of_vertices):
        '''
        This is essentially Keegan's proposed algorithm.
        '''

        oriented = []
        '''
        pick leftmost point or lowest point
        '''
        v0_index = list_of_vertices.index(sorted(list_of_vertices, key=lambda k: [k[0], k[1]])[0])
        oriented.append(list_of_vertices[v0_index])

        last = len(list_of_vertices) - 1

        '''
        compare slopes
        '''
        dir1 = slope(Node(list_of_vertices[v0_index % last]), Node(list_of_vertices[(v0_index + 1) % last]))
        dir2 = slope(Node(list_of_vertices[v0_index % last]), Node(list_of_vertices[(v0_index - 1) % last]))

        '''walk in the direction of lowest slope'''

        if dir1 < dir2:

            vi_index = (v0_index + 1) % last

            while vi_index != v0_index:
                oriented.append(list_of_vertices[vi_index])
                vi_index = (vi_index + 1) % last

        elif dir2 < dir1:

            vi_index = (v0_index - 1) % last

            while vi_index != v0_index:
                oriented.append(list_of_vertices[vi_index])
                vi_index = (vi_index - 1) % last

        return oriented




def det2x2(a, b, c, d):
    #   [a, b;
    #    c, d]
    return a * d - b * c




def det3x3(a, b, c, d, e, f, g, h, i):
    #   [a, b, c;
    #    d, e, f;
    #    g, h, i]
    return (a * det2x2(e, f, h, i)) - (b * det2x2(d, f, g, i)) + (c * det2x2(d, e, g, h))




def ccw(a, b, c):

    if type(a) == None or type(b) == None or type(c) == None:
        raise TypeError(a, b, c)

    determinant = 0

    if type(a) == Lambda or type(b) == Lambda or type(c) == Lambda:
        # Cycle the input order so that the Lambda is the last input argument of the ccw() function
        if type(a) == Lambda:
            return ccw(b, c, a)

        elif type(b) == Lambda:
            return ccw(c, a, b)

        else:
            # Check if the direction of Lambda is the same as the direction from point a to point b
            if c[0] * (b[1] - a[1]) == c[1] * (b[0] - a[0]):
                if type(c.next) == Node:
                    return ccw(a, b, c.next)

                elif type(c.prev) == Node:
                    return ccw(a, b, c.prev)

            else:
                # In this case, Lambda and the vector from a to b are not the same
                if type(c.next) == Node:
                    # Lambda is the head of the linked list
                    determinant = c[0] * b[1] - c[1] * b[0] + c[1] * a[0] - c[0] * a[1]

                elif type(c.prev) == Node:
                    # Lambda is the tail of the linked list
                    determinant = c[1] * b[0] - c[0] * b[1] + c[0] * a[1] - c[1] * a[0]


                if determinant < 0:
                    return -1

                elif determinant > 0:
                    return 1

                else:
                    return 0


    else:
        determinant = det2x2(a[0] - c[0], b[0] - c[0], a[1] - c[1], b[1] - c[1])
        #determinant = det3x3(a[0], b[0], c[0], a[1], b[1], c[1], 1, 1, 1)
        '''
        print("ccw()")
        print(a)
        print(b)
        print(c)
        print(str(det3x3(a[0], b[0], c[0], a[1], b[1], c[1], 1, 1, 1)))
        '''
        if determinant == 0:
            return 0
        elif determinant > 0:
            return 1
        else:
            return -1



def findIntersection(v1, v2, u1, u2):


    p1 = p2 = q1 = q2 = None
    v1_v2_is_ray = False
    u1_u2_is_ray = False

    ### Handle the inputs v1 and v2 and determine if they denote a line segment or ray
    # If v1 is a Lambda and v2 is a Node or vice versa
    if ((type(v1) == Lambda) and (type(v2) == Node)) or ((type(v1) == Node) and (type(v2) == Lambda)):
        v1_v2_is_ray =  True

        if type(v1) == Lambda:
            p1 = v2.coords

            if type(v1.next) == Node:
                p2 = (v2.coords[0] - v1.direction[0], v2.coords[1] - v1.direction[1])

            elif type(v1.prev) == Node:
                p2 = (v2.coords[0] + v1.direction[0], v2.coords[1] + v1.direction[1])

        elif type(v2) == Lambda:
            p1 = v1.coords

            if type(v2.next) == Node:
                p2 = (v1.coords[0] - v2.direction[0], v1.coords[1] - v2.direction[1])

            elif type(v2.prev) == Node:
                p2 = (v1.coords[0] + v2.direction[0], v1.coords[1] + v2.direction[1])

    # If v1 and v2 are both Nodes
    elif ((type(v1) == Node) and (type(v2) == Node)):
        p1 = v1.coords
        p2 = v2.coords

    # If v1 and v2 are both Lambdas
    elif ((type(v1) == Lambda) and (type(v2) == Lambda)):
        raise ValueError("findIntersect:    BOTH v1 AND v2 ARE LAMBDAS. UNDEFINIED BEHAVIOR.")

    else:
        raise ValueError("findIntersect:    YOU REALLY GOOFED IN INPUTTING v1 AND v2")


    ### Handle the inputs u1 and u2 and determine if they denote a line segment or ray
    # If u1 is a Lambda and u2 is a Node or vice versa
    if ((type(u1) == Lambda) and (type(u2) == Node)) or ((type(u1) == Node) and (type(u2) == Lambda)):
        u1_u2_is_ray = True

        if type(u1) == Lambda:
            q1 = u2.coords

            if type(u1.next) == Node:
                q2 = (u2.coords[0] - u1.direction[0], u2.coords[1] - u1.direction[1])

            elif type(u1.prev) == Node:
                q2 = (u2.coords[0] + u1.direction[0], u2.coords[1] + u1.direction[1])

        elif type(u2) == Lambda:
            q1 = u1.coords

            if type(u2.next) == Node:
                q2 = (u1.coords[0] - u2.direction[0], u1.coords[1] - u2.direction[1])

            elif type(u2.prev) == Node:
                q2 = (u1.coords[0] + u2.direction[0], u1.coords[1] + u2.direction[1])

    # If u1 and u2 are both Nodes
    elif ((type(u1) == Node) and (type(u2) == Node)):
        q1 = u1.coords
        q2 = u2.coords

    # If u1 and u2 are both Lamdas
    elif ((type(u1) == Lambda) and (type(u2) == Lambda)):
        raise ValueError("findIntersect:    BOTH u1 AND u2 ARE LAMBDAS. UNDEFINIED BEHAVIOR.")

    else:
        # print("findIntersect: YOU REALLY GOOFED IN INPUTTING u1 AND u2")
        raise ValueError('findIntersect:    YOU REALLY GOOFED IN INPUTTING u1 AND u2')


    ### Compute intersection
    determinant = det2x2(q2[0] - q1[0], p1[0] - p2[0], q2[1] - q1[1], p1[1] - p2[1])

    if determinant == 0:
        print("Determinant is 0")
        return None


    t0 = (((q1[1] - q2[1]) * (p1[0] - q1[0])) + ((q2[0] - q1[0]) * (p1[1] - q1[1]))) / determinant
    t1 = (((p1[1] - p2[1]) * (p1[0] - q1[0])) + ((p2[0] - p1[0]) * (p1[1] - q1[1]))) / determinant

    intersection = (p1[0] + t0 * (p2[0] - p1[0]), p1[1] + t0 * (p2[1] - p1[1]))
    #intersection1 = (q1[0] + t1 * (q2[0] - q1[0]), q1[1] + t1 * (q2[1] - q1[1]))
    #print("Bool:   " + str(intersection == intersection1))
    #print("t0: " + str(t0))
    #print("t1: " + str(t1))
    #rint("intersection:    " + str(intersection))
    #print("intersection1:  " + str(intersection1))


    ### Interpret parametrization values based on input types
    #print("v1_v2_is_ray:   " + str(v1_v2_is_ray))
    #print("u1_u2_is_ray:   " + str(u1_u2_is_ray))

    if v1_v2_is_ray and u1_u2_is_ray:
        if (t0 >= 0) and (t1 >= 0):
            return intersection

    elif v1_v2_is_ray and not u1_u2_is_ray:
        if (t0 >= 0) and (0 <= t1 <= 1):
            return intersection

    elif not v1_v2_is_ray and u1_u2_is_ray:
        if (0 <= t0 <= 1) and (t1 >= 0):
            return intersection

    elif not v1_v2_is_ray and not u1_u2_is_ray:
        if (0 <= t0 <= 1) and (0 <= t1 <= 1):
            return intersection

    print("No intersection")
    return None
    #print("Final return")
    #raise ValueError("findIntersection: YOU DONE GOOFED")


def slope(v1, v2):
    if (type(v1) == Lambda) and (type(v2) == Lambda):
        print("DOUBLE LAMBDAS. DO SOMETHING ABOUT IT")

    elif (type(v1) == Lambda):
        if v1.direction[0] == 0:
            # print("slope: Divide by 0")
            if v1.direction[1] < 0:
                return float("-inf")
            elif v1.direction[1] > 0:
                return float("inf")
            return 0.0
        else:
            return v1.direction[1] / v1.direction[0]

    elif (type(v2) == Lambda):
        if v2.direction[0] == 0:
            # print("slope: Divide by 0")
            if v2.direction[1] < 0:
                return float("-inf")
            elif v2.direction[1] > 0:
                return float("inf")
            return 0.0
        else:
            return v2.direction[1] / v2.direction[0]

    else:
        den = (v2[0] - v1[0])
        num = (v2[1] - v1[1])
        if den == 0:
            # print("slope:   Divide by 0")
            if num < 0:
                return float("-inf")
            elif num > 0:
                return float("inf")
            return 0.0
        return num / den

    raise ValueError("Slope:    error")




def edgeDirection(n1, n2):
    return (n2[0] - n1[0], n2[1] - n1[1])




def dot(x, y):
    return sum(x[i] * y[i] for i in range(len(x)))




def move(start, direction):

    if type(direction) == Node:
        return direction

    if type(direction) == Lambda:

        if direction.next == None:
            return Node((start[0] + direction[0], start[1] + direction[1]))

        else:
            return Node((start[0] - direction[0], start[1] - direction[1]))




def findRegion(wprime, wdprime, v_iplus1):
    # Set t = 0 at wprime
    # Set t = 1 at wdprime
    # Find t for v_iplus1
    # return:
    #   -1 , t < 0
    #   0  , 0 <= t <= 1
    #   1  , t > 1


    diff_1 = (v_iplus1.coords[0] - wprime.coords[0], v_iplus1.coords[1] - wprime.coords[1])
    diff_2 = (wdprime.coords[0] - wprime.coords[0], wdprime.coords[1] - wprime.coords[1])

    dot_product = diff_1[0] * diff_2[0] + diff_1[1] * diff_2[1]

    if dot_product < 0:
        return -1

    else:
        den = ((diff_2[0] ** 2) + (diff_2[1] ** 2))
        if den != 0:
            square_l2_norm_ratio = ((diff_1[0] ** 2) + (diff_1[1] ** 2)) / den
        else:
            square_l2_norm_ratio = float("inf")

        if 0 <= square_l2_norm_ratio <= 1:
            return 0

        elif square_l2_norm_ratio > 1:
            return 1

        else:
            print("findRegion:  square_l2_norm_ratio is negative when that's impossible")

def plotA(ax, ker_tup, F, L, i, shape, head, tail):
    #pdb.set_trace()


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
    
    shape.set_alpha(0.5)


    ax.add_patch(shape)
    ax.add_patch(k)
    
    ax.set_title("drawing K" + str(i))

    if type(F) != Lambda:
        ax.plot(F.coords[0], F.coords[1], marker='s', label='F[' + str(i) + ']', color='r', alpha=0.8, markersize=8)

    if type(L) != Lambda:
        ax.plot(L.coords[0], L.coords[1], marker='o', label='L[' + str(i) + ']', color='k', alpha=0.8, markersize=8)

    if type(head) != Lambda:
        ax.plot(head.coords[0], head.coords[1], marker='*', label='H[' + str(i) + ']', color='g', alpha=0.8, markersize=8)

    if type(tail) != Lambda:
        ax.plot(tail.coords[0], tail.coords[1], marker='d', label='T[' + str(i) + ']', color='c', alpha=0.8, markersize=8)

    ax.legend(loc='upper left')

    input("Press [enter] to continue.")

def JeffsAlgorithm(K):

    #pdb.set_trace()

    if type(K.head) == Lambda and type(K.tail) == Lambda:

        cur_node, int_dct_H, t_dct = K.head, dict(), dict()
        bounding_box_corners = [Node((XLIM[0], YLIM[0])), Node((XLIM[1], YLIM[0])), Node((XLIM[1], YLIM[1])), Node((XLIM[0], YLIM[1]))]
        #pdb.set_trace
        while cur_node != K.tail and not int_dct_H:
            for i in range(4):
                intersection = findIntersection(bounding_box_corners[i % 4], bounding_box_corners[(i+1) % 4], cur_node, cur_node.next)

                if intersection != None:
                    int_dct_H[i] = Node(intersection)

            cur_node = cur_node.next

        first_node = cur_node
        cur_node = cur_node.prev
        print(int_dct_H)
        if not int_dct_H:
            ##pdb.set_trace()
            return (Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)]), -1)

        for key, value in int_dct_H.items():
            if cur_node == K.head:
                if cur_node[0] == 0:
                    t_dct[key] = (value[1] - cur_node.next[1]) / (-cur_node[1])
                else:
                    t_dct[key] = (value[0] - cur_node.next[0]) / (-cur_node[0])

            elif cur_node == K.tail:
                ##pdb.set_trace()
                return Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)], -1)

            else:
                ##pdb.set_trace()
                if cur_node[0] == 0:
                    t_dct[key] = (value[1] - cur_node.next[1]) / (cur_node[1] - cur_node.next[1])
                else:
                    t_dct[key] = (value[0] - cur_node.next[0]) / (cur_node[0] - cur_node.next[0])

        m = max(t_dct.values())
        for key in t_dct.keys():
            if t_dct[key] == m:
                k = key
                break
        head_intersect = int_dct_H[k]


        cur_node, int_dct_F, t_dct = K.tail, dict(), dict()
        bounding_box_corners = [Node((XLIM[0], YLIM[0])), Node((XLIM[1], YLIM[0])), Node((XLIM[1], YLIM[1])), Node((XLIM[0], YLIM[1]))]

        while cur_node != K.head and not int_dct_F:
            for i in range(4):
                intersection = findIntersection(bounding_box_corners[i % 4], bounding_box_corners[(i+1) % 4], cur_node.prev, cur_node)

                if intersection != None:
                    int_dct_F[i-1] = Node(intersection)

            cur_node = cur_node.prev

        last_node = cur_node
        cur_node = cur_node.next

        ##pdb.set_trace()
        if not int_dct_F:
            return Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)], -1)

        for key, value in int_dct_F.items():
            if cur_node == K.tail:
                if cur_node[0] == 0:
                    t_dct[key] = (value[1] - cur_node.prev[1]) / cur_node[1]
                else:
                    t_dct[key] = (value[0] - cur_node.prev[0]) / cur_node[0]

            else:
                if cur_node[0] == 0:
                    t_dct[key] = (value[1] - cur_node.prev[1]) / (cur_node[1] - cur_node.prev[1])
                else:
                    t_dct[key] = (value[0] - cur_node.prev[0]) / (cur_node[0] - cur_node.prev[0])

        m = max(t_dct.values())
        for key in t_dct.keys():
            if t_dct[key] == m:
                k = key
                break
        tail_intersect = int_dct_F[k]

        #pdb.set_trace()

        if head_intersect.coords == tail_intersect.coords:
            return Polygon([(-1000, -1000), (-1000.000000001, -1000), (-1000, -1000.0000000001), (-1000, -1000)], -1)


        corner_index = 0
        if tail_intersect[0] == 0:
            corner_index = 0

        elif tail_intersect[1] == 0:
            corner_index = 1

        elif tail_intersect[0] == 100:
            corner_index = 2

        elif tail_intersect[1] == 100:
            corner_index = 3
        #pdb.set_trace()


        pt_lst, cur_node = [head_intersect.coords], first_node
        while cur_node != last_node:
            pt_lst.append(cur_node.coords)
            cur_node = cur_node.next
        pt_lst.append(last_node.coords)
        pt_lst.append(tail_intersect.coords)
        while ccw(head_intersect, tail_intersect, bounding_box_corners[corner_index % 4]) == 1:
            pt_lst.append(bounding_box_corners[corner_index % 4].coords)
            corner_index += 1
        pt_lst.append(pt_lst[0])

        return (Polygon(pt_lst), 1)


    elif type(K.head) != Lambda and type(K.tail) != Lambda:
        bounded_polygon_list = []

        cur_node = K.head
        while cur_node != K.tail:
            bounded_polygon_list.append((cur_node[0], cur_node[1]))
            cur_node = cur_node.next

        bounded_polygon_list.append((K.tail[0], K.tail[1]))
        bounded_polygon_list.append((K.head[0], K.head[1]))

        return (Polygon(bounded_polygon_list), 1)

    else:
        raise ValueError("JeffsAlgorithm:\tGiven a Kernel with a single Lambda")




def main():
    '''
    Class testing
    node = Node((1, 1))
    print(node.getCoords())
    node.setCoords((2, 2))
    print(node.getCoords())

    lam = Lambda()
    print(lam.getDirection())
    lam.setDirection(3)
    print(lam.getDirection())


    k = K()
    poly = StructuredPoly([(0, 0), (1, 0), (0, 1)])
    '''

    '''
    Global functions testing

    #print(ccw((0, 0), [0, -1], (0, 1)))

    #print(findIntersection((-1, 0), (1, 0), (0, 1), (0, -1)))

    #print(slope(Node(1, 1), Node(2, 2)))


    #v1 = Node((-1, 0))
    #v2 = Node((1, 0))
    #u1 = Node((0, 1))
    #u2 = Node((0, -1))

    #w1 = Lambda((-2, 0))
    #w1.prev = v2
    '''
    #print(findIntersection(Node([1, 2]), Node([1, 4]), Node([0, 3]), Node([2, 3])))

    L = Lambda((1, 0))
    N = Node((0, 0))
    L2 = Lambda((2, 3))
    L.next, N.prev = N, L
    N.next, L2.prev = L2, N
    k = K(L, L2)
    k.addNode(N, Node((5, 5)), L2)
    print(k)
    '''
    print(findIntersection(Node((-10, 2)), Node((-10, -2)), L, N))
    '''


if __name__ == '__main__':
    main()

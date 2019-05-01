from Classes import *

def getKernel(poly):
    '''
    input: polygon
    output: kernel
    '''

    #build K1 from first vertex
    coords = [tuple(x) for x in poly.polygon.get_xy()]
    start = Node(coords[0])

    head = Lambda( (coords[1][0] - coords[0][0], coords[1][1] - coords[0][1]) )
    tail = Lambda( (coords[0][0] - coords[-2][0], coords[0][1] - coords[-2][1]))

    head.next = start
    head.prev = None
    start.prev = head
    start.next = tail
    tail.prev = start
    tail.next = None

    kernel = K(head, tail)

    poly.kernel = kernel 
    poly.F = head
    poly.L = tail

    #iterate over remaining vertices
    for i in range(1, len(poly) - 2):
        if poly.flex_dictionary[poly.polygon[i]] == -1:
            reflex()
        elif poly.flex_dictionary[poly.polygon[i]] == 1:
            convex()


def reflex(i, poly):

    points = poly.polygon.get_xy()

    if ccw(points[i], points[i+1], poly.F) != -1:



def convex(i, poly):

    points = poly.polygon.get_xy()

    lamb = Lambda((points[i+1][0] - points[i][0], points[i+1][1] - points[i][1]))
    base_point = Node(points[i])

    base_point.next = lamb
    lamb.prev = base_point

    base_point.prev = None
    lamb.next = None

    if ccw(points[i], points[i+1], poly.L) != 1:

        kernel_crawler = poly.L

        while kernel_crawler != F and findIntersection(base_point, lamb, kernel_crawler, kernel_crawler.prev) != None:
            kernel_crawler = kernel_crawler.prev

        if kernel_crawler == F:
            return -1

        wprime = Node(findIntersection(base_point, lamb, kernel_crawler, kernel_crawler.prev))

        kernel_crawler = poly.L

        while kernel_crawler != poly.kernel.tail and findIntersection(base_point, lamb, kernel_crawler, kernel_crawler.next) != None:
            kernel_crawler = kernel_crawler.next

        






def main():
    getKernel(StructuredPoly([(0, 50), (30, 70), (50, 100), (70, 70), (100, 50), (70, 30), (50, 0), (30, 30), (0, 50)]))

if __name__ == '__main__':
    main()

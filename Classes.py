import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math


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
	def __init__(self, coords = None):
		super().__init__();
		self.coords = coords

	def setCoords(self, coords):
		self.coords = coords
		return

	def getCoords(self):
		return self.coords

	def __getitem__(self, i):
		return self.coords[i]




class Lambda(__BasicNode):
	def __init__(self, direction = None):
		super().__init__()
		self.direction = direction

	def setDirection(self, direction):
		self.direction = direction
		return

	def getDirection(self):
		return self.direction

	def __getitem__(self, i):
		return self.direction[i]



class K:
	def __init__(self, head = None, tail = None):
		self.head = head
		self.tail = tail

	def setHead(self, head):
		self.head = head
		return

	def setTail(self, tail):
		self.tail = tail
		return

	def getHead(self):
		return self.head

	def getTail(self):
		return self.tail




class StructuredPoly:
	def __init__(self, list_of_vertices = []):
		self.polygon = Polygon(list_of_vertices)
		self.k_list = list()
		self.flex_dictionary = self.setFlex(list_of_vertices)
		self.F_list = list()
		self.L_list = list()


	def setFlex(self, list_of_vertices):

		'''
		Get an oriented list of vertices that will show me which way to walk around the polygon
		using orientVert
		'''

		oriented = self.orientVert(list_of_vertices)
		flexes = dict()

		last = len(oriented) - 1
		
		'''
		I want to go around oriented until I find start reflex vertex
		'''
		while i != 0:
			i = 0
			j = 0
			k = 0

			if gbl.ccw(oriented[i], oriented[j], oriented[k]) == -1:
				#found starting reflex vertex
				reflex_index = j
				break
				
			i = (i + 1) % last
			j = (j + 2) % last
			k = (k + 3) % last

		'''
		Now start labeling the vertices starting from reflex_index
		'''

		i = reflex_index
		j = (reflex_index + 1) % last
		k = (reflex_index + 2) % last

		while len(flexes) < len(oriented):

			if gbl.ccw(oriented[i], oriented[j], oriented[k] == -1):
				#mark point j as reflex
				flexes[oriented[j]] = -1
			else:
				#mark point j as convex
				flexes[oriented[j]] = 1

			i = (i + 1) % last
			j = (j + 2) % last
			k = (k + 3) % last

		return flexes

	def orientVert(self, list_of_vertices):
		'''
		This is essentially Keegan's proposed algorithm.
		'''

		oriented = []
		'''
		pick leftmost point or lowest point
		'''
		v0_index = list_of_vertices.index(sorted(list_of_vertices, key=lambda k: [k[1], k[0]])[0])
		oriented.append(list_of_vertices[v0_index])

		last = len(list_of_vertices) - 1

		'''
		compare slopes
		'''
		dir1 = gbl.slope(Node(list_of_vertices[v0_index % last]), Node(list_of_vertices[(v0_index + 1) % last]))
		dir2 = gbl.slope(list_of_vertices[(v0_index - 1) % last], list_of_vertices[v0_index])

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
	#	[a, b;
	#	 c, d]
	return a * d - b * c




def det3x3(a, b, c, d, e, f, g, h, i):
	#	[a, b, c;
	#	 d, e, f;
	#	 g, h, i]
	return (a * det2x2(e, h, i, f)) - (b * det2x2(d, f, g, i)) + (c * det2x2(d, e, g, h))



def ccw(a, b, c):
	# It is assumed that inputs a, b, and c are lists/tuples of numbers of size 2
	determinant = det2x2(a[0] - c[0], b[0] - c[0], a[1] - b[1], b[1] - c[1])

	if determinant == 0:
		return 0
	elif determinant > 0:
		return 1
	else:
		return -1



def findIntersection(v1, v2, u1, u2):
	p1 = p2 = q1 = q2 = None
	v1_v2_is_ray = u1_u2_is_ray = False

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
		print("findIntersect:	BOTH v1 AND v2 ARE LAMBDAS. UNDEFINIED BEHAVIOR.")
		return None

	else:
		print("findIntersect:	YOU REALLY GOOFED IN INPUTTING v1 AND v2")
		return None


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
		print("findIntersect:	BOTH u1 AND u2 ARE LAMBDAS. UNDEFINIED BEHAVIOR.")
		return None

	else:
		print("findIntersect:	YOU REALLY GOOFED IN INPUTTING u1 AND u2")
		return None


	### Compute intersection
	determinant = det2x2(q2[0] - q1[0], p1[0] - p2[0], q2[1] - q1[1], p1[1] - p2[1])

	if determinant == 0:
		print("Determinant is 0")
		return None


	t0 = (((q1[1] - q2[1]) * (p1[0] - q1[0])) + ((q2[0] - q1[0]) * (p1[1] - q1[1]))) / determinant
	t1 = (((p1[1] - p2[1]) * (p1[0] - q1[0])) + ((p2[0] - p1[0]) * (p1[1] - q1[1]))) / determinant

	intersection = (p1[0] + t0 * (p2[0] - p1[0]), p1[1] + t0 * (p2[1] - p1[1]))
	#intersection1 = (q1[0] + t1 * (q2[0] - q1[0]), q1[1] + t1 * (q2[1] - q1[1]))
	#print("Bool:	" + str(intersection == intersection1))
	#print("t0:	" + str(t0))
	#print("t1:	" + str(t1))
	#rint("intersection:	" + str(intersection))
	#print("intersection1:	" + str(intersection1))


	### Interpret parametrization values based on input types
	#print("v1_v2_is_ray:	" + str(v1_v2_is_ray))
	#print("u1_u2_is_ray:	" + str(u1_u2_is_ray))

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

	#print("Final return")
	return None

def slope(v1, v2):
	if (type(v1) == Lambda) and (type(v2) == Lambda):
		print("DOUBLE LAMBDAS. DO SOMETHING ABOUT IT")
	elif (type(v1) == Lambda):
		return v1.direction
	elif (type(v2) == Lambda):
		return v2.direction
	else:
		den = (v2[0] - v1[0])
		return (v2[1] - v1[1]) / den

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

#print(findIntersect(v2, w1, u1, u2))

'''

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon



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


#Class testing
'''
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

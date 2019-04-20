import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from Global_Functions import *


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
		self.flex_dictionary = setFlex(list_of_vertices)
		self.F_list = list()
		self.L_list = list()


	def setFlex(self, list_of_vertices):
		'''
		Note: This will only work if the list is organized such that the first point is not repeated and 
		the list is circular!
		'''

		oriented = orientVert(list_of_vertices)

		flexes = dict()

		i = 0
		j = 0
		k = 0
		
		while len(flexes) < len(list_of_vertices):
			if CCW(oriented[i], oriented[j], oriented[k]) == -1:
				#mark point j as reflex
				flexes[oriented[j]] = 0
			else:
				#mark point j as nonreflex
				flexes[oriented[j]] = 1
			i += 1
			j += 1
			k += 1

		return flexes

	def orientVert(self, list_of_vertices):
		oriented = []
		'''
		pick leftmost point or lowest point
		'''
		v0_index = list_of_vertices.index(sorted(list_of_vertices, key=lambda k: [k[1], k[0]])[0])
		oriented.append(list_of_vertices[v0_index])

		'''
		compare slopes
		'''
		dir1 = slope(list_of_vertices[v0_index], list_of_vertices[v0_index + 1])
		dir2 = slope(list_of_vertices[v0_index - 1], list_of_vertices[v0_index])

		if dir1 < dir2:

			vi_index = v0_index + 1
			
			while vi_index != v0_index:
				oriented.append(list_of_vertices[vi_index])
				vi_index += 1

		elif dir2 < dir1:

			vi_index = v0_index - 1
			
			while vi_index != v0_index:
				oriented.append(list_of_vertices[vi_index])
				vi_index -= 1

		return oriented


# Class testing
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

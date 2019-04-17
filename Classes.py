from shapely.geometry.polygon import Polygon


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




class Lambda(__BasicNode):
	def __init__(self, direction = None):
		super().__init__()
		self.direction = direction

	def setDirection(self, direction):
		self.direction = direction
		return

	def getDirection(self):
		return self.direction



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
		self.flex_dictionary = dict()


# Class testing
"""
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
"""








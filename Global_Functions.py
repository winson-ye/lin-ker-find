from Classes import *
import math


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
		if v1.direction[0] == 0:
			print("slope:	Divide by 0")
			return None
		else:
			return v1.direction[1] / v1.direction[0]

	elif (type(v2) == Lambda):
		if v2.direction[0] == 0:
			print("slope:	Divide by 0")
			return None
		else:
			return v2.direction[1] / v2.direction[0]

	else:
		den = (v2[0] - v1[0])
		return (v2[1] - v1[1]) / den

	return None












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

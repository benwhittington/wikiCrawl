import os
import numpy as np
from glob import glob

class Node(object):
	
	# a node object has:
	#	a name
	#	a value
	#	arcs in (names?)
	#	arcs out (names?)

	def __init__(self):
		self.name = None
		self.value = None
		self.arcs_in = []
		self.arcs_out = []
	def __repr__(self):
		# returns the name of the node 
		return 'nd:{}'.format(self.name)
class Arc(object):
	
	# an arc object has:
	#	a name
	#	a node it came from
	#	a node it goes to

	def __init__(self):
		self.weight = None
		self.to_node = None
		self.from_node = None
	def __repr__(self):
		return '{} -> {}'.format(self.to_node.name,self.from_node.name)
class NetworkError(Exception):
	'''An error to raise when violations occur.
	'''
	pass
class Network(object):
	# network class contains 2 lists
	#	one of all the nodes in the network
	#	one of all the arcs in the network

	def __init__(self):
		self.nodes = []
		self.arcs = []
	def __repr__(self):
		return 'ntwk'
	def get_node(self, name):
		''' Loops through the list of nodes and returns the one with NAME.
		
		    Returns NetworkError if node does not exist.
		'''
		# loop through list of nodes until node found
		for node in self.nodes:
			if node.name == name:
				return node
		
		raise NetworkError
	def display(self):
		''' Print information about the network.
		'''
		# print nodes
		print('network has {:d} nodes: '.format(len(self.nodes))+(len(self.nodes)*'{}, ').format(*(nd.name for nd in self.nodes)))
		# print arcs
		for arc in self.arcs:
			print ('{} --> {} with weight {}'.format(arc.from_node.name, arc.to_node.name, arc.weight))


	def add_node(self, name, value=None):
		'''Adds a Node with NAME and VALUE to the network.
		'''
		node = Node()
		node.name = name
		node.value = value				
		# 3. THINK VERY CAREFULLY ABOUT WHAT THE NEXT COMMAND IS DOING
		# append node to the list of nodes
		self.nodes.append(node)


	def join_nodes(self, node_from, node_to, weight):
		'''Joins to Nodes: node_from and node_to
		'''
		# make new unassigned arc
		arc = Arc()
		# assign attributes
		arc.weight = weight
		arc.from_node = node_from
		arc.to_node = node_to
		
		node_from.arcs_out.append(arc)
		node_to.arcs_in.append(arc)

		# append arc to list of arcs in Network object
		self.arcs.append(arc)


#!/usr/bin/env python
#tree.py
###USAGE### tree.py ; sms=N ; $#=0


class Tree(object):

	def __init__(self, name, data = None, children = None):
		self.name = name
		self.data = data
		self.children = []
		self.parent = None
		if children is not None:
			for child in children:
				self.addChild(child)

	def addChild(self, child):
		assert isinstance(child, Tree)
		assert child.isRoot()
		child._setParent(self)
		self.children.append(child)

	def __str__(self):
		return str(self.name)

	def __len__(self):
		return len(self.children)

	# only prints descendants, not ancestors
	def prettyStr(self, indent = '\t', level = 0):
		prefix = str(indent) * int(level)
		output = ''
		output += prefix + "Name: " + str(self.name) + '\n'
		output += prefix + "Data: " + str(self.data) + '\n'
		if len(self) > 0:
			for i, child in enumerate(self.children):
				output += prefix + str(i) + ":\n"
				output += child.prettyStr(indent, level + 1)
		return output

	def getName(self):
		return self.name

	def removeChild(self, i):
		del self.children[i]

	def popChild(self, i):
		child = self.children[i]
		self.removeChild(i)
		child._removeParent()
		return child

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data

	def _removeParent(self):
		self.parent = None

	def _setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent

	def getChild(self, i):
		return self.children[i]

	def isRoot(self):
		return (self.parent is None)

	def hasAncestorWithName(self, ancestorName):
		if self.isRoot():
			return False
		else:
			if self.parent.getName() == ancestorName:
				return True
			else:
				return self.parent.hasAncestorWithName(ancestorName)



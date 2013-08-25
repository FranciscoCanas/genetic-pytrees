from random import random,randint,choice
from copy import deepcopy
from math import log

class tree:
	"""
	This is a wrapper class for the tree-like source structure that will also
	keep track of some of the meta-parameters for later use.
	"""
	def __init__(self,num_params,func_list=[],max_depth=5,pr_func=0.5,
	             pr_param=0.5,const_func=lambda:randint(0,100)):
		self.num_params = num_params
		self.func_list = func_list
		self.max_depth = max_depth
		self.pr_func = pr_func
		self.pr_param=pr_param
		self.const_func = const_func
		self.root = random_tree(num_params, func_list, max_depth, 
		                        pr_func, pr_param,const_func)	
		
	def mutate(self, prob_change=0.1):
		"""
		Randomly mutate the source tree rooted at self.root by recursively
		mutating it and all of its descendants.
		"""
		self.root = self._mutate(self.root,prob_change,self.max_depth)
		
	def _mutate(self, subtree, prob_change,max_depth):
		"""
		Private helper for mutate.
		"""
		# Return a brand new random tree if we achieve mutation:
		if random()<prob_change:
			return random_tree(self.num_params, self.func_list, 
			                   max_depth, self.pr_func, 
			                   self.pr_param, self.const_func)
		else: 
			result = deepcopy(subtree)
			# Otherwise, if we're at a function onde, recursively
			# mutate its children.
			if isinstance(subtree,fnode):
				result.children=[self._mutate(child,prob_change,
				                              max_depth-1) 
				                 for child in subtree.children]
			return result
		
	def crossbreed(self, other, prob_swap=0.25,atroot=True):
		"""
		Creates a new tree by replacing subtrees randomly with subtrees
		from another tree.
		"""
		return self._crossbreed(self.root, other, prob_swap, atroot)
		
	def _crossbreed(self, this, other, prob_swap=0.25,atroot=True):
		"""
		Private helper for crossbreed.
		"""
		# Return a copy of the other subtree if we're not at root
		# and we achieve swappiness.
		if random()<prob_swap and not atroot:
			return deepcopy(other)
		else:
			result = deepcopy(this)
			# Recurse into all of the children of 
			# this subtree and crosbreed if both current subtrees
			# are function nodes.
			if isinstance(this, fnode) and isinstance(other, fnode):
				result.children = [self._crossbreed(child, 
				                             choice(other.children),
				                             prob_swap,
				                             False) 
				                   for child in this.children]
			return result
		
	
	def evaluate(self, paramlist):
		return self.root.evaluate(paramlist)
	
	def print_to_string(self,paramlist):
		self.root.print_to_string(paramlist)

class func:
	"""
	This is a wrapper for functions.
	"""
	def __init__(self, function, numparam, name):
		self.function = function# A function object (lambda or otherwise)
		self.numparam = numparam# Number of parameters (or children)
		self.name = name	# A string for the function name.
		

class fnode:
	"""
	The function node: A node initialized with a func. It evaluates the func
	with its children (if any) as parameters and returns the result.
	"""
	def __init__(self, func, children):
		self.function = func.function	# A function object wrapped in func.
		self.name= func.name		# The name of the function above.
		# A list containing the children to this node (ie: the paramlist for the func).
		self.children = children	
		
	def evaluate(self,inp):
		# map list of children to list of childrens' return values.
		result=[n.evaluate(inp) for n in self.children] 
		# evaluate using the childrens' return values.
		return self.function(result)	
	
	def print_to_string(self,paramlist,indent=0):
		"""
		Generates a printable representation of this source 'tree'.
		"""
		print (' '*indent)+self.name
		for child in self.children:
			child.print_to_string(paramlist,indent+4)
		
		
class pnode:
	"""
	The parameter node: A node that returns one of the paramlist passed 
	into the program.
	"""
	def __init__(self, paramid):
		self.paramid = paramid
		
	def evaluate(self, paramlist):
		return paramlist[self.paramid]
	
	def print_to_string(self,paramlist,indent=0):
		print ' '*indent + str(self.paramid) + "=" + str(self.evaluate(paramlist))
		
class cnode:
	"""
	The constants node: A node that holds and return constant values 
	in the program.
	"""
	def __init__(self, value):
		self.value = value
	
	def evaluate(self, paramlist):
		return self.value
	
	def print_to_string(self,paramlist,indent=0):
		print ' '*indent + str(self.value)

		
def random_tree(num_params, func_list, max_depth=5, pr_func=0.5, pr_param=0.5,
                const_func=lambda:randint(0,100)):
	"""
	Makes and returns a random source code tree.
	num_params: the number of parameters this tree takes on evaluate.
	func_list: A list of functions to form this tree's vocabulary.
	max_depth: An upper bound on tree depth.
	pr_func: The probability of a child being a function.
	pr_param: The probability of a child being a parameter.
	const_func: A method that returns a random constant.
	"""
	
	# If we are not at maxdepth and we draw random func:
	if random() < pr_func and max_depth > 0:
		# Randomly pick a function
		f=choice(func_list)
		# Create a list of subtrees based on function's required paramlist:
		children = [random_tree(num_params,func_list,max_depth-1,
		                        pr_func,pr_param,const_func)
		            for i in range(f.numparam)]
		# Wrap it up in a node and return
		return fnode(f,children)
	# if we draw random param:
	elif random()<pr_param:
		# Return a parameter node randomly choosing one of the program paramlist.
		print num_params
		return pnode(randint(0,max(num_params-1,0)))
	else:
		# Return a constant node with some random num.
		return cnode(const_func())
	

	
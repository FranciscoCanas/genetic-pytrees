from src.pytree import *
from src.pyforest import *

def if_base(p):
    if p[0]>0: return p[1]
    else: return p[2]
    
def is_greater_base(p):
    if p[0] > p[1]: return 1
    else: return 0
    
def test_tree1():
    """
    Looks like this:
    if (param[0]>0):
        return param[1] + 5
    else:
        return param[1] - 2
    """
    return fnode(func_if, [
        fnode(func_gt,[pnode(0),cnode(3)]),
        fnode(func_add,[pnode(1),cnode(5)]),
        fnode(func_sub,[pnode(1), cnode(2)])
        ])

# Func wrappers for common functions:
func_add=func(lambda p:p[0]+p[1],2,'add')
func_sub=func(lambda p:p[0]-p[1],2,'sub')
func_mul=func(lambda p:p[0]*p[1],2,'mul')
func_if=func(if_base,3,'if')
func_gt=func(is_greater_base,2,'gt')

# A list containing all funcs:
func_list = [func_add, func_sub, func_mul, func_if, func_gt]

def test_tree(tree, paramlist):
    print "Tree Structure: "
    tree.print_to_string(paramlist)
    result = tree.evaluate(paramlist)
    print "Result: " + str(result)
    return result

def pytree_tests():
    """
    Some tests for treerep.py
    """ 
    
    
    t1=test_tree1()
    r1 = test_tree(t1,[2,3])
    r2 = test_tree(t1,[5,3])
    assert (r1==1)
    assert (r2==8)
    
    # Some random trees and tests:
    r1 = random_tree(3,func_list,3,0.6,0.5,lambda:randint(0,5))
    r2 = random_tree(3,func_list,5,0.7,0.5,lambda:randint(0,50000))
    r3 = random_tree(3,func_list,10,0.5,0.3)
    
    test_tree(r1,[1,2,3])
    test_tree(r2,[1,2,3])
    test_tree(r3,[1,2,3])
    
    #tree wrapper tests
    print "Testing tree wrapper:"
    tw1 = tree(3,func_list,12,0.7,0.5,lambda:randint(0,5))
    test_tree(tw1,[1,2,3])
    print "Mutating tree:"
    tw1.mutate(0.1)
    test_tree(tw1,[1,2,3])
    print "Mutating tree again:"
    tw1.mutate(0.25)
    test_tree(tw1,[1,2,3])
    print "Generating tw2:"
    tw2 = tree(3,func_list,12,0.3,0.7,lambda:randint(0,50))
    test_tree(tw2,[1,2,3])
    print "Crossbreeding tw2 and tw3:"
    tw3 = tw1.crossbreed(tw2)
    test_tree(tw3,[1,2,3])
    
def pyforest_tests():
    """
    Some test and useage examples for pyforest.py
    """
    f1 = pyforest([x*2 for x in range(6)], # possible depths
                  func_list, # list of functions for the nodes
                  range(1,5), # possible number of params
                  [0.25,0.5,0.75], # possible func node probabilities
                  [0.7,0.5,0.4,0.3], # possible param node probabilities
                  [lambda: randint(-1,2),
                   lambda: choice([x**3 for x in range(25)]),
                   lambda: randint(-100,100)], # possible constant generation funcs
                  10, # num of trees in forest
                  lambda: choice([x**2 for x in range(6)])# parameter-gen func
                  )
    
    f1.print_to_string()
    print f1.evaluate_forest()
    


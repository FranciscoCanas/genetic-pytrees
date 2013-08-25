from src.pytree import *

def if_base(p):
    if p[0]>0: return p[1]
    else: return p[2]
    
def is_greater_base(p):
    if p[0] > p[1]: return 1
    else: return 0
    
def test_tree1():
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

def test_tree(tree, paramlist):
    print "Tree Structure: "
    tree.print_to_string()
    print "Result: " + str(tree.evaluate(paramlist))

def pytree_tests():
    """
    Some tests for treerep.py
    """ 
    # A list containing all funcs:
    func_list = [func_add, func_sub, func_mul, func_if, func_gt]
    
    t1=test_tree1()
    test_tree(t1,[2,3])
    test_tree(t1,[5,3])
    
    # Some random trees and tests:
    r1 = random_tree(3,func_list,3,0.6,0.5,lambda:randint(0,5))
    r2 = random_tree(3,func_list,5,0.7,0.5,lambda:randint(0,50000))
    r3 = random_tree(3,func_list,10,0.5,0.3)
    
    test_tree(r1,[1,2,3])
    test_tree(r2,[1,2,3])
    test_tree(r3,[1,2,3])
    
    # tree wrapper tests
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
    


import os
from problem import Problem, OptType
from bip_state import BinaryIntegerProgramming as BIP
from monte_carlo import mcts
from node import Node
from  bb import BranchAndBound
import pickle
import numpy as np

def call_bb(p):
    b_b = BranchAndBound(p)
    res = b_b.bbsolve()
    # print(f'solution value: {res[0]}, vars_solution: {res[1]}')
    # print(f'node searched: {res[3]}')
    # print(f'jumps: {res[2]}')

def problem_page_35():
    #page 35
    func_coeff = [-9,-5,-6,-4]
    var_bounds = [(0,1),(0,1),(0,1),(0,1)]
    const_coeff = [[6,3,5,2], [0,0,1,1],[-1,0,1,0],[0,-1,0,1]]
    const_bound = [10,1,0,0]
    p = Problem(OptType.MIN, func_coeff, const_coeff, const_bound, var_bounds, func_coeff)

    vars_val = [None] * len(p.func_coeff)
    root = Node(vars_val, p)
    bip = BIP(root,None)
    mc = mcts(iterationLimit=len(p.func_coeff)*2)
    best = mc.search(bip)
    print(best.total_reward)
    print()
    #call_bb(p)


def problem_mission_impossible():
    '''
            0
        10       15
    -1      -1   5      4

    '''
    node = Node([None,None],1,0)
    node10 = Node([None,None],2,10)
    node15=Node([None,None],3,15)
    nodenull1 = Node([None,None],4,66)
    nodenull2 = Node([None, None], 5, 67)
    node4 =Node([None,None],6,4)
    node5 = Node([None,None],7,5)
    node.add_children([node10,node15])
    node10.add_children([nodenull1,nodenull2])
    node15.add_children([node5,node4])
    bip = BIP(node,node)
    mc = mcts(iterationLimit=10)
    mc.search(bip)

if __name__ == '__main__':
    # problem_mission_impossible()
    # problem_page_35()
    with open("problems_pickle_v2",'rb') as f:
        problems_arr = pickle.load(f)
    for i,(p,v) in enumerate(problems_arr):

        # b_b = BranchAndBound(p)
        # res = b_b.bbsolve()
        print('_______________________________________________________\n\n\n\n')
        vars_val = [None] * len(p.func_coeff)
        root = Node(vars_val, p)
        bip = BIP(root,None)
        mc = mcts(iterationLimit=len(p.func_coeff)*200)
        res = mc.search(bip)
        print(res.total_reward)
        print(f'problem {i+1} solution is {v} mc solution is {res.total_reward}')
        break
    # p = problems_arr[-1]
    # sol = [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
    # for i, c in enumerate(p.constraint_coeff):
    #     if np.dot(c, sol) > p.constraint_bound[i]:
    #         print("infeasible")
    # print(f'solution value: {res[0]}, vars_solution: {res[1]}')
    # print(f'node searched: {res[3]}')
    # print(f'jumps: {res[2]}')

from scipy.optimize import linprog as scilp
import enum
from node import Node
import copy
import numpy as np

class LPResult(enum.Enum):
    VAR_COEFF = 0,
    FUNC_VAL = 1,
    SLACKS_VAL = 2,
    CON = 3, #The (nominally zero) residuals of the equality constraints, b_eq - A_eq @ x
    SUCESS = 4,
    STATUS = 5,
    NUM_ITER = 6,
    MSG = 7


class Tree(object):
    def __init__(self,problem):
        vars_val = [None] * len(problem.func_coeff)
        self.best_possible_val = self.lp_node_value(problem)['fun']
        self.root = Node(vars_val, problem, self.best_possible_val)

    def lp_node_value(self, problem):
        result = scilp(problem.func_coeff,A_ub = problem.constraint_coeff,b_ub = problem.constraint_bound, bounds = problem.var_bounds)
        return result

    def get_lp_addition(self, var_vals, level, problem):
        addition = np.dot(var_vals[:level], problem.original_func_coeff[:level])
        result = copy.deepcopy(self.lp_node_value(problem))
        if result["success"]:
            val = result["fun"] + addition
        return result,val

    def get_children(self,node):
        if node.is_final:
            return None
        prob1 = copy.deepcopy(node.get_problem())
        prob2 = copy.deepcopy(node.get_problem())
        vars_val_l = node.var_val.copy()
        vars_val_r = node.var_val.copy()
        vars_val_l[node.level] = 1
        left_n = Node(vars_val_l, prob1)
        vars_val_r[node.level] = 0
        right_n = Node(vars_val_r, prob2)
        return left_n, right_n


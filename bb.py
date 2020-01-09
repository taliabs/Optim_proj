from heapq import *
from tree import Tree
from node import Node
import numpy as np


class MaxHeap(object):

    def __init__(self):
        self.priority_queue = []

    def add(self,data):
        #for i in data:
        item = (-data.val, data)
        heappush(self.priority_queue, item)

    def get_item(self):
        if len(self.priority_queue) == 0:
            return None
        return heappop(self.priority_queue)[1]

    def is_empty(self):
        if len(self.priority_queue) == 0:
            return Tree
        return False


class BranchAndBound(Tree):
    def __init__(self):
        self.priority_queue = MaxHeap()
        self.jump_indicator = {}
        self.node_searched = []

    def bbsolve(self):
        self.priority_queue.add(self.root)
        jump = 0
        while not self.priority_queue.is_empty():
            temp_best_node = self.priority_queue.get_item()
            self.node_searched.append(temp_best_node.var_val)
            jump = abs(temp_best_node.level- jump) #todo - change to xsor between vars_val
            self.jump_indicator[jump] = self.jump_indicator.get(jump, 0) + 1
            jump = temp_best_node.level

            if not temp_best_node.not_valid:
                if temp_best_node.is_final:  # if a valid solution then this is the best
                    return temp_best_node.val, temp_best_node.var_val, self.jump_indicator, self.node_searched
                else:  # otherwise, we're unsure if this branch holds promise. Maybe it can't actually achieve this lower bound. So branch into it
                    new_nodes = self.get_children(temp_best_node)
                    for new_node in new_nodes:
                        if new_node.is_final:
                            self.priority_queue.add(new_node)
                        else:
                            val = self.lp_node_value(new_node) # todo - check res val
                            if val not in ["infeasible", "unbounded"]:
                                new_node.val = val
                                if val is int:
                                    new_node.is_final = True
                                    new_node.var_val = val.res
                                self.priority_queue.add(new_node)
                            # else:
                            #     new_node.val = np.Infinity
                            #     new_node.is_final = True
                            #     new_node.not_valid = True
                        #heappush(heap, (res, next(counter), new_node))  # using counter to avoid possible comparisons between nodes. It tie breaks
        # no solution for this problem
        return None, None, self.jump_indicator, self.node_searched

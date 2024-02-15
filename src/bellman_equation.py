"""
Creating general functions to solve dynamic programs
"""
from typing import List, NamedTuple
import numpy as np
cache = {} #store any calculations we do, so that we don't have to do them again
# we can use tuples as keys for dictionaries bc they can't be changed.  
WEIGHTS = np.arange(1,8)
VALUES = np.arange(7,0,-1)

class KnapsackState(NamedTuple):
    """Type of named tuple that contains two attributes,
    remaining weight and item_idx

    Args:
        NamedTuple (_type_): _description_
    """
    remaining_weight: int
    item_idx: int = 0

def actions(state: KnapsackState)->List:
    """returns a list of actions given our current state

    Args:
        state (_type_): _description_

    Returns:
        List: returns a list 0 and 1. 0 for leave. 1 for take
    """
    if state.item_idx == WEIGHTS.shape[0] - 1:
    # if it is the last item no more actions can be taken - terminal state detection
        return []
    if state.remaining_weight < WEIGHTS[state.item_idx]:
    # if we exceed our weight capacity we can only leave the item
        return [0]
    return [0, 1]

def transition(state: KnapsackState, action: int):
    """takes in our current state and our choice of action and returns a new state

    Args:
        state (_type_): _description_
        action (_type_): _description_
    """
    if action ==1: # we take the object
        return KnapsackState(state.remaining_weight - WEIGHTS[state.item_idx],
                             state.item_idx + 1)
    else: # do not take object
        return KnapsackState(state.remaining_weight, state.item_idx + 1)

def immediate_reward(state:KnapsackState, action)->float:
    """gives us our immediate payoff

    Args:
        state (_type_): _description_
        action (_type_): _description_

    Returns:
        float: _description_
    """
    if action:
        return VALUES[state.item_idx]
    return 0

def bellman_equation(state: KnapsackState)-> float:
    """solves dynamic programming

    Args:
        state (Tuple[int,int]): _description_

    Returns:
        float: _description_
    """
    # we set to 0 instead of - infinity because all values are guaranteed
    # positive by problem definition
    if state in cache:
        return cache[state]
    max_reward = 0 
    for a in actions(state):
        new_state = transition(state, a)
        future_reward = bellman_equation(new_state)
        reward = immediate_reward(state, a) + future_reward
        if reward > max_reward:
            max_reward = reward
    cache[state] = max_reward #max_reward is best possible value given current action
    #max_reward is the interesting number here. 
    return max_reward
#need to be able to generalize Bellman for other probs. adapt actions,
#transition, immediate reward


#use bellman 
#state - how many floors there are and how many eggs you have. (n: eggs, k: floors)
#we want the value fucntion on the 
#so not which floor you should drop it from next, but how many floors you need to test. 
#INTRO TO RECURRSION IS DUE 2/20 - NEXT CLASS 
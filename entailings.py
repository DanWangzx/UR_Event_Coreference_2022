import json
import jsontrips 

ontd = jsontrips.ontology()
import numpy as np


def conjoin(term1, type):  # whether term1 entailed by term2. e.g. if Sam is a DOG, Sam must be an animal.    
    curr_term = term1.type
    if term1.type == type:
        return True
    while curr_term != 'ROOT':
        parent = lf_parent(curr_term)
        #print(parent)
        if parent == type:
            return True
        curr_term = parent
    return False


def gender_check(token1, token2):
    type1 = token1.type
    type2 = token2.type
    result = True
    v1 = gender(type1)
    v2 = gender(type2)
    if not np.dot(v1, v2):
        result = False
    return result


def gender(string):
    g = 'defailt'
    if 'MALE' in string and not 'FEMALE' in string:
        g = [1, 0] # male
    elif 'FEMALE' in string:
        g = [0, 1] # female
    else:
        g = [1, 1] # unknown
    
    return g

def entailed_by(term1, term2):  # whether term1 entailed by term2. e.g. if Sam is a DOG, Sam must be an animal.    
    curr_term = term1.type
    if term1.type == term2.type:
        return True
    while curr_term != 'ROOT':
        parent = lf_parent(curr_term)
        if parent == term2.type:
            return True
        curr_term = parent
    return False


def lf_parent(term1):
    parent = ontd[term1]['parent']
    return parent


def lf_child(term1):
    children = ontd[term1]['children']
    return children


def wu_palmer_sim(sense1, sense2):

    temp, depth1, depth2 = lcs_finder(sense1, sense2)
    root_track, hist = track_root(temp)
    sense1_track, hist = track_root(sense1)
    sense2_track, hist = track_root(sense2)
    score = 2*root_track/(sense1_track+ sense2_track)

    return score # the score of two sense: float


def lcs_finder(sense1, sense2):
    depth_01 = 0
    depth_02 = 0
    x, hist = track_root(sense1) # len(hist) is the steps to take back for sense1 
    #print(f'the ontology of word1 is {hist}')
    temp = sense2

    if sense1 == sense2:
        return temp, depth_01, depth_02

    while True:
        if ontd[temp]['parent'] not in hist:
            #print(f'current temp is {temp}')
            temp = ontd[temp]['parent']
            depth_02 += 1
        else:
            temp = ontd[temp]['parent']
            break

    for i in range(len(hist)):
        if hist[i] == temp:
            depth_01 = i + 1
    #print(f'lease common sub is {temp}')
    
    return temp, depth_01, depth_02 # the depth of a lcs: int


def look_parent(sense1):
    parent = ontd[sense1]['parent']
    return parent


def track_root(sense1) -> tuple:
    depth = 0
    hist = []
    temp = sense1
    while True:
        #print(f'temp in is {temp}')
        if ontd[temp]['parent'] == 'ROOT':
            depth += 1
            hist.append('ROOT')
            return depth, hist
        else:
            #print(f'current depth is {depth}')
            depth += 1
            temp = ontd[temp]['parent']
            hist.append(temp)
            #print(f' out {temp} ')




#test_score1 = wu_palmer_sim('ANIMAL', 'ANIMAL')


stop = 1
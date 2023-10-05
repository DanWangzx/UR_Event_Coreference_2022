from cmath import inf
import entailings as et
import numpy as np

def score_fin(full_potential_dict, SVOs):
    noun_scores = evidence_noun_wu_palmer(full_potential_dict)
    verb_scores = evidence_verb_wu_palmer(full_potential_dict, SVOs)
    mappings = {}
    for key in noun_scores:
        mappings[key] = []
        value_noun = noun_scores[key] # [(token, score)]
        value_verb = verb_scores[key] # [(flagger, comp, base, sub, token1), (flagger, comp, sub, token2)]
        if len(value_noun) != 0:
            max_score = 0
            best_token = None
            for index in range(len(value_noun)):
                token = value_noun[index][0]
                plural_score = evidence_plularity(token, key)
                n_score = value_noun[index][1]
                v_score = 0
                if len(value_verb) != 0:
                    v_score = value_verb[index][2]
                fin_score = (n_score + v_score)*plural_score
                mappings[key].append(((n_score, v_score), token))#
                '''
                if fin_score > max_score:
                    max_score = fin_score
                    best_token = token
            if best_token:
                mappings[key].append((max_score, best_token))
            '''
        
    return mappings 


def evidence_noun_wu_palmer(full_potential_dict): # too early to get max from here
    new_mappings = {}
    for key in full_potential_dict:
        if key.spec != 'VERB':
            potential_list = full_potential_dict[key]
            #score_fin = -inf
            pair_fin = []
            for i in potential_list:
                if i.spec != 'VERB':
                    score = et.wu_palmer_sim(key.type, i.type)
                    '''
                    if score > score_fin:
                        score_fin = score
                        pair_fin = [i, score]
                    '''
                    pair_fin.append((i, score))
            new_mappings[key] = pair_fin
    return new_mappings
        

def evidence_verb_wu_palmer(full_potential_dict, SVOs, subject_param = 1.5, obejct_param = 1):
    mappings = {}
    for i in SVOs:
        for j in i:
            flagger, token1, token2 = j
            if flagger == 0: # if the tuple is a S-V
                mappings[token1] = (flagger, et.wu_palmer_sim(token1.type, token2.type), token2) 
            if flagger == 1: # if the tupe is a V-O
                mappings[token2] = (flagger, et.wu_palmer_sim(token1.type, token2.type), token1)
    
    # -- CHECK --

    out_mappings = {}
    for key in full_potential_dict:
        value = full_potential_dict[key]
        out_mappings[key] = []
        if key.spec != 'VERB' and key in mappings:
            flagger, base_score, verb_token = mappings[key]
            for i in value:
                if i.spec != 'VERB':
                    subs_score = et.wu_palmer_sim(verb_token.type, i.type)
                    comparative = subs_score - base_score
                    out_mappings[key].append((flagger, comparative, subs_score, i))


    return out_mappings


def evidence_plularity(token1, token2):
    s1 = token1.spec
    s2 = token2.spec

    if s1 == 'PRO-SET' or s1 == 'INDEF-SET' or s1 == 'THE-SET' or s1 == 'SOME':
        a = [0, 1]
    else:
        a = [1, 0]
    if s2 == 'PRO-SET' or s2 == 'INDEF-SET' or s2 == 'THE-SET' or s2 == 'SOME':
        b = [0, 1]
    else:
        b = [1, 0]
    if np.dot(a, b):
        return 1
    else:
        return 0



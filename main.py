from CSP_solver import CSP
import entailings as et
import numpy as np
import domain_modification as dm
import CSP_solver as cp

#path = '.\sample-input-output\input\input6'
spec_list = ['THE', 'THE-SET', 'PRO', 'PRO-SET', 'A', 'SOME', 'INDEF-SET', 'NAME', 'VERB'] # anything not a verb should be thrown into the wu_palmer



class TOKENS():
    def __init__(self, head_string, text, input_order, inherit=None): # each token represents features of a constituent with unique id, as provided.
        self.head = head_string
        self.order = input_order
        features = text.replace('(', '').replace(')', '')
        quoted = features.split('"')[1::2]
        self.string = quoted[0]
        features = features.replace(quoted[0], '').replace('"', '').split(' ')
        self.spec = features[0]
        self.type = features[2][5:]
        self.id = features[3]
        self.inherit = inherit # this is for intra-sentence referring only
    def __repr__(self) -> str:
        return self.id

class SOLUTIONS():
    def __init__(self, domain, curr_dict, parse_bags):
        self.domain = domain
        self.assign = curr_dict
        self.bags = parse_bags
        self.dc = None
    def __repr__(self) -> str:
        return len(self.domain)

    def add_dc(self, discourse_center_map):
        self.dc = discourse_center_map

def parse(filename):
    with open(filename, 'r') as f:
        data = f.read()
        inputs = data.split('\n\n')  
    
    token_bags = []
    for i in range(len(inputs)):
        tokens = []
        text = inputs[i].split('\n')
        head_string = text[0]
        for j in range(1, len(text)):
            m = text[j].split('(')
            if len(m) >= 2:
                tok_head = TOKENS(head_string, m[1], i, inherit='HEAD')
                tokens.append(tok_head)
                for l in range(2, len(m)):
                        tok = TOKENS(head_string, m[l], i, inherit=tok_head)
                        tokens.append(tok)
        token_bags.append(tokens)
    return token_bags


def pre_cluster(bags_of_tokens, neighbor=1):
    # step 1, initialize a dictionary, which includes all tokens

    # dict[token] = [list of tokens]
   
    neighbor_bag_pair = []
    for i in range(len(bags_of_tokens)):
        #print(i)
        '''
        if i+neighbor <= len(bags_of_tokens):
            neighbors_for = bags_of_tokens[i+1:i+neighbor+1]
            nf = [item for sublist in neighbors_for for item in sublist]
        else:
            neighbors_for = bags_of_tokens[i:]
            nf = [item for sublist in neighbors_for for item in sublist]
        '''
        if neighbor:
            if i - neighbor >= 0:
                neighbors_back = bags_of_tokens[i-neighbor:i]
                #print(neighbors_back)
                nb = [item for sublist in neighbors_back for item in sublist]
            else:
                neighbors_back = bags_of_tokens[:i]
                #print(neighbors_back)
                nb = [item for sublist in neighbors_back for item in sublist]
        else:
            neighbors_back = bags_of_tokens[:i]
            nb = [item for sublist in neighbors_back for item in sublist]
        neighbors = []
        #neighbors.extend(nf) maybe only the backward should work since we are only doing update after each input
        neighbors.extend(nb)
        neighbor_bag_pair.append((bags_of_tokens[i], neighbors))
    
    domain = []
    neighbor_dict = {}
    for i in range(0, len(neighbor_bag_pair)): #TODO: intra-corefs 
        fix, compare = neighbor_bag_pair[i]
        for j in fix:
            neighbor_dict[j] = []
        
            if j.spec != 'VERB':
                domain.append(j)
        
            if j.spec == 'NAME':
                for l in compare:
                    if l.spec == 'NAME' and j.string == l.string:
                        #domain.remove(j)
                        neighbor_dict[j] = [l]
                    
            elif j.spec == 'THE' or j.spec == 'THE-SET':
                for l in compare:
                    if l.string == j.string:
                        if l.spec == 'A' or l.spec == 'SOME':
                                neighbor_dict[j].append(l)
                        else:
                            if l.spec != 'PRO' and l.spec != 'PRO-SET':
                                neighbor_dict[j].append(l)
                if neighbor_dict[j]:
                    neighbor_dict[j].reverse()
                    neighbor_dict[j] = [neighbor_dict[j][0]]
            else:
                for l in compare:
                    neighbor_dict[j].append(l)


    solution = SOLUTIONS(domain, neighbor_dict, bags_of_tokens) # a primal solution with Name_referent solved and filtered out already.
    solution = dm.event_coref(dm.plural_coref(dm.indef_def_coref(dm.pronoun_person_coref(solution))))
    discourse_center = dm.discourse_center(solution)
    solution.dc = discourse_center

    #print(f'solution assign is {solution.assign}')
    #print(f'solution domain is {solution.domain}')
    '''
    pro_list = []
    for i in solution.domain:
        if i.spec == 'PRO' or i.spec == 'PRO-SET':
            pro_list.append(i)
    
    remodified = True
    for i in solution.domain:
        if i.spec != 'PRO' and i.spec != 'PRO-SET':
            if len(solution.assign[i]) > 1:
                remodified = False
                break
    
    if remodified:
        #print(f'remodying the domain to pronouns only')
        solution.domain = pro_list    

    #print(f'pronouns are {pro_list}')
    '''
    
    return solution

'''
    output = {}
    for i in neighbor_bag_pair:
        fix, compare = i
        for j in fix:
            if j in identified: # keep the Name_string identified pair intact
                output[j] = neighbor_dict[j]
            else:
                output[j] = []
                for l in compare:
                    #if l not in identified:
                    if ep(l, j):
                        output[j].append(l)
    
    # output: a dict with domains (filtered plural and name.check) TODO:make it a class?


    pair_score_bags = []
    for i in neighbor_bag_pair:
        sub_pairs = []
        explored = []
        for j in i[0]:
            for l in i[1]:
                if (j, l) and (l, j) not in explored:
                    explored.append((j, l))
                    sub_pairs.append((j, l))
        pair_score_bags.append(sub_pairs)
'''

#parse_bag = parse(path)
#test = evidence_plularity(parse_bag[0][0], parse_bag[0][1])

#parse_bag = parse(path)

# x = []
#solucion = pre_cluster(parse_bag, neighbor=0)

#assignment, solution_bags = cp.CSP(solucion)

#print(f'the final assignment is: {assignment}')



def file_convert(assignment, solution_bags, file_name):
    output = []
    for bag in solution_bags:
        temp = ''
        for i in bag:
            if i in assignment.keys():
                temp += '('+'COREF' + ' ' + str(i)+' '+str(assignment[i][0])+')'
                temp += ' '
        if len(temp) == 0:
            temp += '()'
        output.append(temp)
    
    with open(file_name, mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(output))
    

#domain_check(solucion)

#SVO_list = get_SVO(parse_bag)


# dict_test is a dict of all possible substitutions
#noun_score_dict = en(dict_test)

#verb_score_dict = ev(dict_test, SVO_list)

#score_fin = sf(dict_test, SVO_list)


def main():
    import sys
    filename_input = sys.argv[1]
    data = parse(filename_input)
    output_choice = sys.argv[2]

    parse_bag = parse(filename_input)
    solucion = pre_cluster(parse_bag, neighbor=0)
    assignment, solution_bags = cp.CSP(solucion)
    file_convert(assignment, solution_bags, output_choice)


if __name__ == '__main__':
    main()




stop = 1
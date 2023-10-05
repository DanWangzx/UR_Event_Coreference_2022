
'''
def name_coref 

def plural_coref
'''
from re import L
import entailings
import evidence

person_strings = {'MALE': ['he', 'him',  'He', 'Him'], 'FEMALE': ['she', 'her', 'She', 'Her']}
non_perosn_string = ['it', 'It']
first_person_strings = ['We', 'we', 'us']
reflexive = {'themselves': ['they', 'They'], 'himself': ['He', 'he'], 'herself':['She', 'she'], 'itself': ['it', 'It']}

class SOLUTIONS():
    def __init__(self, domain, curr_dict, parse_bags):
        self.domain = domain
        self.assign = curr_dict
        self.bags = parse_bags

    def __repr__(self) -> str:
        return len(self.domain)

def indef_def_coref(solution):
    domain = solution.domain
    assign_new = solution.assign.copy()
    bags = solution.bags
    domain_new = domain.copy()
    for i in domain:
        if i.spec == 'A' or i.spec == 'VERB' or i.order==0 or i.spec == 'SOME' or not assign_new[i] or i.string in first_person_strings:
            assign_new[i] = []
            domain_new.remove(i) # i been removed from domain because we know it shouldnt't refer to anything (verb should only be referred)
    solution_new = SOLUTIONS(domain_new, assign_new, bags)
    return solution_new


def pronoun_person_coref(solution):
    domain = solution.domain
    assign_new = solution.assign.copy()
    bags = solution.bags
    ppro_list = [item for sublist in person_strings.values() for item in sublist]
    domain_new = domain.copy()
    for i in domain:
        #print(i)
        if i.string in ppro_list:
            assign_i_new = assign_new[i].copy()
            for j in assign_new[i]:
                if entailings.gender_check(i, j):
                    if not entailings.conjoin(j, 'ANIMAL'):
                        assign_i_new.remove(j)
                else:
                    assign_i_new.remove(j)
            assign_new[i] = assign_i_new
        elif i.string in non_perosn_string:
            assign_i_new = assign_new[i].copy()
            for j in assign_new[i]:
                #print(j)
                if entailings.conjoin(j, 'PERSON'):
                    assign_i_new.remove(j)
                elif not entailings.conjoin(j, i.type) and not entailings.conjoin(i, j.type):
                    assign_i_new.remove(j)
            assign_new[i] = assign_i_new
        elif 'sel' in i.string and (i.spec == 'PRO' or i.spec =='PRO-SET'):
            target_strings = reflexive[i.string]
            for bag in bags:
                if i in bag:
                    for token in bag:
                        if token.string in target_strings:
                            assign_new[i] = [token]
                        break
            #domain_new.remove(i)
    solution_new = SOLUTIONS(domain_new, assign_new, bags)
    return solution_new


def plural_coref(solution):
    domain = solution.domain
    assign_new = solution.assign.copy()
    bags = solution.bags
    for i in domain:
        assign_i_new = assign_new[i].copy()
        for j in assign_new[i]:
            if not evidence.evidence_plularity(i, j):
                assign_i_new.remove(j)
        assign_new[i] = assign_i_new
    solution_new = SOLUTIONS(domain, assign_new, bags)
    return solution_new


def event_coref(solution):
    domain = solution.domain
    assign_new = solution.assign.copy()
    bags = solution.bags
    for i in domain:
        assign_i_new = assign_new[i].copy()
        for j in assign_new[i]:
            if j.spec == 'VERB':
                if i.spec == 'PRO' and (i.string == 'it' or i.string =='It'):
                    continue
                else:
                    assign_i_new.remove(j)
        assign_new[i] = assign_i_new
    assign = {}
    for i in domain:
        assign[i] = assign_new[i]
    solution_new = SOLUTIONS(domain, assign, bags)
    return solution_new


def SVO(sub_bag):
    subject = []
    object = []
    adjunct = []
    for j in range(len(sub_bag)):
        if sub_bag[j].spec == 'VERB':
            subject = sub_bag[:j]
                #SVO.append((i[j-1], i[j]))
            if j+1 < len(sub_bag):
                immediate_next = sub_bag[j+1]
                object.append(immediate_next)
                if immediate_next.inherit == 'HEAD':
                    for i in sub_bag[j+2:]:
                        if i.inherit == immediate_next:
                            object.append(i)
                        else:
                            adjunct.append(i)
                else:
                    adjunct = sub_bag[j+2:]
                break
            else:
                break
                #SVO.append((i[j], i[j+1]))
    
    #TODO returning: ([subject_pro], [object_pro], [adjunct_pro])
    return subject, object, adjunct


def pronoun_extract(SVO_bags, assign, local):
    output=[[],[],[]]
    if local:  # returning the pronouns of current sentence
        for i in range(len(SVO_bags)):
            new_i = SVO_bags[i].copy()
            for j in SVO_bags[i]:
                if j.spec != 'PRO' and j.spec != 'PRO-SET':
                    new_i.remove(j)
            output[i] = new_i
    else:
        return None
    '''
    else: # returning the entities of the context that couldve been referred to
        for j in 
        for i in parse_bag[index][1]:
            if assign[i] 
    '''

    return output


def discourse_center(solution):
    bags = solution.bags
    assign_new = solution.assign.copy()
    domain = solution.domain
    # initialize a tuple of cp and cb[]
    IDs = [i for i in range(len(bags))]
    sub_cat = {'cb': '', 'cp': ''}
    D = [sub_cat.copy() for i in range(len(bags))]

    #test = (pronoun_extract(SVO(bags[2]), solution.assign, local=True))
    for i in IDs:
        D[i]['cp'] = (pronoun_extract(SVO(bags[i]), solution.assign, local=True))
        
       # D[i]['cb'] = pronoun_extract(bags, i, solution.assign, local=False)
        D[i]['cb'] = SVO(bags[i])
    

    return D
    '''
    D_new = D.copy()
    for i in IDs:
        cp_bag = D_new[i]['cp']
        cp_list = [item for sublist in cp_bag for item in sublist]
        if len(cp_list) == 0:
            if D_new[i]['cb'][0]:
                D_new[i]['cb'] = D_new[i]['cb'][0][0]
            else:
                D_new[i]['cb'] = None
        else:
            cb_potential_last =  D[i-1]['cb']    
            D_new[i]['cb'] = cb_potential_last        
            
    initial = bags[0][0]


    for i in initial:
        if i.spec == 'PRO' or i.spec == 'PRO-SET':
            pass
        else:
            cb_init = None
    '''

from doctest import run_docstring_examples


def CSP(solution):
    return back_track({}, solution)

def back_track(assignment, solution):
    solved_domain = assignment.keys()
    if len(solution.domain) == len(solved_domain):
        output = solution.assign.copy()
        for i in assignment.keys():
            output[i] = [assignment[i]]
        return output, solution.bags
    next_var = select_a_var(solution, assignment)

    for pair in order_domain_value(next_var, assignment, solution):
        if check_consistent(pair,assignment, solution):
            assignment[next_var] = pair[1]
            result = back_track(assignment, solution)
            if result:
                return result
            else:
                assignment.pop(next_var)
    return False


def select_a_var(solution, assignment):
    index = len(assignment)
    if index < len(solution.domain):
        next_var = solution.domain[index]
    return next_var


def order_domain_value(next_var, assignment, solution):
    index = next_var.order
    pairs = []
    value_list = []
    mappings = solution.assign
    if len(mappings[next_var]) == 1:
        return [[next_var, mappings[next_var][0]]]

    for j in range(0, index):
        for i in range(len(solution.dc[index-j-1]['cb'])):
            value_list.extend(solution.dc[index-j-1]['cb'][i])
    #value_list.reverse()

    temp = []
    for i in value_list:
        if i in mappings[next_var]:
            temp.append(i)
    

    for value in temp:
        pairs.append([next_var, value])
    

    return pairs

def check_consistent(pair, assignment, solution, autopass=False):

    token1, token2 = pair
    mappings = solution.assign
    if len(mappings[token1]) == 1 and mappings[token1][0] == token2:
        return True
 
    if autopass:
        return True

    
    if not self_reflexive(pair, assignment, solution, autopass=False):
        return False
    
    return True
    


def self_reflexive(pair, assignment, solution, autopass=False):

    var, value = pair
    mappings = solution.assign
    bag = solution.bags


    temp_assignment = assignment.copy()
    for i in mappings.keys():
        if i not in temp_assignment:
            if len(mappings[i]) == 1:
                temp_assignment[i] = mappings[i][0]
    temp_assignment[var] = value

    #r_temp_assignment = {v: k for k, v in temp_assignment.items()}

    explored = []
    queue = [var]
    while queue:
        next = queue.pop(0)
        if next in temp_assignment.keys():
            token = temp_assignment[next]
            if token not in explored:
                explored.append(token)
                queue.append(token)
        
        if next in temp_assignment.values():
            for key, value in temp_assignment.items():
                if value == next:
                    if key not in explored:
                        explored.append(key)
                        queue.append(key)

    referent_list = explored
    #print(f'current pair is {pair}, assignment is {temp_assignment}, r is, referent list is {referent_list}')


    result = True 
    for i in bag:
        count = 0
        for j in i:
            if j in referent_list:
                if j.spec != 'PRO' and j.spec != 'PRO-SET':
                    count += 1
                else:
                    if 'sel' not in j.string:
                        count += 1

        if count >= 2:
            result = False
            break

    return result

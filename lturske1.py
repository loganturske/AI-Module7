from unification import parse, unification
from copy import deepcopy
start_state = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Store)"
]

goal = [
    "(item Drill)",
    "(place Home)",
    "(place Store)",
    "(agent Me)",
    "(at Me Home)",
    "(at Drill Me)"
]

actions = {
    "drive": {
        "action": "(drive ?agent ?from ?to)",
        "conditions": [
            "(agent ?agent)",
            "(place ?from)",
            "(place ?to)",
            "(at ?agent ?from)"
        ],
        "add": [
            "(at ?agent ?to)"
        ],
        "delete": [
            "(at ?agent ?from)"
        ]
    },
    "buy": {
        "action": "(buy ?purchaser ?seller ?item)",
        "conditions": [
            "(item ?item)",
            "(place ?seller)",
            "(agent ?purchaser)",
            "(at ?item ?seller)",
            "(at ?purchaser ?seller)"
        ],
        "add": [
            "(at ?item ?purchaser)"
        ],
        "delete": [
            "(at ?item ?seller)"
        ]
    }
}


def check_all_conds(start_state, conds, param_one, param_two, param_three):
    temp_conds = deepcopy(conds)
    for cond in temp_conds:
        for index, ele in enumerate(cond):
            if cond[index] == param_one[0]:
                cond[index] = param_one[1]
            if cond[index] == param_two[0]:
                cond[index] = param_two[1]
            if cond[index] == param_three[0]:
                cond[index] = param_three[1]
        if check_if_unify(start_state, cond) is False:
            return False
    return True


def check_if_unify(states, cond):
    for state in states:
        if unification(state, cond) is not False:
            return True
    return False


def apply_action(start_state, add, delete):
    state = deepcopy(start_state)
    for index, ele in enumerate(state):
        if ele == delete:
            state[index] = add
    return state

def apply_vars(action, actual, to_change):
    temp = deepcopy(to_change[0])
    for idx, ele in enumerate(temp):
        for index, needle in enumerate(action):
            if needle == ele:
                temp[idx] = actual[index]
    return temp


def forward_planner(start_state, goal, actions, plan=[], explored=[], debug=False):

    viable_actions = []
    if goal == start_state:
        return plan
    for key in list(actions.keys()):
        variables = {}
        for cond in actions[key]['conditions']:
            if len(cond) < 3:
                for state in start_state:
                    if unification(state, cond) is not False:
                        unified = unification(state, cond)
                        name = list(unified.keys())[0]
                        exists = variables.get(name)
                        if exists:
                            variables[name] = variables[name] + [unified[name]]
                        else:
                            variables[name] = []
                            variables[name] = variables[name] + [unified[name]]
        for param_one in variables[actions[key]['action'][1]]:
            para_one_name = actions[key]['action'][1]
            for param_two in variables[actions[key]['action'][2]]:
                para_two_name = actions[key]['action'][2]
                for param_three in variables[actions[key]['action'][3]]:
                    para_three_name = actions[key]['action'][3]
                    if check_all_conds(start_state, actions[key]['conditions'], (para_one_name, param_one), (para_two_name, param_two), (para_three_name, param_three)):
                        viable_actions.append([actions[key]['action'][0], param_one, param_two, param_three])

    for action in viable_actions:
        add = apply_vars(actions[action[0]]['action'], action, actions[action[0]]['add'])
        delete = apply_vars(actions[action[0]]['action'], action, actions[action[0]]['delete'])
        new_state = apply_action(start_state, add, delete)
        if new_state in explored:
            continue
        explored.append(new_state)
        plan.append(action)
        if forward_planner(new_state, goal, actions, plan, explored, debug) is not False:
            return plan
        plan.remove(action)
    return False


parsed_start_state = []
for ele in start_state:
    parsed_start_state.append(parse(ele))
parsed_goal = []
for ele in goal:
    parsed_goal.append(parse(ele))
parsed_actions = {}
for key in actions:
    parsed_actions[key] = {}
    parsed_actions[key]['action'] = parse(actions[key]['action'])
    parsed_actions[key]['conditions'] = [parse(x) for x in actions[key]['conditions']]
    parsed_actions[key]['add'] = [parse(x) for x in actions[key]['add']]
    parsed_actions[key]['delete'] = [parse(x) for x in actions[key]['delete']]
plan = forward_planner(parsed_start_state, parsed_goal, parsed_actions)
print(plan)

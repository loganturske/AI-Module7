from unification import parse, unification

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


def generate_states(start_state, actions, debug=False):



def forward_planner( start_state, goal, actions, debug=False):
    states = generate_states(start_state, actions, debug)
    return []


parsed_start_state = []
for ele in start_state:
    parsed_start_state.append(parse(ele))
parsed_goal = []
for ele in goal:
    parsed_goal.append(parse(ele))
parsed_actions = {}
for key in actions:
    parsed_actions[key] = {}
    parsed_actions[key]['actions'] = parse(actions[key]['action'])
    parsed_actions[key]['conditions'] = [parse(x) for x in actions[key]['conditions']]
    parsed_actions[key]['add'] = [parse(x) for x in actions[key]['add']]
    parsed_actions[key]['delete'] = [parse(x) for x in actions[key]['delete']]
plan = forward_planner( parsed_start_state, parsed_goal, parsed_actions)
#print(plan)

"""State machine states.

Given rules on which state transitions are legal,
facilitate state transitions.

example rules:
        kanban_states = {
            'todo': {
                'next': ['*'],
                'prev': ['*'],
            },
            'doing': {
                'next': ['*'],
                'prev': ['*'],
            },
            'done': {
                'next': ['*'],
                'prev': ['*'],
            },
        }
        temperature_states = {
            'too hot': {
                'next': ['just right'],
                'prev': ['just right'],
            },
            'too cold': {
                'next': ['just right'],
                'prev': ['just right'],
            },
            'just right': {
                'next': ['too hot', 'too cold'],
                'prev': ['too hot', 'too cold'],
            }
        }

"""


class TransitionException(Exception):
    """Exception for invalid transitions.
    """

    def __init__(self, src_state: str, next_state: str):
        self.src_state = src_state
        self.next_state = next_state

    def __str__(self):
        return f'Invalid transition from {self.src_state} to {self.next_state}'


def transition(state: str, next_state: str, rules: dict) -> str:
    """Transition to the next state based on the current state and the rules.
    """
    legal_states = rules[state].get('next', [])
    if '*' in legal_states or next_state in legal_states:
        return next_state
    else:
        raise TransitionException(state, next_state)


def get_next_states(state: str, rules: dict) -> list:
    """Return a list of all the next states.
    """
    states = rules[state].get('next', [])
    if '*' in states:
        return list(rules.keys())
    else:
        return states

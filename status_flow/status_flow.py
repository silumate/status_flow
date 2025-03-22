"""status machine.

Given rules on which status transitions are legal,
facilitate status transitions.

example rules:
        kanban_status = {
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
        temperature_status = {
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

    def __init__(self, curr_status: str, next_status: str):
        self.curr_status = curr_status
        self.next_status = next_status

    def __str__(self):
        return f'Invalid transition from {self.curr_status} to {self.next_status}'


def transition(status: str, next_status: str, rules: dict) -> str:
    """Transition to the next status based on the current status and the rules.
    """
    legal_statuses = rules[status].get('next', [])
    if '*' in legal_statuses or next_status in legal_statuses:
        callbacks = rules[next_status].get('callback', [])
        for fn in callbacks:
            fn(status)
        return next_status
    else:
        raise TransitionException(status, next_status)


def get_next_statuses(status: str, rules: dict) -> list:
    """Return a list of all the next status.
    """
    next_statuses = rules[status].get('next', [])
    if '*' in next_statuses:
        return list(rules.keys())
    else:
        return next_statuses


def add_transition_callback(status: str, callback: callable, rules: dict) -> None:
    """Add a callback to the rules.
    """
    if 'callback' not in rules[status]:
        rules[status]['callback'] = []
    callbacks = rules[status].get('callback')
    callbacks.append(callback)


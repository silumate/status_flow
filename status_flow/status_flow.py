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

# Constants
CALLBACK_KEY = '_callback'


class TransitionException(Exception):
    """Exception for invalid transitions.
    """

    def __init__(self, curr_status: str, next_status: str):
        self.curr_status = curr_status
        self.next_status = next_status

    def __str__(self):
        return f'Invalid transition from {self.curr_status} to {self.next_status}'


class Status:
    """Class representing a status with transition rules.
    
    This class encapsulates the current status and the rules for transitions.
    It provides methods for transitioning between statuses, getting next possible
    statuses, and adding callbacks.
    """
    
    def __init__(self, initial_status: str, rules: dict):
        """Initialize a Status object.
        
        Args:
            initial_status: The initial status.
            rules: A dictionary defining the rules for transitions.
        """
        self.current = initial_status
        self.rules = rules
    
    def transition(self, next_status: str) -> str:
        """Transition to the next status based on the current status and the rules.
        
        Args:
            next_status: The status to transition to.
            
        Returns:
            The new status after the transition.
            
        Raises:
            TransitionException: If the transition is not allowed.
        """
        legal_statuses = self.rules[self.current].get('next', [])
        if '*' in legal_statuses or next_status in legal_statuses:
            callbacks = self.rules[next_status].get(CALLBACK_KEY, [])
            for fn in callbacks:
                fn(self.current)
            self.current = next_status
            return self.current
        else:
            raise TransitionException(self.current, next_status)
    
    def get_next_statuses(self) -> list:
        """Return a list of all the next possible statuses.
        
        Returns:
            A list of status names.
        """
        next_statuses = self.rules[self.current].get('next', [])
        if '*' in next_statuses:
            return list(self.rules.keys())
        else:
            return next_statuses
    
    def add_transition_callback(self, status: str, callback: callable) -> None:
        """Add a callback to be executed when transitioning to the specified status.
        
        Args:
            status: The status to add the callback for.
            callback: A callable that takes the previous status as an argument.
        """
        if CALLBACK_KEY not in self.rules[status]:
            self.rules[status][CALLBACK_KEY] = []
        callbacks = self.rules[status].get(CALLBACK_KEY)
        callbacks.append(callback)


# Status Flow

This is a simple library to define statuses and legal transitions between them. It provides methods to get states you can transition to and execute those transitions. You can also add callback methods that are triggered following a transition.

Status_flow is like a state machine, but rather than focusing on events (methods), it focuses on tracking status changes. This keeps the code simple and generic. The event handling can happen elsewhere, with a mechanism to add callback methods for event processing.

## Defining Statuses

The convenience of this library comes from how the statuses are defined in a dictionary. Each key is the name of a status, and the value for the keys is a new dictionary with data on the next legal status.

```python
temperature_status_rules = {
    'too hot': {
        'next': ['just right'],
    },
    'too cold': {
        'next': ['just right'],
    },
    'just right': {
        'next': ['too hot', 'too cold'],
    }
}
```

## Using the Status Class

The library provides a `Status` class that encapsulates the current status and transition rules:

```python
from status_flow import Status

# Define rules
temperature_status_rules = {
    'too hot': {
        'next': ['just right'],
    },
    'too cold': {
        'next': ['just right'],
    },
    'just right': {
        'next': ['too hot', 'too cold'],
    }
}

# Create a Status object with an initial status
room_status = Status('just right', temperature_status_rules)

# Get possible next statuses
possible_next = room_status.get_next_statuses()
print(possible_next)  # ['too hot', 'too cold']

# Transition to a new status
room_status.transition('too hot')
print(room_status.current)  # 'too hot'

# Add a callback
def too_hot_callback(prev_state):
    print(f"It's too hot now! It was {prev_state} before.")

room_status.add_transition_callback('too hot', too_hot_callback)
```

## Handling Illegal Transitions

When attempting an illegal transition, a `TransitionException` is raised:

```python
from status_flow import Status, TransitionException

# Define rules
temperature_status_rules = {
    'too hot': {
        'next': ['just right'],  # Can only go to 'just right' from 'too hot'
    },
    'too cold': {
        'next': ['just right'],  # Can only go to 'just right' from 'too cold'
    },
    'just right': {
        'next': ['too hot', 'too cold'],  # Can go to either 'too hot' or 'too cold' from 'just right'
    }
}

room_status = Status('too hot', temperature_status_rules)

try:
    # This will raise a TransitionException because we can't go directly from 'too hot' to 'too cold'
    room_status.transition('too cold')
except TransitionException as e:
    print(f"Error: {e}")  # Error: Invalid transition from too hot to too cold
```

See the unit tests for more examples.

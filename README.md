# Status Flow

This is a very simple library to define statuses, and legal transistions to other statuses.  It has a method for getting legal states you can transition to, and one to execute the transition.  You can also add callback methods following a transition.  

This code is not object oriented in order to keep things very simple.

Status_flow is like a state machine... but rather than focusing on events (methods), I focus on tracking status changes.  This keeps the code simple and generic.  The event handling can happen elsewhere.  I even provide a mechanism to add call-back methods to do event processing.

See the unit tests for examples.

# Defining Statuses
The convenience of this library comes from how the statuses are defined in a dictionary.  Each key is the name of a status and the value for the keys are a new dictionary with data on next legal status.

```
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

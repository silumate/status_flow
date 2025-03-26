import unittest
from status_flow import Status, TransitionException
import copy

# Common status rule definitions
TEMPERATURE_STATUS_RULES = {
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

KANBAN_STATUS_RULES = {
    'todo': {
        'next': ['*'],
    },
    'doing': {
        'next': ['*'],
    },
    'done': {
        'next': ['*'],
    },
}

class TestStatusClass(unittest.TestCase):
    """Tests for the new Status class."""
    
    def test_status_class_temperature_transition(self):
        room_status = Status('just right', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        room_status.transition('too hot')
        self.assertEqual(room_status.current, 'too hot')
        room_status.transition('just right')
        self.assertEqual(room_status.current, 'just right')
        room_status.transition('too cold')
        self.assertEqual(room_status.current, 'too cold')
    
    def test_status_class_kanban_transition(self):
        jira_issue = Status('todo', copy.deepcopy(KANBAN_STATUS_RULES))
        jira_issue.transition('doing')
        self.assertEqual(jira_issue.current, 'doing')
        jira_issue.transition('done')
        self.assertEqual(jira_issue.current, 'done')
        jira_issue.transition('todo')
        self.assertEqual(jira_issue.current, 'todo')
    
    def test_status_class_illegal_transition(self):
        room_status = Status('too hot', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        # from too hot, you can only go to just right
        with self.assertRaises(TransitionException):
            room_status.transition('too cold')
        self.assertEqual(room_status.current, 'too hot')
        room_status.transition('just right')
        room_status.transition('too cold')
        self.assertEqual(room_status.current, 'too cold')
        # from too cold, you can only go to just right
        with self.assertRaises(TransitionException):
            room_status.transition('too hot')
        self.assertEqual(room_status.current, 'too cold')
    
    def test_status_class_get_next_statuses(self):
        room_status = Status('just right', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        self.assertEqual(room_status.get_next_statuses(), ['too hot', 'too cold'])
        room_status.transition('too cold')
        self.assertEqual(room_status.get_next_statuses(), ['just right'])
        room_status.transition('just right')
        room_status.transition('too hot')
        self.assertEqual(room_status.get_next_statuses(), ['just right'])
        self.assertNotEqual(room_status.get_next_statuses(), ['just right', 'too cold'])
    
    def test_status_class_callback(self):
        room_status = Status('just right', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        msg = None

        def too_hot_callback(status: Status):
            nonlocal msg
            msg = f'It\'s too hot and it was {status.prev} before'

        def too_cold_callback(status: Status):
            nonlocal msg
            msg = f'It\'s too cold and it was {status.prev} before'

        def just_right_callback(status: Status):
            nonlocal msg
            msg = f'It\'s just right and it was {status.prev} before'

        room_status.add_transition_callback('too hot', too_hot_callback)
        room_status.add_transition_callback('too cold', too_cold_callback)
        room_status.add_transition_callback('just right', just_right_callback)

        room_status.transition('too hot')
        self.assertEqual(msg, 'It\'s too hot and it was just right before')
        room_status.transition('just right')
        self.assertEqual(msg, 'It\'s just right and it was too hot before')
        room_status.transition('too cold')
        self.assertEqual(msg, 'It\'s too cold and it was just right before')


    def test_constructor_invalid_status(self):
        """Test initializing with an invalid status."""
        with self.assertRaises(TransitionException):
            Status('invalid_status', copy.deepcopy(TEMPERATURE_STATUS_RULES))

    def test_wildcard_get_next_statuses(self):
        """Test get_next_statuses with wildcard."""
        jira_issue = Status('todo', copy.deepcopy(KANBAN_STATUS_RULES))
        # Should return all statuses when '*' is present
        self.assertEqual(set(jira_issue.get_next_statuses()), 
                        set(KANBAN_STATUS_RULES.keys()))

    def test_transition_to_nonexistent_status(self):
        """Test transitioning to a status not in the rules."""
        room_status = Status('todo', copy.deepcopy(KANBAN_STATUS_RULES))
        with self.assertRaises(TransitionException):
            room_status.transition('nonexistent_status')

    def test_multiple_callbacks(self):
        """Test multiple callbacks for the same status."""
        room_status = Status('just right', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        callback_results = []
        
        def callback1(status):
            callback_results.append('callback1')
        
        def callback2(status):
            callback_results.append('callback2')
        
        room_status.add_transition_callback('too hot', callback1)
        room_status.add_transition_callback('too hot', callback2)
        
        room_status.transition('too hot')
        # Check both callbacks were executed in order
        self.assertEqual(callback_results, ['callback1', 'callback2'])

    def test_transition_method_chaining(self):
        """Test that transition returns self for method chaining."""
        jira_issue = Status('todo', copy.deepcopy(KANBAN_STATUS_RULES))
        # This should work if transition returns self
        result = jira_issue.transition('doing').transition('done')
        self.assertEqual(result.current, 'done')
        self.assertEqual(jira_issue.current, 'done')

    def test_callback_exception(self):
        """Test behavior when a callback raises an exception."""
        room_status = Status('just right', copy.deepcopy(TEMPERATURE_STATUS_RULES))
        
        def failing_callback(status):
            raise ValueError("Callback error")
        
        room_status.add_transition_callback('too hot', failing_callback)
        
        #Exception propagates
        with self.assertRaises(ValueError):
            room_status.transition('too hot')

if __name__ == '__main__':
    unittest.main()

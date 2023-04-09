import unittest
from status_flow.status_flow import transition, get_next_statuses, TransitionException, add_transition_callback


class TestStatusFlow(unittest.TestCase):

    def test_temperature_transition(self):
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
        room_status = 'just right'
        room_status = transition(room_status, 'too hot', temperature_status_rules)
        self.assertEqual(room_status, 'too hot')
        room_status = transition(room_status, 'just right', temperature_status_rules)
        self.assertEqual(room_status, 'just right')
        room_status = transition(room_status, 'too cold', temperature_status_rules)
        self.assertEqual(room_status, 'too cold')

    def test_kanban_transition(self):
        kanban_status_rules = {
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
        jira_issue_status = 'todo'
        jira_issue_status = transition(jira_issue_status, 'doing', kanban_status_rules)
        self.assertEqual(jira_issue_status, 'doing')
        jira_issue_status = transition(jira_issue_status, 'done', kanban_status_rules)
        self.assertEqual(jira_issue_status, 'done')
        jira_issue_status = transition(jira_issue_status, 'todo', kanban_status_rules)
        self.assertEqual(jira_issue_status, 'todo')

    def test_illegal_transition(self):
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
        room_status = 'too hot'
        # from too hot, you can only go to just right
        with self.assertRaises(TransitionException):
            room_status = transition(room_status, 'too cold', temperature_status_rules)
        self.assertEqual(room_status, 'too hot')
        room_status = transition(room_status, 'just right', temperature_status_rules)
        room_status = transition(room_status, 'too cold', temperature_status_rules)
        self.assertEqual(room_status, 'too cold')
        # from too cold, you can only go to just right
        with self.assertRaises(TransitionException):
            room_status = transition(room_status, 'too hot', temperature_status_rules)
        self.assertEqual(room_status, 'too cold')

    def test_get_next_statuses(self):
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
        room_status = 'just right'
        self.assertEqual(get_next_statuses(room_status, temperature_status_rules), ['too hot', 'too cold'])
        room_status = transition(room_status, 'too cold', temperature_status_rules)
        self.assertEqual(get_next_statuses(room_status, temperature_status_rules), ['just right'])
        room_status = transition(room_status, 'just right', temperature_status_rules)
        room_status = transition(room_status, 'too hot', temperature_status_rules)
        self.assertEqual(get_next_statuses(room_status, temperature_status_rules), ['just right'])
        self.assertNotEqual(get_next_statuses(room_status, temperature_status_rules), ['just right', 'too cold'])

    def test_callback(self):
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
        room_status = 'just right'
        msg = None

        def too_hot_callback(prev_state: str):
            nonlocal msg
            msg = f'It\'s too hot and it was {prev_state} before'

        def too_cold_callback(prev_state: str):
            nonlocal msg
            msg = f'It\'s too cold and it was {prev_state} before'

        def just_right_callback(prev_state: str):
            nonlocal msg
            msg = f'It\'s just right and it was {prev_state} before'

        add_transition_callback('too hot', too_hot_callback, temperature_status_rules)
        add_transition_callback('too cold', too_cold_callback, temperature_status_rules)
        add_transition_callback('just right', just_right_callback, temperature_status_rules)

        room_status = transition(room_status, 'too hot', temperature_status_rules)
        self.assertEqual(msg, 'It\'s too hot and it was just right before')
        room_status = transition(room_status, 'just right', temperature_status_rules)
        self.assertEqual(msg, 'It\'s just right and it was too hot before')
        room_status = transition(room_status, 'too cold', temperature_status_rules)
        self.assertEqual(msg, 'It\'s too cold and it was just right before')


if __name__ == '__main__':
    unittest.main()

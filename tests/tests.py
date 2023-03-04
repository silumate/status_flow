import unittest
from state_machine.state_machine import transition, get_next_states, TransitionException


class TestStateMachine(unittest.TestCase):

    def test_temperature_transition(self):
        temperature_state_def = {
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
        room_state = 'just right'
        room_state = transition(room_state, 'too hot', temperature_state_def)
        self.assertEqual(room_state, 'too hot')
        room_state = transition(room_state, 'just right', temperature_state_def)
        self.assertEqual(room_state, 'just right')
        room_state = transition(room_state, 'too cold', temperature_state_def)
        self.assertEqual(room_state, 'too cold')

    def test_kanban_transition(self):
        kanban_state_def = {
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
        jira_issue_state = 'todo'
        jira_issue_state = transition(jira_issue_state, 'doing', kanban_state_def)
        self.assertEqual(jira_issue_state, 'doing')
        jira_issue_state = transition(jira_issue_state, 'done', kanban_state_def)
        self.assertEqual(jira_issue_state, 'done')
        jira_issue_state = transition(jira_issue_state, 'todo', kanban_state_def)
        self.assertEqual(jira_issue_state, 'todo')

    def test_illegal_transition(self):
        temperature_state_def = {
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
        room_state = 'too hot'
        with self.assertRaises(TransitionException):
            room_state = transition(room_state, 'too cold', temperature_state_def)
        self.assertEqual(room_state, 'too hot')
        room_state = transition(room_state, 'just right', temperature_state_def)
        room_state = transition(room_state, 'too cold', temperature_state_def)
        self.assertEqual(room_state, 'too cold')
        with self.assertRaises(TransitionException):
            room_state = transition(room_state, 'too hot', temperature_state_def)
        self.assertEqual(room_state, 'too cold')

    def test_get_next_states(self):
        temperature_state_def = {
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
        room_state = 'just right'
        self.assertEqual(get_next_states(room_state, temperature_state_def), ['too hot', 'too cold'])
        room_state = transition(room_state, 'too cold', temperature_state_def)
        self.assertEqual(get_next_states(room_state, temperature_state_def), ['just right'])
        room_state = transition(room_state, 'just right', temperature_state_def)
        room_state = transition(room_state, 'too hot', temperature_state_def)
        self.assertEqual(get_next_states(room_state, temperature_state_def), ['just right'])
        self.assertNotEqual(get_next_states(room_state, temperature_state_def), ['just right', 'too cold'])


if __name__ == '__main__':
    unittest.main()

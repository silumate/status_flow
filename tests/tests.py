import unittest
from state_machine import states


class TestStateMachine(unittest.TestCase):

    def test_temperature_transition(self):
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
        room_state = 'just right'
        room_state = states.transition(room_state, 'too hot', temperature_states)
        self.assertEqual(room_state, 'too hot')
        room_state = states.transition(room_state, 'just right', temperature_states)
        self.assertEqual(room_state, 'just right')
        room_state = states.transition(room_state, 'too cold', temperature_states)
        self.assertEqual(room_state, 'too cold')

    def test_kanban_transition(self):
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
        jira_issue_state = 'todo'
        jira_issue_state = states.transition(jira_issue_state, 'doing', kanban_states)
        self.assertEqual(jira_issue_state, 'doing')
        jira_issue_state = states.transition(jira_issue_state, 'done', kanban_states)
        self.assertEqual(jira_issue_state, 'done')
        jira_issue_state = states.transition(jira_issue_state, 'todo', kanban_states)
        self.assertEqual(jira_issue_state, 'todo')

    def test_illegal_transition(self):
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
        room_state = 'too hot'
        with self.assertRaises(states.TransitionException):
            room_state = states.transition(room_state, 'too cold', temperature_states)
        self.assertEqual(room_state, 'too hot')
        room_state = states.transition(room_state, 'just right', temperature_states)
        room_state = states.transition(room_state, 'too cold', temperature_states)
        self.assertEqual(room_state, 'too cold')
        with self.assertRaises(states.TransitionException):
            room_state = states.transition(room_state, 'too hot', temperature_states)
        self.assertEqual(room_state, 'too cold')


if __name__ == '__main__':
    unittest.main()

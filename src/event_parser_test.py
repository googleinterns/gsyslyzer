""" Module for unit testing the parsing of log events into event groups """

import unittest
from copy import copy

import event_parser, constants
from mocks import MockLogEvent

class EventParserTest(unittest.TestCase):
    """ Test suite for the event parser """
    def setUp(self):
        super(EventParserTest, self).setUp()

        # Set up fake event group rules for CAT and DOG groups
        self.tag_cat = "cat"
        self.trigger_tags_cat = ["C", "A", "T"]
        
        self.tag_dog = "dog"
        self.trigger_tags_dog = ["D", "O", "G"]
        self.context_tags_dog = ["X", "Y"]

        event_group_rule_cat = event_parser.EventGroupRule(self.tag_cat, self.trigger_tags_cat)
        event_group_rule_dog = event_parser.EventGroupRule(self.tag_dog, self.trigger_tags_dog,
                                              self.context_tags_dog)

        self.event_group_rules = [event_group_rule_cat, event_group_rule_dog]

    def get_test_case_event_parser(self, tags):
        """ Quick setup for different test cases """
        log_events = []
        for tag in tags:
            mock_log_event = MockLogEvent(tag)
            log_events.append(mock_log_event)

        log_event_parser = event_parser.LogEventParser(log_events,
                                                       self.event_group_rules)
        return log_event_parser
    
    def test_coinciding_events(self):
        test_tags = ["D", "D", "O", "O", "G", "G"]
        expected_num_groups_found = 2

        parser = self.get_test_case_event_parser(test_tags)
        parser.parse_log_events()
        
        groups_found = parser.event_groups_found
        num_groups_found = len(groups_found)

        self.assertEqual(num_groups_found, expected_num_groups_found)

    def test_overlapping_context_events(self):
        test_tags = ["Y", "D", "X", "O", "G", "D", "O", "G"]
        expected_num_groups_found = 2
        expected_num_all_events = 4

        parser = self.get_test_case_event_parser(test_tags)
        parser.parse_log_events()

        groups_found = parser.event_groups_found
        num_groups_found = len(groups_found)
        self.assertEqual(num_groups_found, expected_num_groups_found)

        for group in groups_found:
            num_all_events = len(group.all_log_events)
            self.assertEqual(num_all_events,expected_num_all_events)

    def test_noisy_events(self):
        test_tags = ["C", "NOISE", "D", "A", "X", "T", "O", "G", "G"]
        expected_num_groups_found = 2

        parser = self.get_test_case_event_parser(test_tags)
        parser.parse_log_events()

        groups_found = parser.event_groups_found
        num_groups_found = len(groups_found)
        self.assertEqual(num_groups_found, expected_num_groups_found)


if __name__ == "__main__":
    unittest.main()

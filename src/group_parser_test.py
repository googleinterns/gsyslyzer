""" Module for testing the group_parser"""

import unittest

import group_parser
import mocks

class GroupParserTest(unittest.TestCase):
    """ testing suite for the event group parser """
    def setUp(self):
        super(GroupParserTest, self).setUp()
       
        tags = ["A", "A", "A", "B", "C", "C", "A", "A"]
        self.criteria = mocks.MockCriteria(yes=["A", "C"])

        groups = []
        for tag in tags:
            groups.append(mocks.MockLogEventGroup(tag))

        self.groups = groups
        self.group_parser = group_parser.EventGroupParser(self.groups, [self.criteria])

    def test_burst_detection(self):
        self.group_parser.parse_event_groups()

        bursts = self.group_parser.burst_dict

        self.assertTrue("A" in bursts)
        self.assertEqual(len(bursts["A"]), 2)

        self.assertTrue("C" in bursts)
        self.assertEqual(len(bursts["C"]), 1)


if __name__ == "__main__":
    unittest.main()



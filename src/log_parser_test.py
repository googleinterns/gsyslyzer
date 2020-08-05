""" Module for unit testing the raw Gsys log parser """

import unittest

import log_parser
import event_rule
import constants

class LogParserTest(unittest.TestCase):
    """ Test suite for the log parser """
    def setUp(self):
        super(LogParserTest, self).setUp()

        self.path_to_fake_log = "test_data/fake_logs/log_parser_fake_log"

        self.fake_event_with_message_type = event_rule.EventRule("A", "(.*)(I'm a test event)(.*)", constants.MessageType.INFO)
        self.fake_event = event_rule.EventRule("B", "(.*)(I'm a different test event)(.*)")
        self.fake_events = [self.fake_event_with_message_type, self.fake_event]

        self.fake_parser = log_parser.LogParser(self.path_to_fake_log, self.fake_events)
   
    def test_extract_log_line_details(self):
        example_line = "I0924 00:33:03.847223   22675 init_google.cc:966] argv[0]: '/usr/local/bin/gsysd'"
        real_info = {
                        "message_type": "I",
                        "date": "0924",
                        "timestamp": "00:33:03.847223",
                        "thread_id": "22675",
                        "source_file": "init_google.cc",
                        "source_file_line_number": "966",
                        "message": "argv[0]: '/usr/local/bin/gsysd'"
                    }

        extracted_info = self.fake_parser.extract_log_line_details(example_line)

        for key in real_info.keys():
            self.assertEqual(real_info[key], extracted_info[key])

    def test_extract_year(self):
        line = "Log file created at: 2019/09/24 00:33:03"
        year = "2019"

        extracted_year = self.fake_parser.extract_year(line)

        self.assertEqual(extracted_year, year)


if __name__ == "__main__":
    unittest.main()

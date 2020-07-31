""" Module for parsing a raw Gsys log into predefined events """

import re
from datetime import datetime

import constants
from event_rule import EventRule
from log_event import LogEvent

class LogParser:
    """ Parser that loads, preproccesses, and extracts events from the
        raw Gsys log 
    
        Attributes
        ----------
        log_line_details_regex: compiled regex for extracting log line
        path_to_raw_log: relative path to raw log to be ingested
        raw_log: string of the entire raw log
        log_lines: list of string lines that comprise the log
        event_rules: list of EventRules to search for in the log
        log_events_found: list of chronological LogEvents found
        log_events_found_dict: dict of LogEvents found in the log with tag as key
    """

    def __init__(self, path_to_raw_log, event_rules):
        line_details_regex = constants.RegularExpressions.LOG_LINE_DETAILS_REGEX.value
        self.log_line_details_regex = re.compile(line_details_regex) 
        self.path_to_raw_log = path_to_raw_log
        self.event_rules = event_rules

        self.log_events_found = []
        self.log_events_found_dict = {}

        self.raw_log = self.load_log()
        self.log_lines = self.raw_log.split('\n')
        
    def load_log(self):
        try:
            with open(self.path_to_raw_log) as raw_log:
                loaded_log = str(raw_log.read())
                return loaded_log
        except:
            raise Exception("Something went wrong loading the log file.")

    def extract_year(self, line):
        creation_regex = constants.RegularExpressions.LOG_CREATION_REGEX.value
        log_creation_regex = re.compile(creation_regex)
        log_creation_match = log_creation_regex.match(line)

        if log_creation_match:
            return log_creation_match.group('year')
        return None

    def parse_log(self):
        first_line = True
        log_year = None

        for line in self.log_lines:

            if first_line:
                log_year = self.extract_year(line)
                first_line = False
                continue

            for rule in self.event_rules:
                result = self.apply_rule(line, rule)

                if result is not None:
                    tag = rule.tag

                    log_line_details_dict = self.extract_log_line_details(line)
                    log_line_details_dict['year'] = log_year
                    log_event = LogEvent(tag, log_line_details_dict, result)

                    self.log_events_found.append(log_event)
                    
                    if tag not in self.log_events_found_dict:
                        self.log_events_found_dict[tag] = [log_event]
                    else:
                        self.log_events_found_dict[tag].append(log_event)

    def convert_string_message_type_to_enum(self, line_message_type):
        options = {
            "I": constants.MessageType.INFO,
            "W": constants.MessageType.WARNING,
            "E": constants.MessageType.ERROR,
            "F": constants.MessageType.FAILURE
        }

        if line_message_type in options:
            message_type_enum = options[line_message_type]
        else:
            message_type_enum = None

        return message_type_enum

    def apply_rule(self, line, rule):
        rule_message_type = rule.message_type

        if rule_message_type is not None:
            message_str = line[0]
            line_message_type = constants.MessageType.from_str(message_str)
            
            if line_message_type is None or line_message_type != rule_message_type:
                return None

        match_object = rule.regular_expression.match(line)
        return match_object

    def extract_log_line_details(self, line):
        result = self.log_line_details_regex.match(line)
        if result:
            log_line_details_dict = result.groupdict()
        else:
            raise Exception("Bad file format.")

        return log_line_details_dict





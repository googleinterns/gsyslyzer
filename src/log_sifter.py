""" Module for completing end to end parsing of a log """

import json

import constants
import json_generator
import text_generator
from log_parser import LogParser
from event_parser import LogEventParser
from group_parser import EventGroupParser 
from symptom_burst import SymptomBurst
from symptom import Symptom
from signals import DetectedSignal
from log_event_group import LogEventGroup
from log_event import LogEvent

class LogSifter:
    """ Object for implementing the high level flow of parsing the log

        Attributes
        ----------
        log_file_path: string relative file path to the log
        event_rules: list of EventRule objects to be applied
        group_rules: list of EventGroupRules to be applied
        criterias: list of Criteria objects to be applied
        flags: argparse Parser object for storing the build flags from the CLI """

    def __init__(self, log_file_path, event_rules, group_rules, criterias, flags):
        self.log_file_path = log_file_path
        self.event_rules = event_rules
        self.group_rules = group_rules
        self.criterias = criterias
        self.flags = flags

    def sift_log(self):
        """ Implements the logical flow of the multiple parsing stages. """

        # Parse the raw log
        log_parser = LogParser(self.log_file_path, self.event_rules)
        log_parser.parse_log()
        log_events = log_parser.log_events_found

        # Parse the log events
        event_parser = LogEventParser(log_events, self.group_rules)
        event_parser.parse_log_events()
        event_groups = event_parser.event_groups_found

        collect_statistics = self.flags.collect_statistics

        # Parse the event groups
        group_parser = EventGroupParser(event_groups, self.criterias,
                                        collect_statistics)
        group_parser.parse_event_groups()
        statistics = group_parser.statistics_summaries

        # Construct the output
        if self.flags.json_output:
            self.output_to_json(group_parser, collect_statistics)
        else:
            self.output_to_terminal(group_parser)

    def output_to_terminal(self, group_parser):
        """ Outputs a listing of each symptom burst and its details to
            the terminal depending on the level of verbosity selected. """
        text_generator.TextGenerator(group_parser, self.flags.verbosity).write_output()
         

    def output_to_json(self, group_parser, statistics):
        """ Unpacks the group parser into json output then writes the
            results to gsyslyzeer_output.json. """
        json_generator.JsonGenerator(group_parser).write_output()


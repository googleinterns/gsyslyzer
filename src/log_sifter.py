""" Module for completing end to end parsing of a log """

import json

import constants
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
        flags: Objcet for storing the build flags from the CLI """

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
            self.output_to_json(group_parser, statistics)
        else:
            self.output_to_terminal(group_parser, statistics)

    def output_to_terminal(self, group_parser, statistics):
        """ Outputs a listing of each symptom burst and its details to
            the terminal depending on the level of verbosity selected. """

        burst_tags = list(group_parser.burst_dict.keys())
        burst_dict = group_parser.burst_dict
        burst_list = group_parser.bursts

        symptom_list = group_parser.symptoms_found

        if self.flags.verbosity == constants.VerbosityLevel.HIGH:
            for symptom in symptom_list:
                # come back to this after json rep is done.
                pass
        elif self.flags.verbosity == constants.VerbosityLevel.MEDIUM:
            for burst in burst_list:
                tag = burst.tag

                print("\n{0} Burst".format(tag))
                print("------------------------------------")
                print(burst.burst_start_timestamp)
                print("({0}) {1} symptoms detected.".format(burst.symptom_count, tag))
                print("Burst duration: {0}".format(burst.duration))
                print(burst.action_msg)
                print("------------------------------------")

        elif self.flags.verbosity == constants.VerbosityLevel.LOW:
            for tag in burst_tags:
                # Pull action message from first symptom in first burst
                burst = burst_dict[tag][0]
                print("\n{0}".format(tag))
                print("------------------------------------")
                print("{0} symptom detected.".format(tag))
                print(burst.action_msg)
                print("------------------------------------\n")
            

    def output_to_json(self, group_parser, statistics):
        """ Unpacks the group parser into json output then writes the
            results to gsyslyzeer_output.json. """

        dict_output = self.convert_to_dict(group_parser)
        with open("gsyslyzer_output.json", "w") as outfile:
            json.dump(dict_output, outfile)

    def convert_to_dict(self, object_to_translate):
        """ Recursively unpacks objects stored within the gorup parser
            to build JSON representations of the important pieces of
            data that should be reported to the user from each nested
            object. """

        if isinstance(object_to_translate, list):
            translated_list = []
            for item in object_to_translate:
                translated_list.append(self.convert_to_dict(item))

            return translated_list
        elif isinstance(object_to_translate, EventGroupParser):
            output = {}
            output["symptom_bursts"] = self.convert_to_dict(object_to_translate.bursts)
            output["statistics"] = object_to_translate.statistics_summaries

            return output
        elif isinstance(object_to_translate, SymptomBurst):
            output = object_to_translate.__dict__
            output["burst_start_timestamp"] = str(output["burst_start_timestamp"])
            output["duration"] = str(output["duration"])
            output["symptoms"] = self.convert_to_dict(output["symptoms"])

            return output
        elif isinstance(object_to_translate, Symptom):
            output = object_to_translate.__dict__
            output["start_timestamp"] = str(output["start_timestamp"])
            output["duration"] = str(output["duration"])
            output["signal"] = self.convert_to_dict(output["signal"])

            return output
        elif isinstance(object_to_translate, DetectedSignal):
            output = {}
            output["start_timestamp"] = str(object_to_translate.start_timestamp)
            output["duration"] = str(object_to_translate.duration)
            output["end_timestamp"] = str(object_to_translate.end_timestamp)
            
            if object_to_translate.interval is not None:
                output["interval"] = str(object_to_translate.interval)

            output["groups"] = self.convert_to_dict(object_to_translate.groups)

            return output
        elif isinstance(object_to_translate, LogEventGroup):
            output = {}
            output["tag"] = object_to_translate.tag
            all_events = object_to_translate.all_log_events
            output["ordered_events"] = self.convert_to_dict(all_events)

            return output
        elif isinstance(object_to_translate, LogEvent):
            output = object_to_translate.__dict__
            output["timestamp"] = str(output["timestamp"])

            return output


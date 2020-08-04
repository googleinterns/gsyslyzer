""" Module for writing Gsyslyzer output to the terminal. """

import constants

class TextGenerator:
    def __init__(self, group_parser, verbosity):
        self.group_parser = group_parser
        self.verbosity = verbosity

    def write_output(self):
        """ Outputs a listing of each symptom burst and its details to
            the terminal depending on the level of verbosity selected. """

        burst_tags = list(self.group_parser.burst_dict.keys())
        burst_dict = self.group_parser.burst_dict
        burst_list = self.group_parser.bursts

        symptom_list = self.group_parser.symptoms_found

        if self.verbosity == constants.VerbosityLevel.HIGH:
            for burst in burst_list:
                tag = burst.tag

                print("\n{0} Burst".format(tag))
                print("------------------------------------")
                print(burst.burst_start_timestamp)
                print("({0}) {1} symptoms detected.".format(burst.symptom_count, tag))
                print("Burst duration: {0}".format(burst.duration))
                print(burst.action_msg)
                print("------------------------------------")

        elif self.verbosity == constants.VerbosityLevel.LOW:
            for tag in burst_tags:
                # Pull action message from first symptom in first burst
                burst = burst_dict[tag][0]
                print("\n{0}".format(tag))
                print("------------------------------------")
                print("{0} symptom detected.".format(tag))
                print(burst.action_msg)
                print("------------------------------------\n")

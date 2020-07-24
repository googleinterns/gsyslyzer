from log_sifter import LogSifter

""" Module for providing an object that will ease the process of
    building a LogSifter object """

class SifterBuilder:
    """ Class for building a Sifter object """
    def __init__(self):
        self.event_rules = []
        self.group_rules = []
        self.criterias = []
        self.log_file_path = None

    def add_event_rule(self, rule):
        self.event_rules.append(rule)

    def add_group_rule(self, rule):
        self.group_rules.append(rule)

    def add_criteria(self, criteria):
        self.criterias.append(criteria)

    def build_sifter(self, flags):
        if not self.event_rules:
            raise Exception("BUILDER ERROR:\nBuilder has no event rules defined.")

        if not self.group_rules:
            raise Exception("BUILDER ERROR:\nBuilder has no group rules defined.")

        if not self.criterias:
            raise Exception("BUILDER ERROR:\nBuilder has no criteria defined.")

        log_file_path = flags.log_file_path
        sifter = LogSifter(log_file_path, self.event_rules, self.group_rules,
                           self.criterias, flags)

        return sifter

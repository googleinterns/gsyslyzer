""" Module for parsing event groups by applying criteria against them 
    to generate signals that will be evaluated to determine if group
    is symptomatic """

import copy

import symptom_burst

class EventGroupParser:
    """ Parser for applying criteria against event groups 

        Attributes
        ----------
        event_groups: list of LogEventGroup objects to be parsed
        criterias: list of criteria objects to be applied
        collect_statistics: boolean denoting if statistics should
                            be collected
        symptoms_found: chronological list of symptoms detected
        bursts: chronological list of symptom bursts detected
        burst_dict: dictionary of bursts with key of symtom tag
        statistics_summaries: dicitonary of statistics summary
                              with key of the signal tag that the
                              summary describes """

    def __init__(self, event_groups, criterias, collect_statistics=False):
        self.event_groups = event_groups
        self.criterias = criterias
        self.collect_statistics = collect_statistics

        self.symptoms_found = []
        self.bursts = []
        self.burst_dict = {}
        self.statistics_summaries = {}

    def parse_event_groups(self):
        """ Applies each criteria against the event groups and stores
            the results, and then detects bursts in the results. """

        detected_signals = []
        confirmed_signals = []

        for criteria in self.criterias:
            criteria_output = criteria.apply_criteria(self.event_groups,
                                                      self.collect_statistics)
            if self.collect_statistics:
                statistics_summary = criteria_output["statistics"]
                signal_tag = statistics_summary["signal_tag"]
                self.statistics_summaries[signal_tag] = statistics_summary

            symptoms = criteria_output["symptoms"]

            self.symptoms_found += symptoms
        
            detected_signals += criteria_output["detected_signals"]
            confirmed_signals += criteria_output["confirmed_signals"]

        self.detect_bursts(detected_signals, confirmed_signals)

    def detect_bursts(self, detected_signals, confirmed_signals):
        """ Loops through confirmed signals and detected signals to
            group together consecutive confirmed signals. """

        if len(confirmed_signals) == 0:
            return

        symptoms = copy.copy(self.symptoms_found)
        confirmed_signal = confirmed_signals.pop(0)
        related_symptom = symptoms.pop(0)
        prev_symptom_tag = None

        burst_list = []

        for signal in detected_signals:
            if signal == confirmed_signal:
                # Its definitely A symptom ... but is it part of current burst?
                if prev_symptom_tag is None:
                    # Its a brand new burst
                    prev_symptom_tag = related_symptom.tag
                    burst_list.append(related_symptom)

                    if len(confirmed_signals) > 0:
                        confirmed_signal = confirmed_signals.pop(0)
                        related_symptom = symptoms.pop(0)
                elif prev_symptom_tag == related_symptom.tag:
                    # Its part of the current burst
                    burst_list.append(related_symptom)

                    if len(confirmed_signals) > 0:
                        confirmed_signal = confirmed_signals.pop(0)
                        related_symptom = symptoms.pop(0)
                else:
                    # Its a different burst right after the current one
                    burst = symptom_burst.SymptomBurst(burst_list)
                    self.bursts.append(burst)

                    if prev_symptom_tag not in self.burst_dict:
                        self.burst_dict[prev_symptom_tag] = [burst]
                    else:
                        self.burst_dict[prev_symptom_tag].append(burst)

                    burst_list = [related_symptom]
                    prev_symptom_tag = related_symptom.tag

                    if len(confirmed_signals) > 0:
                        confirmed_signal = confirmed_signals.pop(0)
                        related_symptom = symptoms.pop(0)
            else:
                # The burst is broken by an innocent group
                if prev_symptom_tag is not None and len(burst_list) > 0:
                    burst = symptom_burst.SymptomBurst(burst_list)
                    self.bursts.append(burst)

                    if prev_symptom_tag not in self.burst_dict:
                        self.burst_dict[prev_symptom_tag] = [burst]
                    else:
                        self.burst_dict[prev_symptom_tag].append(burst)

                burst_list = []
                prev_symptom_tag = None


        # Check for leftover burst that did not get logged
        if prev_symptom_tag is not None and len(burst_list) > 0:
            burst = symptom_burst.SymptomBurst(burst_list)
            self.bursts.append(burst)

            if prev_symptom_tag not in self.burst_dict:
                self.burst_dict[prev_symptom_tag] = [burst]
            else:
                self.burst_dict[prev_symptom_tag].append(burst)

    def convert_to_dict(self):
        dict_form = {}
        dict_form["statistics"] = self.statistics_summaries
        dict_form["symptom_bursts"] = []
        
        for burst in self.bursts:
            converted_burst = burst.convert_to_dict()
            dict_form["symptom_bursts"].append(converted_burst)

        return dict_form

""" Module for defining criteria to be used to evaluate event groups. """

from symptom import Symptom
from signal_statistics import SignalStatistics
import constants

class Criteria:
    """ Object for detecting and evaluating signals resulting from
        event groups. Given some symptom tag, a signal to detect,
        and an evaluator for that signal, the criteria will detect
        and build instances of these symptoms

        Attributes
        ----------
        symptom_tag: string name for the symptom this criteria defines
        signal: signal object to detect
        evaluator: evaluator object to apply to detected signals
        action_msg: string message to build into a detcted symptom

    """

    def __init__(self, symptom_tag, signal, evaluator, action_msg):
        self.symptom_tag = symptom_tag
        self.signal = signal
        self.evaluator = evaluator
        self.action_msg = action_msg

    def apply_criteria(self, event_groups, collect_statistics):
        """ Detects signals and applies an evaluator to them. Those
            that are confirmed are then built into symptom instances.
            If the collect_statistics flag is marked, then the 
            SignalStatistics module is used to collect statistics. """

        detected_signals = self.signal.detect_signals(event_groups)
        confirmed_signals = self.evaluator.evaluate_signals(detected_signals)

        symptoms = self.build_symptoms(confirmed_signals)
        output_dict = {
            "symptoms": symptoms,
            "detected_signals": detected_signals,
            "confirmed_signals": confirmed_signals.keys()
        }

        if collect_statistics:
            stat_summary = SignalStatistics().collect_signal_stats(detected_signals)
            output_dict["statistics"] = stat_summary

        return output_dict

    def build_symptoms(self, signals):
        """ Creates a symptom instance for each of the confirmed
            signals given. """

        symptoms = []
        for signal in signals:
            symptom = Symptom(self.symptom_tag, self.action_msg, signal)
            symptoms.append(symptom)

        return symptoms

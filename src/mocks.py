import re
from datetime import datetime

from log_parser import LogEvent

class MockLogEvent:
    """ Mock for a LogEvent object """ 
    def __init__(self, tag, timestamp=None, is_context=None):
        self.tag = tag
        self.timestamp = timestamp
        self.is_context = is_context

class MockLogEventGroup:
    """ Mock object for an LogEventGroup object """
    def __init__(self, tag, all_mock_events=None):
        self.tag = tag
        self.trigger_log_events = []
        self.context_log_events = []
        self.all_log_events = []

        if all_mock_events is not None:
            for mock_event in all_mock_events:
                if mock_event.is_context:
                    self.context_log_events.append(mock_event)
                else:
                    self.trigger_log_events.append(mock_event)

                self.all_log_events.append(mock_event)

class MockSymptom:
    """ Mock for a detected Symptom object """
    def __init__(self, tag, duration=0):
        self.tag = tag
        self.start_timestamp = 0
        self.action_msg = "Do Nothing."
        self.duration = duration

class MockCriteria:
    """ Mock for any <criteria type>Criteria object """
    def __init__(self, yes=[]):
        self.yes = yes

    def apply_criteria(self, event_groups, collect_statistics):
        symptoms = []
        detected_signals = []
        confirmed_signals = []

        for group in event_groups:
            if group.tag in self.yes:
                symptoms.append(MockSymptom(group.tag))
                confirmed_signals.append(group.tag)

            detected_signals.append(group.tag)

        mocked_output = {
            "detected_signals": detected_signals,
            "confirmed_signals": confirmed_signals,
            "symptoms": symptoms
        }

        return mocked_output


""" Module for defining the different types of signals that can be 
    extracted from a list of event groups. """

import datetime

class DetectedSignal:
    """ Object for representing a signal that has been found """
    def __init__(self, tag, time, groups):
        self.tag = tag
        self.groups = groups

        if isinstance(time, datetime.timedelta):
            self.interval = time
        else:
            self.interval = None

        self.start_timestamp = groups[0].trigger_log_events[0].timestamp
        self.end_timestamp = groups[-1].trigger_log_events[-1].timestamp
        self.duration = self.end_timestamp - self.start_timestamp

    def convert_self_to_dict(self):
        dict_form = {}
        dict_form["start_timestamp"] = str(self.start_timestamp)
        dict_form["duration"] = str(self.duration)
        dict_form["end_timestamp"] = str(self.end_timestamp)
            
        if self.interval is not None:
            dict_form["interval"] = str(dict_form.interval)

        dict_form["groups"] = []
        for group in self.groups:
            converted_group = group.convert_self_to_dict()
            dict_form["groups"].apppend(converted_group)

        return output

class IntervalGroupSignal:
    """ Interval signal detector for event groups """
    def __init__(self, tag, start_group_tag, end_group_tag):
        self.tag = tag
        self.start_group_tag = start_group_tag
        self.end_group_tag = end_group_tag

    def detect_signals(self, event_groups):
        """ Loops through event groups and creates a DetectedSignal for
            each time delta between the start and end event group. """

        signals = []
        start_group_queue = []

        for group in event_groups:
            tag = group.tag

            if tag == self.start_group_tag:
                start_group_queue.append(group)
            elif tag == self.end_group_tag:
                if len(start_group_queue) > 0:
                    start_group = start_group_queue.pop(0)
            
                    start_timestamp = start_group.trigger_log_events[-1].timestamp
                    end_timestamp = group.trigger_log_events[0].timestamp
                    timedelta = end_timestamp - start_timestamp

                    detected_signal = DetectedSignal(self.tag, timedelta, 
                                                     [start_group, group])
                    signals.append(detected_signal)

        return signals

class RepeatGroupSignal:
    """ Repeating group signal detector """
    def __init__(self, tag, group_tag):
        self.tag = tag
        self.group_tag = group_tag
        
    def detect_signals(self, event_groups):
        """ Loops through event groups and creates a DetectedSignal for
            each time delta between repeats of the given event group. """

        signals = []

        start_group = None
        for group in event_groups:
            if group.tag == self.group_tag:
                if start_group is not None:
                    start_timestamp = start_group.trigger_log_events[-1].timestamp
                    end_timestamp = group.trigger_log_events[0].timestamp
                    timedelta = end_timestamp - start_timestamp

                    detected_signals = DetectedSignal(self.tag, timedelta, 
                                                      [start_group, group])
                    signals.append(detected_signals)

                start_group = group

        return signals

class ExistenceGroupSignal:
    """ Object for detecting existence of a group """
    def __init__(self, tag, group_tag):
        self.tag = tag
        self.group_tag = group_tag

    def detect_signals(self, event_groups):
        """ Loops through event groups and creates a DetctedSignal for
            each occurence of the given event group. """

        signals = []
        for group in event_groups:
            if group.tag == self.group_tag:
                timestamp = group.trigger_log_events[0].timestamp
                detected_signal = DetectedSignal(self.tag, timestamp, [group])
                signals.append(detected_signal)

        return signals

class IntervalEventSignal:
    """ Object for intervals between events rather than groups"""
    def __init__(self, tag, group_tag, start_event_tag, end_event_tag):
        self.tag = tag
        self.group_tag = group_tag
        self.start_event_tag = start_event_tag
        self.end_event_tag = end_event_tag
    
    def detect_signals(self, event_groups):
        """ Loops through event groups and creates a DetectedSignal for
            the interval between each start and end event within the 
            given event group. """

        signals = []

        for group in event_groups:
            if group.tag == self.group_tag:
                events = group.all_log_events
                start_time = None

                for event in events:
                    event_tag = event.tag

                    if event_tag == self.start_event_tag:
                        start_time = event.timestamp
                    elif event_tag == self.end_event_tag and start_time is not None:
                        end_time = event.timestamp
                        timedelta = end_time - start_time
                        detected_signal = DetectedSignal(self.tag, timedelta, [group])
                        signals.append(detected_signal)

        return signals


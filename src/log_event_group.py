""" Module for defining an object representation of a detected event group """

class LogEventGroup:
    """ Stores the details of a singular occurence of an event group 
        
        Attributes
        ----------
        tag: Label for the event group
        trigger_log_events: ordered list of events that comprise
                            an event group
        context_log_events: list of context events
        all_log_events: chonological order of all events"""

    def __init__(self, tag, trigger_log_events=[], context_log_events=[],
                 all_log_events=[]):

        self.tag = tag
        self.trigger_log_events = trigger_log_events
        self.context_log_events = context_log_events
        self.all_log_events = all_log_events

    def add_log_event(self, trigger_log_event=None, context_log_event=None):
        if trigger_log_event is not None and context_log_event is not None:
            raise Exception("LogEventGroup Error: Only one event is addable at a time.")
        elif trigger_log_event is not None:
            event = trigger_log_event
            self.trigger_log_events.append(event)
        elif context_log_event is not None:
            event = context_log_event
            self.context_log_events.append(event)

        self.all_log_events.append(event)

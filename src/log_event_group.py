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

    def convert_self_to_dict(self):
        """ Converts self to dictionary form for json output """

        dict_form = {}
        dict_form["tag"] = self.tag
        all_events = self.all_log_events
        dict_form["ordered_events"] = []

        for event in all_events:
            converted_event = event.convert_self_to_dict()
            dict_form["ordered_events"].append(converted_event)

        return dict_form 

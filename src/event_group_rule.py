""" Module for defining a rule to group together events """

class EventGroupRule:
    """ Defines the tags that make up an event group and any conextual
        events that should be parsed as well. Also defines if
        statistics should be collected for this specific event group
        
        Attributes
        tag: label for the rule
        trigger_event_tags: list of tags associated to LogEvents
                            and that define the event group
        context_event_tags: list of tags associated to LogEvents
                            and that supply context to event group """

    def __init__(self, tag, trigger_event_tags, context_event_tags=[]):
        self.trigger_event_tags = trigger_event_tags
        self.context_event_tags = context_event_tags
        self.tag = tag

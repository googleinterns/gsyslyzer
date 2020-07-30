from datetime import datetime
from event_group_rule import EventGroupRule
from log_event_group import LogEventGroup
from log_parser import LogEvent, LogParser

""" Module for parsing Log Events into Event Groups """

class LogEventParser:
    """ Parser for applying group rules against a list of events to
        create instances of event groups
        
        Attributes
        ----------
        log_events: list of LogEvent objects to be parsed
        event_group_rules: list of EventGroupRule objects to be applied
                           for event grouping
        event_groups_found: chronological list list of detected 
                            LogEventGroup objects
        event_groups_found_dict: dictionary of LogEventGroups where
                                 key is the group tag """

    def __init__(self, log_events, event_group_rules):
        self.log_events = log_events
        self.event_group_rules = event_group_rules

        self.event_groups_found = []
        self.event_groups_found_dict = {}

    def get_event_search_dict(self, event_group_rule):
        """ Initializes a search dictionary for tracking whether a group 
        has attained all required events, a partial gorup will sit
        in a queue with key of the next event it needs

        ex: Group requires C, A, and T
            Two partial groups exist; one with C and A, one with just C
            search_dict: {
                "C": []
                "A": [[C]] # needs an A next
                "T": [[C, A]] # needs a T next
            } 
            
        Uses queues to ensure first occurences of events are grouped
        together """

        search_dict = {tag: [] for tag in event_group_rule.trigger_event_tags}
        return search_dict

    def update_search_dict(self, group_tag, search_dict, event, context_event_buffer):
        """ Moves partial groups from stage to stage in the search dict,
        or stores them as valid if they complete """
        
        ordered_tags = list(search_dict.keys())
        event_tag = event.tag
        tag_index = ordered_tags.index(event_tag)
        next_tag_index = tag_index + 1

        if tag_index == 0 and next_tag_index == len(ordered_tags):
            # In the special case that a group only requires one event
            # the current context buffer and first event found are 
            # immediately grouped and stored as a valid group.
            all_log_events = context_event_buffer + [event]
            
            event_group = LogEventGroup(tag=group_tag, trigger_log_events=[event],
                                        context_log_events=context_event_buffer,
                                        all_log_events=all_log_events)

            self.event_groups_found.append(event_group)

            if group_tag not in self.event_groups_found_dict:
                self.event_groups_found_dict[group_tag] = [event_group]
            else:
                self.event_groups_found_dict[group_tag].append(event_group)
            
            context_event_buffer = []
        elif tag_index == 0:
            # In the case that the first event is found, the
            # context buffer and the event found are grouped into a 
            # partial group and stored in the search dictionary.
            all_log_events = context_event_buffer + [event]
            
            event_group = LogEventGroup(tag=group_tag, trigger_log_events=[event],
                                        context_log_events=context_event_buffer,
                                        all_log_events=all_log_events)

            context_event_buffer = []
            
            next_tag = ordered_tags[next_tag_index]
            search_dict[next_tag].append(event_group)
        elif next_tag_index == len(ordered_tags):
            # In the case that the last event is found, the partial
            # group is removed from the search dictionary and 
            # stored as a valid group.
            partial_groups_list = search_dict[event_tag]

            if len(partial_groups_list) > 0:
                event_group = partial_groups_list.pop(0)
                event_group.add_log_event(event)
            
                self.event_groups_found.append(event_group)

                if group_tag not in self.event_groups_found_dict:
                    self.event_groups_found_dict[group_tag] = [event_group]
                else:
                    self.event_groups_found_dict[group_tag].append(event_group)
        else:
            # In the case that it is some other relevant event, the
            # event is added to the partial group at the front of the
            # current queue and then pushed to the next queue.
            event_group = search_dict[event_tag].pop(0)
            event_group.add_log_event(event)
            
            next_tag = ordered_tags[next_tag_index] 
            search_dict[next_tag].append(event_group)

        return context_event_buffer

    def parse_log_events(self):
        """ Driving method for parsing the log events. Each rule is applied
        to the full log event set. Context events are grouped in a 
        buffer until the first trigger event in their group is seen, 
        and then they are grouped with that instance. """

        for rule in self.event_group_rules:
            search_dict = self.get_event_search_dict(rule)
            context_tags = rule.context_event_tags
            context_event_buffer = []
            group_tag = rule.tag

            for event in self.log_events:
                tag = event.tag
                if tag in search_dict:
                    context_event_buffer = self.update_search_dict(group_tag,
                                                                   search_dict, event, 
                                                                   context_event_buffer)
                elif tag in context_tags:
                    context_event_buffer.append(event)


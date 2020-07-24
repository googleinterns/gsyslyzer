import re

import constants

""" Module for defining a rule to classify log lines into events """

class EventRule:
    """ A rule that can be applied to a line of the log to check for an event
    
        Attributes
        ----------
        tag: A string name for the event
        regular_expression: A string holding the regular expression for
                            a specific event
        message_type [optional]: An int enum for the type of message the
                                 log produces for this event 
    """

    def __init__(self, tag, regular_expression, message_type=None):
        allowed_message_types = [constants.MessageType.INFO,
                                 constants.MessageType.WARNING,
                                 constants.MessageType.ERROR,
                                 constants.MessageType.FAILURE] 
        
        if message_type is None or message_type in allowed_message_types:
            self.message_type = message_type
        else:
            raise Exception("Provided message type does not exist.")

        try:
            self.regular_expression = re.compile(regular_expression)
        except:
            raise Exception("Provided regular expression is invalid.")

        self.tag = tag

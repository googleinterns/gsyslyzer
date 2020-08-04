""" Module for definig an instance of a detected symptom """

class Symptom:
    """ An object to represent an occurence of a specific symptom"""
    def __init__(self, tag, action_msg, signal):
        self.tag = tag
        self.action_msg = action_msg
        self.signal = signal
        self.start_timestamp = signal.start_timestamp
        self.duration = signal.duration

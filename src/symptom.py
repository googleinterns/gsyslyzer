""" Module for definig an instance of a detected symptom """

class Symptom:
    """ An object to represent an occurence of a specific symptom"""
    
    def __init__(self, tag, action_msg, signal):
        self.tag = tag
        self.action_msg = action_msg
        self.signal = signal
        self.start_timestamp = signal.start_timestamp
        self.duration = signal.duration

    def convert_to_dict(self):
        dict_form = self.__dict__
        dict_form["start_timestamp"] = str(dict_form["start_timestamp"])
        dict_form["duration"] = str(dict_form["duration"])
        dict_form["signal"] = dict_form["signal"].convert_to_dict()

        return dict_form

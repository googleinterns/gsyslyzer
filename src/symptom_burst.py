""" Module for defining a series of back to back symptom occurences """

import datetime

class SymptomBurst:
    """ Object for defining the collection of symtpoms that occured
        in succession 
        
        Attributes
        ----------
        symptoms: list of Symptom objects
        burst_start_timestamp: datetime object for the start of a burst
        action_msg: String action that is relayed to user
        tag: String identifier for this type of symptom burst
        symptom_count: int count of all symptom occurences
        duration: datetime.timedelta of the total time of the burst
        """

    def __init__(self, symptoms):
        self.symptoms = symptoms
        self.burst_start_timestamp = symptoms[0].start_timestamp
        self.action_msg = symptoms[0].action_msg
        self.tag = symptoms[0].tag
        self.symptom_count = len(symptoms)

        duration = datetime.timedelta(seconds=0)
        for symptom in symptoms:
            duration += symptom.duration

        self.duration = duration

    def convert_to_dict(self):
        """ Converts self to a dict form for json output """
        
        dict_form = self.__dict__
        dict_form["burst_start_timestamp"] = str(dict_form["burst_start_timestamp"])
        dict_form["duration"] = str(dict_form["duration"])
        dict_form["symptoms"] = []
        
        for symptom in self.symptoms:
            converted_symptom = symptom.convert_to_dict()
            dict_form["symptoms"].append(converted_symptom)

        return dict_form

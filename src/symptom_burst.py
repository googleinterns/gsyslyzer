""" Module for defining a series of back to back symptom occurences """

class SymptomBurst:
    """ Object for defining the collection of symtpoms that occured
        in succession """

    def __init__(self, symptoms):
        self.symptoms = symptoms
        self.burst_start_timestamp = symptoms[0].start_timestamp
        self.action_msg = symptoms[0].action_msg
        self.tag = symptoms[0].tag
        self.symptom_count = len(symptoms)

        duration = 0
        for symptom in symptoms:
            duration += symptom.duration

        self.duration = duration

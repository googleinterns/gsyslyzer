""" Module for generating a json object representation of Gsyslyzer 
    the output. """

import json

class JsonGenerator:
    def __init__(self, group_parser):
        self.group_parser = group_parser

    def write_output(self):
        """ Unpacks the group parser into json output then writes the
            results to gsyslyzeer_output.json. """

        dict_output = self.convert_to_dict(self.group_parser)
        with open("gsyslyzer_output.json", "w") as outfile:
            json.dump(dict_output, outfile, indent=4)

    def convert_to_dict(self, object_to_translate):
        """ Recursively unpacks objects stored within the group parser
            to build JSON representations of the important pieces of
            data that should be reported to the user from each nested
            object. """

        if isinstance(object_to_translate, list):
            translated_list = []
            for item in object_to_translate:
                translated_list.append(self.convert_to_dict(item))

            return translated_list
        else:
            return object_to_translate.convert_self_to_dict()

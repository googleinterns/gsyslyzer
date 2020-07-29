from datetime import datetime

""" Module for defining an object representation for a detected event in the log """

class LogEvent:
    """ A condensed representation of a line in the log that matched
        with an EventRule. 
    
        Attributes
        ----------
        event_rule_match_object: re match object produced by LogParser
        tag: a string name for the event
        timestamp: string time when source line was logged 
                   format: ["hh:mm:ss.uuuuuu"]
        date: string date when source line was logged 
              format: ["mmdd"]
        thread_id: thread id from source line
        source_file: file that logged the line
        source_file_line_number: line number of source file that logged
                                 the source line
        message_type: int enum for type of message produced in log
        message: raw string message from the log
        message_groups_dict: dictionary of separate events and their
                             matched data from the matched EventRule
                             regular_expression
    """
    def __init__(self, tag, log_line_details_dict, event_rule_match_object):
        self.tag = tag

        # Here, we get all the info we can from the match object
        self.message_groups_dict = event_rule_match_object.groupdict()

        # The rest of the attributes are details about the log line
        self.message_type = log_line_details_dict["message_type"]
        self.timestamp = log_line_details_dict["timestamp"] 
        self.date = log_line_details_dict["date"]
        self.year = log_line_details_dict["year"]
        self.thread_id = log_line_details_dict["thread_id"]
        self.source_file = log_line_details_dict["source_file"]
        self.source_file_line_number = log_line_details_dict["source_file_line_number"]
        self.message = log_line_details_dict["message"]

        # Placeholder for ms converted timestamp
        self.timestamp = self.get_timestamp()

    def get_timestamp(self):
        year_str = self.year
        date_str = self.date
        time_str = self.timestamp

        month_str = date_str[:2]
        day_str = date_str[2:]

        # Must convert all the strs into an iso format date
        iso_date_str = year_str + "-" + month_str + "-" + day_str + "T" + time_str
        timestamp = datetime.fromisoformat(iso_date_str)

        return timestamp


""" Module for defining constants used in this project """

import enum

class VerbosityLevel(enum.IntEnum):
    """ Define levels of output verbosity"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class MessageType(enum.IntEnum):
    """ Define message types """
    INFO = 0
    WARNING = 1
    ERROR = 2
    FAILURE = 3
    
    @staticmethod
    def from_log_prefix(self, string_message):
        mapping = {
            "I": INFO,
            "W": WARNING,
            "E": ERROR,
            "F": FAILURE
        }

        if string_message in mapping:
            return mapping[string_message]

        return None

class RegularExpressions(enum.Enum):
    """ Define constant regular expressions """
    MESSAGE_TYPE_REGEX = r"(?P<message_type>[IWEF]{1})"
    DATE_REGEX = r"(?P<date>\d{4})"
    TIMESTAMP_REGEX = r"(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d{6})"
    THREAD_ID_REGEX = r"(?P<thread_id>\d*)"
    SOURCE_FILE_REGEX = r"(?P<source_file>\w*\.{1}\w*)"
    LINE_NUMBER_REGEX = r"(?P<source_file_line_number>\d*)"
    MESSAGE_REGEX = r"(?P<message>.*)"

    LOG_CREATION_REGEX = (r"(Log file created at:)\s*(?P<year>\d{4})(/)"
                        + r"(?P<month>\d{2})(/)(?P<day>\d{2})\s*(?P<time>.*)")

    LOG_LINE_DETAILS_REGEX = (MESSAGE_TYPE_REGEX
                            + "\s*"
                            + DATE_REGEX
                            + "\s*"
                            + TIMESTAMP_REGEX
                            + "\s*"
                            + THREAD_ID_REGEX
                            + "\s*"
                            + SOURCE_FILE_REGEX
                            + ":"
                            + LINE_NUMBER_REGEX
                            + "(\]{1})\s*"
                            + MESSAGE_REGEX)

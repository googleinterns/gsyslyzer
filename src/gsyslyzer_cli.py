""" Module for defining the CLI usage. """

import argparse

class Gsyslyzer:
    """ Object for building and running a complete sifting pipeline
    
        Attributes
        ----------
        builder: SifterBuilder object for bulding the LogSifter
        flags: object storing attributes given as cli flags"""

    def __init__(self, builder):
        self.builder = builder

        parser = argparse.ArgumentParser(description="Gsyslyzer CLI")
        parser.add_argument("--verbosity", default=0, 
                            type=int, help=("0: Symptom summary "
                                            "1: All symptom bursts"))
        parser.add_argument("--collect_statistics", default=False, 
                            type=bool, help=("Set True to collect signal statistics"))
        parser.add_argument("--json_output", default=False, help=("Set True to write output "
                                                                  "to gsift_output.json"))
        parser.add_argument("--log_file_path", required=True)

        self.flags = parser.parse_args()

    def run(self):
        log_sifter = self.builder.build_sifter(self.flags)
        log_sifter.sift_log()

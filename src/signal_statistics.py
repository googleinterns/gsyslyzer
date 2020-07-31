""" Module for collecting statistics on occcurences of signals """

import numpy as np

class SignalStatistics:
    """ Object for parsing over signals and collecting statistics about
        occurence rates, durations, and interval """
    def __init__(self):
        pass

    def collect_signal_stats(self, signals):
        """ Loops through the given signals and adds their hour of
            occurrence, duration, and interval since last occurence to
            their respective datasets. """

        occurence_rate_data = {}
        duration_data = []
        interval_data = []

        signal_tag = signals[0].tag

        for signal in signals:
            duration = signal.duration
            hour = signal.start_timestamp.hour
            interval = signal.interval
            
            if hour not in occurence_rate_data:
                occurence_rate_data[hour] = 1
            else:
                occurence_rate_data[hour] += 1
            
            duration_data.append(duration.total_seconds())
            if interval is not None:
                interval_data.append(interval.total_seconds())

        summary = self.get_summary(signal_tag, occurence_rate_data,
                                   duration_data, interval_data)
        return summary

    def get_summary(self, signal_tag, occurence_rate_data, 
                    duration_data, interval_data):
        """ Makes the NumPy calls to calculate the actual statistics
            and groups all these together into a summary dicitonary. """

        all_hours = list(occurence_rate_data.keys())
        hour_span = np.max(all_hours) - np.min(all_hours)
        hourly_rate = np.sum(list(occurence_rate_data.values())) / float(hour_span)

        durations = np.array(duration_data)
        duration_mean = np.mean(durations)
        duration_std = np.std(durations)
        duration_max = np.max(durations)
        duration_min = np.min(durations)

        intervals = np.array(interval_data)

        if len(intervals) > 0:
            interval_mean_s = np.mean(intervals)
            interval_std_s = np.std(intervals)
            interval_max_s = np.max(intervals)
            interval_min_s = np.min(intervals)
        else:
            interval_mean_s = None
            interval_std_s = None
            interval_max_s = None
            interval_min_s = None

        summary_dict = {
            "signal_tag": signal_tag,
            "hourly_rate": hourly_rate,
            "durations_data_seconds": {
                "mean": duration_mean,
                "std": duration_std,
                "max": duration_max,
                "min": duration_min
            },
            "interval_data_seconds": {
                "mean": interval_mean_s,
                "std": interval_std_s,
                "max": interval_max_s,
                "min": interval_min_s,
            }
        }

        return summary_dict

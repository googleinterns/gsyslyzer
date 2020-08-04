import unittest
import datetime

import signals
from mocks import MockLogEvent, MockLogEventGroup

class SignalsTest(unittest.TestCase):
    def setUp(self):
        super(SignalsTest, self).setUp()

        # Used to define the fake groups and their events for testing
        group_definition_dict = {
            "A": {
                "trigger": ["x", "y"],
                "context": ["z", "a"]
            },
            "C": {
                "trigger": ["q", "r"],
                "context": ["s", "t"]
            },
            "T": {
                "trigger": ["r", "s", "t"],
                "context": ["u"]
            }
        }

        group_tag_order = ["C", "C", "A", "T", "A", "T", "T", "A", "C"]
        mock_event_groups = []

        fake_timestamp = 0

        for group_tag in group_tag_order:
            all_events = []
            
            group_definition = group_definition_dict[group_tag]
            
            for context_tag in group_definition["context"]:
                context_event = MockLogEvent(tag=context_tag, timestamp=fake_timestamp,
                                             is_context=True)
                all_events.append(context_event)

                fake_timestamp += 1

            for trigger_tag in group_definition["trigger"]:
                trigger_event = MockLogEvent(tag=trigger_tag, timestamp=fake_timestamp)
                all_events.append(trigger_event)

                fake_timestamp += 1

            mock_event_group = MockLogEventGroup(tag=group_tag, all_mock_events=all_events)
            mock_event_groups.append(mock_event_group)


        self.mock_event_groups = mock_event_groups

    def test_signal_detection_for_group_intervals(self):
        signal = signals.IntervalGroupSignal(tag="C_T_interval_signal",
                                             start_group_tag="C",
                                             end_group_tag="T")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check that overlapping intervals were correctly detected
        # There should only be two detected signals
        # C:0 => T:12
        # C:4 => T:20

        self.assertEqual(len(detected_signals), 2)

    def test_signal_detection_for_repeat_groups(self):
        signal = signals.RepeatGroupSignal(tag="A_repeat_signal", group_tag="A")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # check that both repeats were detected
        # A:8 => A:16
        # A:16 => A:28

        self.assertEqual(len(detected_signals), 2)

    def test_signal_detection_for_existing_group(self):
        signal = signals.ExistenceGroupSignal(tag="C_exists_signal", group_tag="C")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check all C's detected
        # C:0, C:4, and C:32

        self.assertEqual(len(detected_signals), 3)

    def test_sginal_detection_for_non_existing_group(self):
        signal = signals.ExistenceGroupSignal(tag="NOISE_exists_signal", 
                                              group_tag="NOISE")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check that zero noisy signals detected
        self.assertEqual(len(detected_signals), 0)

    def test_signal_detection_for_context_to_context_interval(self):
        signal = signals.IntervalEventSignal(tag="s_t_event_interval_signal",
                                             group_tag="C",
                                             start_event_tag="s",
                                             end_event_tag="t")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check that there are 3 signals, all with same interval
        # should be one for each C BUT NOT for T

        self.assertEqual(len(detected_signals), 3)

    def test_signal_detection_for_trigger_to_trigger_interval(self):
        signal = signals.IntervalEventSignal(tag="x_y_event_interval_signal",
                                             group_tag="A",
                                             start_event_tag="x",
                                             end_event_tag="y")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check that there are 3 signals, all with same interval
        # One for each A

        self.assertEqual(len(detected_signals), 3)

    def test_signal_detection_for_context_to_trigger_interval(self):
        signal = signals.IntervalEventSignal(tag="t_u_event_interval_signal",
                                             group_tag="T",
                                             start_event_tag="u",
                                             end_event_tag="t")
        detected_signals = signal.detect_signals(self.mock_event_groups)

        # Check that there are 3 signals
        # One for each T

        self.assertEqual(len(detected_signals), 3)

if __name__ == "__main__":
    unittest.main()

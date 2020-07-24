import datetime

from log_parser import EventRule
from event_parser import EventGroupRule
from signals import *
from evaluators import *
from criteria import Criteria
from sifter_builder import SifterBuilder
from gsyslyzer_cli import Gsyslyzer

sifter_builder = SifterBuilder()

# Add the hotplug event to the builder
sifter_builder.add_event_rule(
    EventRule(
        tag="hotplug", 
        regular_expression="(.*)(queueing hotplug event for post rebuild processing:)"\
                           "\s*(subsystem:)\s*(\")(?P<subsystem>\w*)(\")\s*(action:)"\
                           "\s*(\")(?P<action>\w*)(\")\s*(device_link:)\s*(\")"\
                           "(?P<device_link>[a-zA-Z/:\-0-9\.]*)(\")\s*(devpath:)\s*"\
                           "(\")(?P<devpath>[a-zA-Z/:\-0-9\.]*)(\")"
        )
)

# Add the rescan start event to the bulder
sifter_builder.add_event_rule(
    EventRule(
        tag="start_rescan",
        regular_expression="(.*)(launching scheduled platform rebuild)(.*)"
    )
)

# Add the rescan finish event to the builder
sifter_builder.add_event_rule(
    EventRule(
        tag="finish_rescan", 
        regular_expression="(.*)(successfully reinitialized platform)(.*)"
    )
)

# Add platform rescan group to the builder
sifter_builder.add_group_rule(
    EventGroupRule(
        tag="platform_rescan",
        trigger_event_tags=["start_rescan", "finish_rescan"],
        context_event_tags=["hotplug"]
    )
)

# Add rescan loop mode criteria to the builder
sifter_builder.add_criteria(
    Criteria(
        symptom_tag="Rescan Loop Mode",
        signal=RepeatGroupSignal("platform_rescan_signal", "platform_rescan"),
        evaluator=LessThanEvaluator(datetime.timedelta(seconds=5)),
        action_msg="Please contact hardware maintainer."
    )
)

if __name__ == "__main__":
    Gsyslyzer(sifter_builder).run()
    

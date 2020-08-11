import datetime

import gsys_constants
import signals
import evaluators
import log_parser
import event_parser
import criteria
import sifter_builder
import gsyslyzer_cli

if __name__ == "__main__":
    log_sifter_builder = sifter_builder.SifterBuilder()

    # Add the hotplug event to the builder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="hotplug", 
            regular_expression="(.*)(queueing hotplug event for post rebuild processing:)"\
                               "\s*(subsystem:)\s*(\")(?P<subsystem>\w*)(\")\s*(action:)"\
                               "\s*(\")(?P<action>\w*)(\")\s*(device_link:)\s*(\")"\
                               "(?P<device_link>[a-zA-Z/:\-0-9\.]*)(\")\s*(devpath:)\s*"\
                               "(\")(?P<devpath>[a-zA-Z/:\-0-9\.]*)(\")"
            )
    )

    # Add the SIGTERM event to the builder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="sigterm",
            regular_expression="(.*)(SIGTERM)(.*)"
        )
    )

    # Add the SIGSEGV event to the builder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="sigsegv",
            regular_expression="(.*)(SIGSEGV)(.*)"
        )
    )

    # Add the rescan start event to the bulder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="start_rescan",
            regular_expression="(.*)(launching scheduled platform rebuild)(.*)"
        )
    )

    # Add the rescan finish event to the builder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="finish_rescan", 
            regular_expression="(.*)(successfully reinitialized platform)(.*)"
        )
    )   
    
    # Add gsysd version publishing
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="gsysd_version_published",
            regular_expression="(.*)(gsysd version:)(.*)"
        )
    )

    # Add Scaffolding server start-up event to builder
    log_sifter_builder.add_event_rule(
        log_parser.EventRule(
            tag="scaffolding_server_start",
            regular_expression="(.*)(Scaffolding server has started and is serving requests.)(.*)"
        )
    )

    # Add platform rescan group to the builder
    log_sifter_builder.add_group_rule(
        event_parser.EventGroupRule(
            tag="platform_rescan",
            trigger_event_tags=["start_rescan", "finish_rescan"],
            context_event_tags=["hotplug"]
        )
    )

    # Add SIGTERM group to the builder
    log_sifter_buidler.add_group_rule(
        event_parser.EventGroupRule(
            tag="sigterm",
            trigger_event_tags=["sigterm"],
            context_event_tags=[]
        )
    )

    # Add SIGSEGV group to the builder
    log_sifter_buidler.add_group_rule(
        event_parser.EventGroupRule(
            tag="sigsegv",
            trigger_event_tags=["sigsegv"],
            context_event_tags=[]
        )
    )

    # Add Scaffolding server startup group to builder
    log_sifter_builder.add_group_rule(
        event_parser.EventGroupRule(
            tag="gsys_startup",
            trigger_event_rules=["gsysd_version_published", "scaffolding_server_start"],
            context_event_rules=[]
        )
    )

    # Add rescan loop mode criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="Rescan Loop Mode",
            signal=signals.RepeatGroupSignal(
                tag="platform_rescan_signal", 
                group_tag="platform_rescan"
            ),
            evaluator=evaluators.LessThanEvaluator(
                threshold=gsys_constants.PLATFORM_RESCAN_LOOP_MODE_THRESHOLD
            ),
            action_msg="Please contact hardware maintainer."
        )
    )

    # Add Gsys startup criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="Gsys_slow_startup",
            signal=signals.IntervalEventSignal(
                tag="gsys_startup_signal", 
                group_tag="gsys_startup", 
                start_event_tag="gsysd_version_published", 
                end_event_tag="scaffolding_server_start"
            ),
            evaluator=evaluators.GreaterThanEvaluator(
                threshold=gsys_constants.GSYS_SLOW_STARTUP_THRESHOLD
            ),
            action_msg="Gsys is slow to start. CPU utilization/starvation should be investigated."
        )
    )

    # Add SIGTERM criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="SIGTERM",
            signal=signals.ExistenceGroupSignal(
                tag="sigterm_signal", 
                group_tag="sigterm"
            ),
            evaluator=evaluators.ExistenceEvaluator(),
            action_msg="Gsys has been killed by a third party.\n(Check taskd logs for details.)"
        )
    )

    # Add SIGSEGV criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="SIGSEGV",
            signal=signals.ExistenceGroupSignal(
                tag="sigsegv_signal", 
                group_tag="sigsegv"
            ),
            evaluator=evaluators.ExistenceEvaluator(),
            action_msg="Gsys has crashed. Please contact the Gsys team."
        )
    )


    gsyslyzer_cli.Gsyslyzer(log_sifter_builder).run()
    

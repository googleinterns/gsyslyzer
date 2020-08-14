import datetime

import gsys_constants
import signals
import evaluators
import event_rule
import event_group_rule
import log_parser
import event_parser
import criteria
import sifter_builder
import gsyslyzer_cli

if __name__ == "__main__":
    log_sifter_builder = sifter_builder.SifterBuilder()

    # Add the hotplug event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="hotplug", 
            regular_expression="(.*)(queueing hotplug event for post rebuild processing:)"\
                               "\s*(subsystem:)\s*(\")(?P<subsystem>\w*)(\")\s*(action:)"\
                               "\s*(\")(?P<action>\w*)(\")\s*(device_link:)\s*(\")"\
                               "(?P<device_link>[a-zA-Z/:\-0-9\.]*)(\")\s*(devpath:)\s*"\
                               "(\")(?P<devpath>[a-zA-Z/:\-0-9\.]*)(\")"
            )
    )

    # Add PCIE error event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="pcie_error",
            regular_expression="(.*)(Failed read of reg\s)(?P<reg>\d*)(\sfor device at\s)(?P<location>\d*\:\d*\:\d*\.\d*)"
        )
    )

    # Add SMBus error event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="smbus_error",
            regular_expression="(.*)(SMBus device\s)(?P<dev_num>\d*\-\d*)(:\s)"\
                               "(?P<failure_type>Read\d*|Write\d*|ReadBlock)"\
                               "(\sfailure:\s)(?P<msg>.*)"
        )
    )

    # Add the SIGTERM event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="sigterm",
            regular_expression="(.*)(SIGTERM)(.*)"
        )
    )

    # Add the SIGSEGV event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="sigsegv",
            regular_expression="(.*)(SIGSEGV)(.*)"
        )
    )

    # Add the rescan start event to the bulder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="start_rescan",
            regular_expression="(.*)(launching scheduled platform rebuild)(.*)"
        )
    )

    # Add the rescan finish event to the builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="finish_rescan", 
            regular_expression="(.*)(successfully reinitialized platform)(.*)"
        )
    )   
    
    # Add gsysd version publishing event to builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="gsysd_version_published",
            regular_expression="(.*)(gsysd version:)(.*)"
        )
    )

    # Add Gsys server start-up event to builder
    log_sifter_builder.add_event_rule(
        event_rule.EventRule(
            tag="gsys_server_start",
            regular_expression="(.*)(initializing gsys server)(.*)"
        )
    )

    # Add PCIE error group to the builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="pcie_error",
            trigger_event_tags=["pcie_error"],
            context_event_tags=[]
        )
    )

    # Add SMBus error group to the builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="smbus_error",
            trigger_event_tags=["smbus_error"],
            context_event_tags=[]
        )
    )

    # Add platform rescan group to the builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="platform_rescan",
            trigger_event_tags=["start_rescan", "finish_rescan"],
            context_event_tags=["hotplug"]
        )
    )

    # Add SIGTERM group to the builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="sigterm",
            trigger_event_tags=["sigterm"],
            context_event_tags=[]
        )
    )

    # Add SIGSEGV group to the builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="sigsegv",
            trigger_event_tags=["sigsegv"],
            context_event_tags=[]
        )
    )

    # Add Gsys server startup group to builder
    log_sifter_builder.add_group_rule(
        event_group_rule.EventGroupRule(
            tag="gsys_startup",
            trigger_event_tags=["gsysd_version_published", "gsys_server_start"],
            context_event_tags=[]
        )
    )

    # Add PCIE error criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="PCIE Error",
            signal=signals.ExistenceGroupSignal(
                tag="pcie_error_signal",
                group_tag="pcie_error"
            ),
            evaluator=evaluators.ExistenceEvaluator(),
            action_msg="Possible hardare issues exist. Please check the device."
        )
    )

    # Add SMBus error criteria to the builder
    log_sifter_builder.add_criteria(
        criteria.Criteria(
            symptom_tag="SMBus Error",
            signal=signals.ExistenceGroupSignal(
                tag="smbus_error_signal",
                group_tag="smbus_error"
            ),
            evaluator=evaluators.ExistenceEvaluator(),
            action_msg="Possible hardare issues exist. Please check the device."
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
            symptom_tag="Gsys Slow Startup",
            signal=signals.IntervalEventSignal(
                tag="gsys_startup_signal", 
                group_tag="gsys_startup", 
                start_event_tag="gsysd_version_published", 
                end_event_tag="gsys_server_start"
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
            action_msg="Gsys has been killed by a third party. (Check taskd logs for details.)"
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
    

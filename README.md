# __Gsyslyzer__
***
## What is it?
Gsyslyzer is an open source tool that will provide an expert system for analyzing Gsys error conditions from the output log and provide actionable feedback.
The system can be applied to any log output and is rule driven so that it can be applied to other projects.

__Note__: This is not an officially supported Google product

## Dependencies
***
NumPy >= 1.19.0

## How do I use this?
***
To Analyze a Gsys Log:
1. Install dependencies (See __Dependencies__)
2. Navigate to gsyslyzer/src
3. Execute "gsys_pipeline.py" with Python3 (>= 3.6) with the following flags

#### Log File
	--log_file_path <str>
> Relative path to the log file to be analyzed.

#### Output [optional]
	--json_output <True/False>
> Boolean designating if output should be directed to the terminal or to "gsyslyzer.json"
>
> (Default: False)

#### Verbosity [optional]
	--verbosity <int 0/1>
>__Note__: Only affects terminal output.
>
> Integer designating level of verbosity for output:
>
>    0: (Most Users) Symptom and Action summary
>
>    1: (Advanced Users) Details all Symptom Bursts and Actions
>
> (Default: 0)

#### Statistics [optional]
	--collect_statistics <True/False>
> Boolean designating if statistics about the occurences of different signals should be reported on
>
> (Default: False)


## How do I add a new symptom?
***
### The Basics

![Gsyslyzer Design Image](https://github.com/googleinterns/gsyslyzer/tree/master/design_image.png "Gsyslyzer Design")

#### Event Rules:
__tag__: string label

__regular_expression__: string regular expression

#### Event Group Rules:
__tag__: string label

__trigger_event_tags__: ordered list string event tags that define the group

__context_event_tags__: unordered list of event tags to be collected as context

#### Criteria:
__symptom_tag__: string label

__signal__: Signal object of what relationship to detect (see __Signals__)

__evalutor__: Evaluator object of how to compare a signal to a threshold (see __Evaluators__)

__action_msg__: string message to report to user if the symptom occurs

#### Signals
The following are the options for signals:
1. __IntervalGroupSignal__: Detects time between start_group_tag and end_group_tag
    
    __tag__: string label
    
    __start_group_tag__: string group tag 
    
    __end_group_tag__: string group tag

2. __RepeatGroupSignal__: Detects time between repeats of group_tag
    
    __tag__: string label
    
    __group_tag__: string group tag

3. __ExistenceGroupSignal__: Detects if group_tag exists
    
    __tag__: string label
    
    __group_tag__: string group tag

4. __IntervalEventSignal__: Detects time between start_event_tag and end_event_tag within group_tag
    
    __tag__: string label
    
    __group_tag__: string group tag
    
    __start_event_tag__: string event tag 
    
    __end_event_tag__: string event tag

#### Evaluators
The following are options for evaluators:
1. __GreaterThanEvaluator__: Evaluates if signal is greater than a threshold

    __threshold__: datetime.timedelta object

2. __GreaterThanEqualEvaluator__: Evaluates if signal is greater than or equal to a threshold

    __threshold__: datetime.timedelta object

3. __LessThanEvaluator__: Evaluates if signal is less than a threshold

    __threshold__: datetime.timedelta object

4. __LessThanEqualEvaluator__: Evaluates if signal is less than or equal to a threshold

    __threshold__: datetime.timedelta object

5. __ExistenceEvaluator__: Evaluates if signal exists


### An Example
To demonstrate how to define a new symptom let's walkthrough an example...

For this example, suppose we want to identify if our automatic pet feeding software is feeding the pets too often.

(Cats are notorious hackers after all...)

Let's pretend we have the following lines in our log:

***

06:30] Fed the cat

06:35] Fed the dog

06:50] Walked the dog

11:30] Played with the cat

12:30] Owner starts nap

12:31] Fed the cat

12:32] Fed the dog

12:33] Fed the cat

12:34] Fed the dog

12:35] Fed the cat

12:36] Fed the dog

12:40] Owner awakens from nap

***
1. __Event Rules:__ Finding important log events

    In our example we care about the lines that tell us "Fed the cat" and "Fed the dog"

    To capture these, in our pipeline file we will add two event rules with 

    1. 'tag's to label and identify them 
    2. 'regular_expressions' to find them.

```python
log_sifter_builder.add_event_rule(
    event_rule.EventRule(
        tag="fed_cat",
        regular_expression="(.*)(Fed the cat)(.*)"
    )
)
log_sifter_builder.add_event_rule(
    event_rule.EventRule(
        tag="fed_dog",
        regular_expression="(.*)(Fed the dog)(.*)"
    )
)
```

__Note__: Only lines that meet the "[IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg" format should be used

2. __Group Rules:__ Grouping related log events into log event groups

    Since we care about when both the pets get fed...

    It is necessary to define some grouping for when both the cat and the dog get fed.

    To capture this, we add a group rule to our pipeline file with:

    1. 'tag' to label and identify the group
    2. 'trigger_event_tags': a list of event tags that define our group

        (In our instance that will be "fed_cat" then "fed_dog")

    3. 'context_event_tags': a list of event tags that do not define if the group has occured...
        but they might be helpful to know if they occured along with the group

```python
log_sifter_builder.add_group_rule(
    event_group_rule.EventGroupRule(
        tag="pets_fed",
        trigger_event_tags=["cat_fed", "dog_fed"],
        context_event_tags=[] # In our specific example we do not need any context
    )
)
```
__Note__: trigger_event_tags enforce an order. This means that if you list [a, b, c], only occurences where those events occur in that order will meet this group rule. If event c happens before event a, they are not meant to be grouped together.

__Note__: context_event_tags do NOT enforce an order. However, only context events that occur BEFORE the start of the trigger events are considered to be relevant to a given group. This means that if you list [d, e, f], any occurences of any of those events will be grouped into only the immediately next occurence of the group.

3. __Criteria:__ Marking groups as Symptoms 
    Now all we need to do is set up a way to find out if a given "pets_fed" group is abnormal
    
    For our example, let's say that if the pets are fed within 30 minutes of being fed, its abnormal

    To do this we must setup criteria for what it means for a "pets_fed_too_often" symptom

    This criteria will consist of:

    1. 'symptom_tag' to label and identify our symptom
    2. 'signal' that defines what relationship we are interested in detecting
    3. 'evaluator' that defines a threshold for our signal
    4. 'action_msg' to report to the user of what to do if this occurs

```python
log_sifter_builder.add_criteria(
    criteria.Criteria(
        symptom_tag="pets_fed_too_often",
        # We go with the repeat group signal here to see how often the "pets_fed" group repeats
        signal=signals.RepeatGroupSignal( 
            tag="pets_fed_signal",
            group_tag="pets_fed" # Here we set what group tag the signal uses
        )
        # Here we say we care when the signal is LESS than some threshold
        evaluator=evaluators.LessThanEvaluator(
            # Here we set the threshold to be 30 minutes
            threshold=datetime.timedelta(minutes=30)
        ),
        action_msg="Change PetFeeder password... and keep a closer eye on that cat..."
    )
)
```

And that's it!

Now if we run the updated version of our pipeline file, it should detect when occurences of "Fed the cat" followed by "Fed the dog" occurs at an interval of less than 30 minutes.

If that is detected our user will be alerted to change their PetFeeder password and (of course) keep a closer eye on that cat.



## Can I analyze non-Gsys logs?

There is not out of the box implementation for this.

However, a new "<your project>_pipeline.py" file could be written to analyze different logs.

__Log Requirements:__
1. Lines to be analyzed must follow the "[IWEF]mmdd hh:mm:ss.uuuuuu threadid file:line] msg" format
2. A line with the format; "Log file created at: yyyy/mm/dd hh:mm:ss" must be included before any lines to be analyzed

__Pipeline Template:__

Your pipeline implementation should follow the following structure:

```python
log_sifter_builder = sifter_builder.SifterBuilder()

# Your Event Rules
...
# Your Group Rules
...
# Your Criteria
...

gsyslyzer_cli.Gsyslyzer(log_sifter_builder).run()
```




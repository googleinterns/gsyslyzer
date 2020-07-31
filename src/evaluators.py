""" Module for defining the different types of evalulators that can be
    applied to a list of signals. """

class Evaluator:
    """ Parent Evaluator that filters signals """
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate_value(self, value):
        return None

    def evaluate_signals(self, detected_signals):
        confirmed_signals = {}

        for detected_signal in detected_signals:
            value = detected_signal.interval
            if self.evaluate_value(value):
                confirmed_signals[detected_signal] = value

        return confirmed_signals
                
class GreaterThanEvaluator(Evaluator):
    """ Evaluator for checking when values exceed the threshold """
    def __init__(self, threshold):
        super(GreaterThanEvaluator, self).__init__(threshold)

    def evaluate_value(self, value):
        result = value > self.threshold
        return result

class GreaterThanEqualEvaluator(Evaluator):
    """ Evaluator for checking when values meet or exceed the threshold """
    def __init__(self, threshold):
        super(GreaterThanEqualEvaluator, self).__init__(threshold)

    def evaluate_value(self, value):
        result = value >= self.threshold
        return result

class LessThanEvaluator(Evaluator):
    """ Evaluator for checking when values drop below the threshold """
    def __init__(self, threshold):
        super(LessThanEvaluator, self).__init__(threshold)

    def evaluate_value(self, value):
        result = value < self.threshold
        return result

class LessThanEqualEvaluator(Evaluator):
    """ evaluator for checking when values to or below the threshold """
    def __init__(self, threshold):
        super(LessThanEqualEvaluator, self).__init__(threshold)

    def evaluate_value(self, value):
        result = value <= self.threshold
        return result

class ExistenceEvaluator(Evaluator):
    """ Trivial evalutor to mark the existence of signals """
    def __init__(self):
        pass

    def evaluate_value(self, value):
        return True




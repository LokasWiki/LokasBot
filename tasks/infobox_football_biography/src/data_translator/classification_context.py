class ClassificationContext:
    def __init__(self):
        self.strategies = []

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def classify(self, value):
        for strategy in self.strategies:
            result = strategy.classify(value)
            if result:
                return result
        return "unknown"

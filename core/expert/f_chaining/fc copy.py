
class Rule:
    def __init__(self, condition, result,jenis,rule):
        self.condition = condition  # List of conditions
        self.result = result  # Result of the rule
        self.jenis=jenis
        self.rule=rule

    def evaluate(self, facts):
        return all(facts.get(condition, False) for condition in self.condition)

class DiabetesExpert:
    def __init__(self):
        self.rules = []  # List of rules
        self.facts = {}  # Dictionary to store facts
        

    def add_rule(self, condition, result,jenis,rule):
        self.rules.append(Rule(condition, result,jenis,rule))

    def add_fact(self, fact, value):
        self.facts[fact] = value

# Create an instance of the expert system
expert = DiabetesExpert()
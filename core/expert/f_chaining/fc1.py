
class Rule:
    def __init__(self, condition, result):
        self.condition = condition  # List of conditions
        self.result = result  # Result of the rule

    def evaluate(self, facts):
        return all(facts.get(condition, False) for condition in self.condition)

class DiabetesExpert:
    def __init__(self):
        self.rules = []  # List of rules
        self.facts = {}  # Dictionary to store facts

    def add_rule(self, condition, result):
        self.rules.append(Rule(condition, result))

    def add_fact(self, fact, value):
        self.facts[fact] = value

    def infer(self):
        new_facts = True
        while new_facts:
            new_facts = False
            for rule in self.rules:
                if rule.evaluate(self.facts) and rule.result not in self.facts:
                    self.add_fact(rule.result, True)
                    new_facts = True
                    # If consumption of corticosteroids is true, stop the forward chaining
                    if rule.result == 'Diabetes' and rule.condition == ['Konsumsi kortikosteroid']:
                        return

    def diagnosis(self):
        self.infer()
        if self.facts.get('Diabetes', False):
            return "Kemungkinan Diabetes"
        elif self.facts.get('Prediabetes', False):
            return "Kemungkinan Prediabetes"
        else:
            return "Kemungkinan Negatif Diabetes"
# Create an instance of the expert system
expert = DiabetesExpert()
# Define rules and conditions
expert.add_rule(['Poliuri'], 'Diabetes')
expert.add_rule(['Polidipsi'], 'Diabetes')
expert.add_rule(['Polifagi'], 'Diabetes')
expert.add_rule(['Berat badan turun'], 'Diabetes')
expert.add_rule(['Konsumsi kortikosteroid'], 'Diabetes')
expert.add_rule(['Konsumsi dexamethasone'], 'Diabetes')
expert.add_rule(['Konsumsi methylprednisolon'], 'Diabetes')
expert.add_rule(['sering merokok'], 'Diabetes')
expert.add_rule(['obesitas'], 'Diabetes')
expert.add_rule(['perut buncit'], 'Diabetes')
expert.add_rule(['keluarga Diabetes'], 'Diabetes')
expert.add_rule(['Prediabetes_condition'], 'Prediabetes')  # Add a rule for Prediabetes

# Get input from the user
konsumsi_kortikosteroid = input("Apakah Anda mengonsumsi kortikosteroid? (True/False): ").lower() == 'true'
konsumsi_dexamethasone = input("Apakah Anda mengonsumsi dexamethasone? (True/False): ").lower() == 'true'
konsumsi_methylprednisolon = input("Apakah Anda mengonsumsi methylprednisolon? (True/False): ").lower() == 'true'
poliuri = input("Apakah Anda mengalami poliuri (sering buang air kecil)? (True/False): ").lower() == 'true'
polidipsi = input("Apakah Anda mengalami polidipsi (sering haus)? (True/False): ").lower() == 'true'
polifagi = input("Apakah Anda mengalami polifagi (sering lapar)? (True/False): ").lower() == 'true'
berat_badan_turun = input("Apakah berat badan Anda turun? (True/False): ").lower() == 'true'
sering_merokok = input("Apakah Anda Sering merokok ? (True/False): ").lower() == 'true'
obesitas = input("Apakah IBM anda Lebih dari 30 ? (True/False): ").lower() == 'true'
buncit = input("Apakah Anda mengalami perut Buncit? (True/False): ").lower() == 'true'
keluarga_diabetes = input("Apakah Anda memiliki keluarga dan kerabat yang terkena diabetes (True/False): ").lower() == 'true'

# Check specific conditions for immediate diagnosis
if konsumsi_kortikosteroid or konsumsi_dexamethasone or konsumsi_methylprednisolon:
    expert.add_fact('Diabetes', True)
elif poliuri and polidipsi and polifagi and berat_badan_turun:
    expert.add_fact('Diabetes', True)
elif sering_merokok or obesitas or buncit or keluarga_diabetes:
    expert.add_fact('Prediabetes', True)

# Get diagnosis based on forward chaining
diagnosis = expert.diagnosis()
print("Diagnosis:", diagnosis)

# Penanganan
if diagnosis == "Kemungkinan Diabetes":
    print("Anda berada dalam kondisi kemungkinan diabetes. Sebaiknya lakukan diet dan konsultasikan dengan dokter.")
elif diagnosis == "Kemungkinan Prediabetes":
    print("Anda berada dalam kondisi prediabetes. Sebaiknya konsultasikan dengan dokter.")
else:
    print("Anda tidak memiliki tanda-tanda diabetes atau prediabetes. Tetap jaga kesehatan")

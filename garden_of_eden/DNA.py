import copy
import random


class DNA:
    def __init__(self, name, d, δ, basis, rules):
        """make a new DNA with stem length d, angle δ,
        plant basis basis and rules rules.
        basis is a string, and rules is a list of tuples (from, to, proba)
        turning from into to with proba proba"""
        self.name = name
        self.d = d
        self.δ = δ
        self.basis = basis
        self.rules = rules
        self.alphabet = set(basis)
        for a, b, _ in rules:
            self.alphabet |= set(a)
            self.alphabet |= set(b)

    def cross(self, other_dna):
        """returns a new DNA which is the cross of this DNA and the other_dna"""
        dna1 = self.copy()
        dna2 = other_dna.copy()
        name = "{} x {}".format(dna1.name, dna2.name)
        d = random.choice([dna1.d, dna2.d])
        δ = random.choice([dna1.δ, dna2.δ])
        basis = random.choice([dna1.basis, dna2.basis])

        rules = []
        if len(dna1.rules) < len(dna2.rules):
            short_rules = dna1.rules
            long_rules = dna2.rules
        else:
            short_rules = dna2.rules
            long_rules = dna1.rules

        for rule1, rule2 in zip(short_rules, long_rules):
            # with high proba, we just pick one of the two rules,
            # with low proba, it's a funny mix of the two
            if random.random() < .8:
                rules.append(random.choice([rule1, rule2]))
            else:
                a = random.choice([rule1[0], rule2[0]])
                b = ""
                for c1, c2 in zip(rule1[1], rule2[1]):
                    b += random.choice([c1, c2])
                proba = random.choice([rule1[2], rule2[2]])
                rules.append((a, b, proba))

        for i in range(len(short_rules), len(long_rules)):
            rules.append(long_rules[i])

        return DNA(name, d, δ, basis, rules)

    def random_mutation(self):
        i_gene = random.randrange(0, len(self.rules))
        i_letter = random.randrange(0, len(self.rules[i_gene][1]))
        new_rule = self.rules[i_gene][1][:i_letter]
        new_rule += random.choice(list(self.alphabet))
        new_rule += self.rules[i_gene][1][i_letter+1:]
        self.rules[i_gene] = self.rules[i_gene][0], new_rule, self.rules[i_gene][2]

    def copy(self):
        return copy.deepcopy(self)
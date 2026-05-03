import random

class Genome:
    def __init__(self, species, speed, vision, max_age,  size, energy=100, age=0):
        self.species = species
        self.speed = speed
        self.vision = vision
        self.max_age = max_age
        self.size = size
        self.age = age
        self.energy = energy

    @staticmethod
    def child_factor(father_factor, mother_factor):
        mean = (father_factor + mother_factor) / 2
        variation=0.25
        if random.random() < 0.1:
            # 10% chance of big mutation
            return max(0, random.gauss(mean, variation * 3))
        return max(0, random.gauss(mean, variation))

    def can_reproduce(self, partner:'Genome'):
        """Checks if reproduction is possible (energy + age)."""
        # Ensure both parents have enough energy and are mature
        if self.energy < 20 or partner.energy < 20:
            return False
        if self.age <  self.max_age*0.25 or partner.age < partner.max_age*0.25:
            return False
        return True

    def reproduce(self, partner:'Genome'):
        """Produces a child Genome if species are compatible and conditions met."""
        if not self.can_reproduce(partner):
            return None
        child = Genome(
            species=self.species,
            speed=self.child_factor(self.speed, partner.speed),
            vision=self.child_factor(self.vision, partner.vision),
            max_age=self.child_factor(self.max_age, partner.max_age),
            size=self.child_factor(self.size, partner.size),
        )
        # Reduce parent energy after reproduction
        self.energy -= 10
        partner.energy -= 10
        self.age += 1
        partner.age += 1
        return child
    def __str__(self):
        varss=vars(self)
        text=f"genome for\n"
        for v in varss:
            text+=f'{v}-->{varss[v]}\n'
        return text

# quick test
if __name__ == '__main__':
    g1 = Genome('shark', speed=5, vision=10, max_age=20,  size=50,age=10)
    g2 = Genome('shark', speed=6, vision=9, max_age=18, size=55,age=5)
    child = g1.reproduce(g2)
    print(str(child))

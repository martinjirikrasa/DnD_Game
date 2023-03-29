from abstract_classes import Creature
import random

class Hero(Creature):
    object_type = "hero"

    def __init__(self, identifier, name, position, base_attack, base_ac, damage):
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.name = name
        self.max_hp = 20
        self.hp = 20
        self.max_stamina = 20
        self.stamina = 20
        self.xp = 0
        self.level = 1
        self.gold = 0

    def rest(self):
        self.hp = self.max_hp
        self.stamina = self.max_stamina

    def level_up(self):
        self.level += 1
        self.max_hp += 5

class Goblin(Creature):
    object_type = "monster"

    def __str__(self):
        return "Goblin"

    def __init__(self, identifier, position, base_attack, base_ac, damage):
        super().__init__(identifier, position, base_attack, base_ac, damage)
        self.hp = random.randint(1, 5)
        self.xp = 10
        self.gold = random.randint(1, 6)

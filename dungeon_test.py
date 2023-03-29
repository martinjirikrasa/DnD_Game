from abstract_classes import AbstractDungeon
from copy import deepcopy
from map_entities import Hero, Goblin, Creature
import random
import json
import datetime

class Dungeon(AbstractDungeon):
    def __init__(self, size: tuple, hero_name: str):
        super().__init__(size)
        self.width, self.height = size
        self.hero = Hero("@", hero_name, [1, 1], 5, 5, 1)
        self.starting_entities = ["goblin"] * 5
        self.entities = []
        self.empty_space = []
        self.message = ""
        self.create_dungeon()

    def __str__(self):
        printable_map = ""
        for row in self.current_map:
            for column in row:
                printable_map += column
            printable_map += "\n"
        return printable_map

    def create_dungeon(self, max_tunnel_length=9, min_num_tunnels=40):
        # Initialize the dungeon map
        for x in range(self.size[0]):
            self.dungeon_map.append([])
            for y in range(self.size[1]):
                self.dungeon_map[x].append("▓")
        
        # Initialize the starting position
        x, y = 1, 1
        self.dungeon_map[x][y] = "."
        
        
        # Generate the tunnels
        num_created_tunnels = 0
        while num_created_tunnels < min_num_tunnels:
            direction = random.choice(["up", "down", "left", "right"])
            tunnel_length = random.randint(1, max_tunnel_length)
            # 1,1 is not empty_spce
            if direction == "left" and x == 1 and y == 1:
                direction = "down"
            elif direction == "up" and x == 1 and y == 1:
                direction = "righ"


            if direction == "up":
                for j in range(tunnel_length):
                    if x > 1:
                        x -= 1
                        self.dungeon_map[x][y] = "."
                        self.empty_space.append((x, y))
                num_created_tunnels += 1
            elif direction == "down":
                for j in range(tunnel_length):
                    if x < self.size[0] - 2:
                        x += 1
                        self.dungeon_map[x][y] = "."
                        self.empty_space.append((x, y))
                num_created_tunnels += 1
            elif direction == "left":
                for j in range(tunnel_length):
                    if y > 1:
                        y -= 1
                        self.dungeon_map[x][y] = "."
                        self.empty_space.append((x, y))
                num_created_tunnels += 1
            elif direction == "right":
                for j in range(tunnel_length):
                    if y < self.size[1] - 2:
                        y += 1
                        self.dungeon_map[x][y] = "."
                        self.empty_space.append((x, y))
                num_created_tunnels += 1
        
        self.place_entities(self.starting_entities)
        self.current_map = deepcopy(self.dungeon_map)
        self.empty_space = list(map(list,set(self.empty_space)))
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier
    ## saving the game
    def save(self):
        data = {
            "hero_name": self.hero.name,
            "hero_position": self.hero.position,
            "hero_hp": self.hero.hp,
            #"hero_max_stamina": self.hero.max_stamina,
            "hero_stamina": self.hero.stamina,
            "hero_xp": self.hero.xp,
            "hero_level": self.hero.level,
            "hero_gold": self.hero.gold,
            "dungeon_map": self.current_map,
            "entities": [entity.__dict__ if isinstance(entity, Creature) else entity for entity in self.entities],
            "empty_space": self.empty_space,
            "message": self.message
        }
        
        file_name = f"{self.hero.name}_{datetime.datetime.now():%Y-%m-%d-%H}.dng"
        with open(file_name, 'w') as f:
            json.dump(data, f)
 
    ## loading the game
    
    @classmethod
    def load(cls, file):
        with open(file, "r") as f:
            data = json.load(f)

        # Create a new instance of the class
        dungeon = cls.__new__(cls)

        # Set the attributes using the loaded data
        dungeon.hero = Hero(
            "@",
            data['hero_name'],
            data['hero_position'],
            data['hero_level'],
            data['hero_hp'],
            data['hero_stamina']
        )
        dungeon.dungeon_map = data['dungeon_map']
        # dungeon.entities = data['entities']
        dungeon.empty_space = data['empty_space']
        dungeon.message = data['message']
        dungeon.current_map = deepcopy(dungeon.dungeon_map)

        # create creature instances for entities that are still dictiorearies
        dungeon.entities = []
        for entity_data in data['entities']:
            entity_type = entity_data.get('type')
            entity_position = entity_data.get('position')
            if entity_type == 'monster':
                dungeon.entities.append(Goblin(entity_data.get('identifier'), entity_position, entity_data.get('base_attack'), entity_data.get('base_ac'), entity_data.get('damage')))
        

        #replace the old hero position with an empty space
        old_position = tuple(dungeon.hero.position)
        dungeon.dungeon_map[old_position[0]][old_position[1]] = "."
        dungeon.current_map[old_position[0]][old_position[1]] = "."
        # Return the new instance
        return dungeon
    def hero_action(self, action):
        #right
        if action == "R":
            # if self.hero.position[1] + 1 < self.size[1] - 1:
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] + 1] != "▓":
                self.hero.position[1] += 1
        #left
        elif action == "L":
            if self.dungeon_map[self.hero.position[0]][self.hero.position[1] - 1] != "▓":
                self.hero.position[1] -= 1
        #up
        elif action == "U":
            if self.dungeon_map[self.hero.position[0] - 1][self.hero.position[1]] != "▓":
                self.hero.position[0] -= 1
        #down
        elif action == "D":
            if self.dungeon_map[self.hero.position[0] + 1][self.hero.position[1]] != "▓":
                self.hero.position[0] += 1
        #attack
        elif action == "A":
            fighting = False
            for entity in self.entities:
                if tuple(self.hero.position) == entity.position:
                    if hasattr(entity, "attack"):
                        self.fight(entity)
                        fighting = True
                        break
            if not fighting:
                self.message ="Your big sword is hitting air really hard!"
        ## save the game
        self.save()
        ##
        self.update_map(self.entities)

        if self.hero.hp < 1:
            self.message += "\nTHIS IS THE END"

    def place_entities(self, entities: list):
        print(self.empty_space)
        position = random.sample(self.empty_space, len(entities))
        for idx, entity in enumerate(self.starting_entities):
            if entity == "goblin":
                self.entities.append(Goblin(identifier="\033[38;5;1mg\033[0;0m",
                                            position=position[idx], base_attack=-1,
                                            base_ac=0, damage=1))
        for entity in self.entities:
            self.dungeon_map[entity.position[0]][entity.position[1]] = entity.map_identifier

    def update_map(self, entities: list):
        # TODO implement entities
        self.current_map = deepcopy(self.dungeon_map)
        self.current_map[self.hero.position[0]][self.hero.position[1]] = self.hero.map_identifier
        

    def fight(self, monster):
        hero_roll = self.hero.attack()
        monster_roll = monster.attack()
        if hero_roll["attack_roll"] > monster.base_ac:
            monster.hp -= hero_roll["inflicted_damage"]
            if monster.hp > 0:
                self.message = f"Hero inflicted {hero_roll['inflicted_damage']}"
            else:
                self.message = f"Hero Hero inflicted {hero_roll['inflicted_damage']} damage and slain {monster}"
                ## implemented user gaining up to 3 hp after killing a monster
                current_hero_hp = self.hero.hp
                self.hero.hp += random.choice([0, 1, 2, 3])
                if self.hero.hp > current_hero_hp:
                    self.message = f"Hero found a healing package and healed {self.hero.hp - current_hero_hp} hp."
                ###
                self.hero.gold += monster.gold
                self.hero.xp += 1
                self.dungeon_map[monster.position[0]][monster.position[1]] = "."
                self.entities.remove(monster)
        if monster_roll["attack_roll"] > self.hero.base_ac:
            self.message += f"\nMonster inflicted {monster_roll['inflicted_damage']} damage"
            self.hero.hp -= monster_roll['inflicted_damage']
            if self.hero.hp < 1:
                self.message += f"\n{self.hero.name} have been slained by {monster}"
        self.message += f"\nHero HP: {self.hero.hp}  Monster HP: {monster.hp}"

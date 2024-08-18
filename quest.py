import random

# Character Class
class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 10
        self.inventory = []
        self.experience = 0
        self.completed_quests = []

    def attack(self, enemy):
        damage = random.randint(1, self.attack_power)
        enemy.hp -= damage
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")

    def heal(self):
        if "Health Potion" in self.inventory:
            self.hp = self.max_hp
            self.inventory.remove("Health Potion")
            print(f"{self.name} used a Health Potion and restored to full health!")
        else:
            print(f"{self.name} has no Health Potions left!")

    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.attack_power += 5
        self.hp = self.max_hp
        print(f"{self.name} leveled up! Now at level {self.level}, HP: {self.hp}, Attack: {self.attack_power}")

    def gain_experience(self, points):
        self.experience += points
        if self.experience >= self.level * 100:
            self.experience -= self.level * 100
            self.level_up()

    def show_status(self):
        print(f"{self.name} (Level {self.level} {self.character_class}) - HP: {self.hp}/{self.max_hp} - Attack Power: {self.attack_power}")
        print("Inventory:", self.inventory)
        print(f"Experience: {self.experience}")
        print("Completed Quests:", self.completed_quests)

    def add_quest(self, quest):
        self.completed_quests.append(quest)

# Enemy Class
class Enemy:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.hp = level * 20
        self.attack_power = level * 5

    def attack(self, player):
        damage = random.randint(1, self.attack_power)
        player.hp -= damage
        print(f"{self.name} attacks {player.name} for {damage} damage!")

    def show_status(self):
        print(f"{self.name} (Level {self.level}) - HP: {self.hp}")

# Quest Class
class Quest:
    def __init__(self, description, reward_exp, reward_item):
        self.description = description
        self.reward_exp = reward_exp
        self.reward_item = reward_item
        self.is_completed = False

    def complete(self, player):
        if not self.is_completed:
            print(f"Quest Completed: {self.description}")
            player.gain_experience(self.reward_exp)
            if self.reward_item:
                player.inventory.append(self.reward_item)
                print(f"You have received: {self.reward_item}")
            player.add_quest(self.description)
            self.is_completed = True
        else:
            print("Quest already completed!")

# Special Items
class SpecialItem:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

    def use(self, player):
        if self.name in player.inventory:
            self.effect(player)
            player.inventory.remove(self.name)
        else:
            print(f"{player.name} does not have a {self.name}!")

def use_sword(player):
    player.attack_power += 10
    print(f"{player.name} equipped a Sword, increasing attack power!")

def use_mana_potion(player):
    print(f"{player.name} used a Mana Potion!")

sword = SpecialItem("Sword", use_sword)
mana_potion = SpecialItem("Mana Potion", use_mana_potion)

# Updated Explore Function with Special Items
def explore(player):
    print(f"\n{player.name} ventures into the unknown...")
    event = random.choice(["enemy", "item", "nothing", "quest"])

    if event == "enemy":
        enemy = Enemy(random.choice(["Goblin", "Troll", "Orc", "Dragon"]), player.level)
        battle_result = battle(player, enemy)
        if not battle_result:
            return False
    elif event == "item":
        item = random.choice(["Health Potion", "Mana Potion", "Sword"])
        player.inventory.append(item)
        print(f"{player.name} found a {item}!")
        if item == "Sword":
            sword.use(player)
        elif item == "Mana Potion":
            mana_potion.use(player)
    elif event == "nothing":
        print("Nothing interesting happened...")
    elif event == "quest":
        quests = [
            Quest("Find the lost ring", 100, "Ring of Power"),
            Quest("Defeat the bandit leader", 150, "Bandit's Amulet"),
            Quest("Rescue the villager", 200, "Villager's Gratitude")
        ]
        quest = random.choice(quests)
        quest.complete(player)

    return True

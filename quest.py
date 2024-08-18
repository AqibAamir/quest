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

# Extended Battle Function with Special Attacks
def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    while player.hp > 0 and enemy.hp > 0:
        print("\n-- Battle Menu --")
        print("1. Attack")
        print("2. Heal")
        print("3. Use Special Item")
        print("4. Run")

        choice = input("Choose an action: ")

        if choice == "1":
            player.attack(enemy)
            if enemy.hp > 0:
                enemy.attack(player)
        elif choice == "2":
            player.heal()
            enemy.attack(player)
        elif choice == "3":
            if "Sword" in player.inventory:
                sword.use(player)
            if "Mana Potion" in player.inventory:
                mana_potion.use(player)
            enemy.attack(player)
        elif choice == "4":
            print("You fled from the battle!")
            break
        else:
            print("Invalid choice!")

        player.show_status()
        enemy.show_status()

    if player.hp <= 0:
        print("You were defeated...")
        return False
    elif enemy.hp <= 0:
        print(f"{player.name} defeated the {enemy.name}!")
        player.gain_experience(50)
        return True

def create_character():
    name = input("Enter your character's name: ")
    character_class = input("Choose your class (Warrior/Mage/Rogue): ")
    return Character(name, character_class)

def game_loop():
    print("Welcome to the RPG Game!")
    player = create_character()

    while True:
        print("\n-- Main Menu --")
        print("1. Explore")
        print("2. Show Status")
        print("3. Quit Game")

        choice = input("Choose an action: ")

        if choice == "1":
            if not explore(player):
                print("Game Over!")
                break
        elif choice == "2":
            player.show_status()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# Extended Character Classes for Different Roles
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, "Warrior")
        self.hp += 30
        self.max_hp += 30
        self.attack_power += 5

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, "Mage")
        self.hp -= 20
        self.max_hp -= 20
        self.attack_power += 10
        self.mana = 100

def cast_spell(self, enemy):
        if self.mana >= 20:
            spell_damage = random.randint(15, 30)
            enemy.hp -= spell_damage
            self.mana -= 20
            print(f"{self.name} casts a spell on {enemy.name} for {spell_damage} damage!")
        else:
            print(f"{self.name} does not have enough mana to cast a spell!")

class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, "Rogue")
        self.attack_power += 10
        self.stealth = True

    def sneak_attack(self, enemy):
        if self.stealth:
            sneak_damage = random.randint(20, 40)
            enemy.hp -= sneak_damage
            print(f"{self.name} performs a sneak attack on {enemy.name} for {sneak_damage} damage!")
        else:
            print(f"{self.name} is not in stealth mode!")

# Additional Special Items
class Armor(SpecialItem):
    def __init__(self, name, defense_boost):
        super().__init__(name, None)
        self.defense_boost = defense_boost

    def use(self, player):
        if self.name in player.inventory:
            player.max_hp += self.defense_boost
            player.hp = min(player.hp + self.defense_boost, player.max_hp)
            print(f"{player.name} equipped {self.name}, increasing max HP by {self.defense_boost}!")
            player.inventory.remove(self.name)
        else:
            print(f"{player.name} does not have {self.name}!")

# Define some special items
armor = Armor("Steel Armor", 50)
magic_staff = SpecialItem("Magic Staff", lambda player: print(f"{player.name} wields a Magic Staff!"))

# Extended Inventory System
def show_inventory(player):
    print("\nInventory Details:")
    for item in player.inventory:
        if item == "Health Potion":
            print(f"Item: Health Potion - Restores full HP.")
        elif item == "Mana Potion":
            print(f"Item: Mana Potion - Restores 50 Mana.")
        elif item == "Sword":
            print(f"Item: Sword - Increases attack power by 10.")
        elif item == "Steel Armor":
            print(f"Item: Steel Armor - Increases max HP by 50.")
        elif item == "Magic Staff":
            print(f"Item: Magic Staff - Boosts magical attack power.")
        else:
            print(f"Item: {item} - Unknown item.")
    print("\n")

def use_item(player):
    if player.inventory:
        print("Available items to use:")
        show_inventory(player)
        item = input("Enter the name of the item to use: ").strip()
        for special_item in [sword, mana_potion, armor, magic_staff]:
            if item == special_item.name:
                special_item.use(player)
                return
        print(f"{player.name} does not have {item} or cannot use it!")

def complete_quest(player):
    quests = [
        Quest("Find the lost ring", 100, "Ring of Power"),
        Quest("Defeat the bandit leader", 150, "Bandit's Amulet"),
        Quest("Rescue the villager", 200, "Villager's Gratitude"),
        Quest("Retrieve the ancient scroll", 250, "Ancient Scroll"),
        Quest("Slay the dragon", 300, "Dragon's Tooth")
    ]
    quest = random.choice(quests)
    if quest.description not in player.completed_quests:
        quest.complete(player)
    else:
        print("You have already completed this quest.")

    # Additional Combat Options
def enhanced_battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    while player.hp > 0 and enemy.hp > 0:
        print("\n-- Battle Menu --")
        print("1. Attack")
        print("2. Heal")
        print("3. Use Special Item")
        print("4. Use Magic (Mage Only)")
        print("5. Sneak Attack (Rogue Only)")
        print("6. Run")

        choice = input("Choose an action: ")

        if choice == "1":
            player.attack(enemy)
            if enemy.hp > 0:
                enemy.attack(player)
        elif choice == "2":
            player.heal()
            enemy.attack(player)
        elif choice == "3":
            use_item(player)
            enemy.attack(player)
        elif choice == "4" and isinstance(player, Mage):
            player.cast_spell(enemy)
        elif choice == "5" and isinstance(player, Rogue):
            player.sneak_attack(enemy)
        elif choice == "6":
            print("You fled from the battle!")
            break
        else:
            print("Invalid choice!")

        player.show_status()
        enemy.show_status()

    if player.hp <= 0:
        print("You were defeated...")
        return False
    elif enemy.hp <= 0:
        print(f"{player.name} defeated the {enemy.name}!")
        player.gain_experience(50)
        return True
    
    # Crafting System
class CraftingRecipe:
    def __init__(self, name, required_items, result_item):
        self.name = name
        self.required_items = required_items
        self.result_item = result_item

    def craft(self, player):
        if all(item in player.inventory for item in self.required_items):
            for item in self.required_items:
                player.inventory.remove(item)
            player.inventory.append(self.result_item)
            print(f"{player.name} crafted {self.result_item} using {', '.join(self.required_items)}!")
        else:
            print(f"{player.name} does not have all the required items to craft {self.result_item}.")

# Define crafting recipes
health_potion_recipe = CraftingRecipe("Health Potion", ["Herb", "Water"], "Health Potion")
mana_potion_recipe = CraftingRecipe("Mana Potion", ["Magic Herb", "Water"], "Mana Potion")
sword_recipe = CraftingRecipe("Sword", ["Iron Ore", "Wood"], "Sword")

def show_crafting_recipes():
    print("\n-- Crafting Recipes --")
    print("1. Health Potion: Requires Herb, Water")
    print("2. Mana Potion: Requires Magic Herb, Water")
    print("3. Sword: Requires Iron Ore, Wood")

def craft_item(player):
    show_crafting_recipes()
    choice = input("Choose a recipe to craft (1/2/3): ")

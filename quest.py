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
        self.gold = 100  # Start with 100 gold

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
        print(f"{self.name} (Level {self.level} {self.character_class}) - HP: {self.hp}/{self.max_hp} - Attack Power: {self.attack_power} - Gold: {self.gold}")
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
    def __init__(self, description, reward_exp, reward_item, reward_gold=0):
        self.description = description
        self.reward_exp = reward_exp
        self.reward_item = reward_item
        self.reward_gold = reward_gold
        self.is_completed = False

    def complete(self, player):
        if not self.is_completed:
            print(f"Quest Completed: {self.description}")
            player.gain_experience(self.reward_exp)
            if self.reward_item:
                player.inventory.append(self.reward_item)
                print(f"You have received: {self.reward_item}")
            if self.reward_gold:
                player.gold += self.reward_gold
                print(f"You have received: {self.reward_gold} gold")
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

armor = Armor("Steel Armor", 50)
magic_staff = SpecialItem("Magic Staff", lambda player: print(f"{player.name} wields a Magic Staff!"))

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

    if choice == "1":
        health_potion_recipe.craft(player)
    elif choice == "2":
        mana_potion_recipe.craft(player)
    elif choice == "3":
        sword_recipe.craft(player)
    else:
        print("Invalid choice!")

# Trading System
class Merchant:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

    def show_inventory(self):
        print(f"\n-- {self.name}'s Inventory --")
        for item, price in self.inventory.items():
            print(f"{item}: {price} gold")

    def buy(self, player, item):
        if item in self.inventory and player.gold >= self.inventory[item]:
            player.inventory.append(item)
            player.gold -= self.inventory[item]
            print(f"{player.name} bought {item} for {self.inventory[item]} gold!")
        else:
            print("Transaction failed. Either you don't have enough gold or the item is unavailable.")

    def sell(self, player, item):
        if item in player.inventory:
            sell_price = self.inventory.get(item, 10) // 2
            player.inventory.remove(item)
            player.gold += sell_price
            print(f"{player.name} sold {item} for {sell_price} gold!")
        else:
            print(f"{player.name} does not have {item} to sell.")

blacksmith = Merchant("Blacksmith", {"Sword": 50, "Armor": 100, "Health Potion": 20, "Mana Potion": 30})

def trade_with_merchant(player):
    while True:
        print("\n-- Trading Menu --")
        print("1. Buy")
        print("2. Sell")
        print("3. Exit Trading")

        choice = input("Choose an action: ")

        if choice == "1":
            blacksmith.show_inventory()
            item = input("Enter the item you want to buy: ").strip()
            blacksmith.buy(player, item)
        elif choice == "2":
            item = input("Enter the item you want to sell: ").strip()
            blacksmith.sell(player, item)
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

# Example Usage:
# Create a character
hero = Character("Aragon", "Warrior")

# Show character status
hero.show_status()

# Example quest
quest1 = Quest("Defeat the Goblin King", 100, "Sword", 50)
quest1.complete(hero)

# Battle with an enemy
enemy1 = Enemy("Goblin", 2)
hero.attack(enemy1)
enemy1.show_status()

# Use special items
use_item(hero)

# Crafting
craft_item(hero)

# Trading with a merchant
trade_with_merchant(hero)

# Show final status
hero.show_status()



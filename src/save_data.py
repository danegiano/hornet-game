import json
import os

HP_COST = 50
MAX_HP_UPGRADES = 8

class SaveData:
    def __init__(self, path="save_data.json"):
        self.path = path
        self.coins = 0
        self.hp_upgrades = 0
        self.max_island_unlocked = 0
        self.powers = []
        self.completed_levels = {}

        if os.path.exists(self.path):
            self.load()

    def save(self):
        data = {
            "coins": self.coins,
            "hp_upgrades": self.hp_upgrades,
            "max_island_unlocked": self.max_island_unlocked,
            "powers": self.powers,
            "completed_levels": self.completed_levels,
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        self.coins = data.get("coins", 0)
        self.hp_upgrades = data.get("hp_upgrades", 0)
        self.max_island_unlocked = data.get("max_island_unlocked", 0)
        self.powers = data.get("powers", [])
        self.completed_levels = data.get("completed_levels", {})

    def add_coins(self, amount):
        self.coins += amount

    def buy_hp(self):
        if self.hp_upgrades >= MAX_HP_UPGRADES:
            return False
        if self.coins < HP_COST:
            return False
        self.coins -= HP_COST
        self.hp_upgrades += 1
        return True

    def get_max_hp(self):
        from src.settings import PLAYER_MAX_HP
        return PLAYER_MAX_HP + self.hp_upgrades

    def complete_level(self, island_index, level_index):
        key = str(island_index)
        if key not in self.completed_levels:
            self.completed_levels[key] = []
        if level_index not in self.completed_levels[key]:
            self.completed_levels[key].append(level_index)

    def unlock_power(self, power_name):
        if power_name not in self.powers:
            self.powers.append(power_name)

    def has_power(self, power_name):
        return power_name in self.powers

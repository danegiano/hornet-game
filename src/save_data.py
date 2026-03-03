import json
import os

HP_COST = 50
MAX_HP_UPGRADES = 8

class SaveData:
    def __init__(self, path="save_data.json"):
        self.path = path
        self.coins = 0
        self.hp_upgrades = 0
        self.totems = 0
        self.max_island_unlocked = 0
        self.powers = []
        self.circus_unlocked = False
        self.hallucination_unlocked = False
        self.hallucination_island = 0
        self.shadow_powers = []
        self.hallucination_lives = 0  # stock of lives for Hallucination Land
        self.completed_levels = {}

        if os.path.exists(self.path):
            self.load()

    def save(self):
        data = {
            "coins": self.coins,
            "hp_upgrades": self.hp_upgrades,
            "totems": self.totems,
            "max_island_unlocked": self.max_island_unlocked,
            "powers": self.powers,
            "circus_unlocked": self.circus_unlocked,
            "hallucination_unlocked": self.hallucination_unlocked,
            "hallucination_island": self.hallucination_island,
            "shadow_powers": self.shadow_powers,
            "hallucination_lives": self.hallucination_lives,
            "completed_levels": self.completed_levels,
        }
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        self.coins = data.get("coins", 0)
        self.hp_upgrades = data.get("hp_upgrades", 0)
        self.totems = data.get("totems", 0)
        self.max_island_unlocked = data.get("max_island_unlocked", 0)
        self.powers = data.get("powers", [])
        self.circus_unlocked = data.get("circus_unlocked", False)
        self.hallucination_unlocked = data.get("hallucination_unlocked", False)
        self.hallucination_island = data.get("hallucination_island", 0)
        self.shadow_powers = data.get("shadow_powers", [])
        self.hallucination_lives = data.get("hallucination_lives", 0)
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

    def buy_totems(self):
        if self.coins < 500:
            return False
        self.coins -= 500
        self.totems += 3
        return True

    def use_totem(self):
        if self.totems <= 0:
            return False
        self.totems -= 1
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

    def unlock_circus(self):
        if not self.circus_unlocked:
            self.circus_unlocked = True
            self.save()

    def unlock_hallucination(self):
        if not self.hallucination_unlocked:
            self.hallucination_unlocked = True
            self.save()

    def has_shadow_power(self, power_name):
        return power_name in self.shadow_powers

    def unlock_shadow_power(self, power_name):
        if power_name not in self.shadow_powers:
            self.shadow_powers.append(power_name)

    def buy_hallucination_lives(self, amount, cost):
        """Buy up to 10 lives for Hallucination Land."""
        if self.hallucination_lives >= 10:
            return False
        if self.coins < cost:
            return False
        to_buy = min(amount, 10 - self.hallucination_lives)
        self.coins -= cost * to_buy
        self.hallucination_lives += to_buy
        return True

    def use_hallucination_life(self):
        if self.hallucination_lives <= 0:
            return False
        self.hallucination_lives -= 1
        return True

import os
import json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.save_data import SaveData

def test_default_save():
    """New save has correct defaults."""
    save = SaveData(path="/tmp/test_hornet_save.json")
    assert save.coins == 0
    assert save.hp_upgrades == 0
    assert save.max_island_unlocked == 0
    assert save.powers == []
    assert save.completed_levels == {}

def test_save_and_load():
    """Can save and load data."""
    path = "/tmp/test_hornet_save2.json"
    if os.path.exists(path):
        os.remove(path)
    save = SaveData(path=path)
    save.coins = 42
    save.hp_upgrades = 3
    save.powers = ["double_jump", "dash"]
    save.max_island_unlocked = 2
    save.completed_levels = {"0": [0, 1, 2], "1": [0]}
    save.save()

    loaded = SaveData(path=path)
    loaded.load()
    assert loaded.coins == 42
    assert loaded.hp_upgrades == 3
    assert loaded.powers == ["double_jump", "dash"]
    assert loaded.max_island_unlocked == 2
    assert loaded.completed_levels == {"0": [0, 1, 2], "1": [0]}

    os.remove(path)

def test_add_coins():
    save = SaveData(path="/tmp/test_hornet_save3.json")
    save.add_coins(10)
    assert save.coins == 10
    save.add_coins(5)
    assert save.coins == 15

def test_buy_hp():
    save = SaveData(path="/tmp/test_hornet_save4.json")
    save.coins = 100
    assert save.buy_hp() == True
    assert save.coins == 50
    assert save.hp_upgrades == 1
    assert save.buy_hp() == True
    assert save.coins == 0
    assert save.hp_upgrades == 2
    assert save.buy_hp() == False  # not enough coins
    assert save.hp_upgrades == 2

def test_buy_hp_max_limit():
    save = SaveData(path="/tmp/test_hornet_save5.json")
    save.coins = 1000
    save.hp_upgrades = 8
    assert save.buy_hp() == False
    assert save.coins == 1000

def test_complete_level():
    save = SaveData(path="/tmp/test_hornet_save6.json")
    save.complete_level(0, 0)
    save.complete_level(0, 1)
    save.complete_level(0, 0)  # duplicate should not add again
    assert save.completed_levels == {"0": [0, 1]}

def test_powers():
    save = SaveData(path="/tmp/test_hornet_save7.json")
    assert save.has_power("double_jump") == False
    save.unlock_power("double_jump")
    assert save.has_power("double_jump") == True
    save.unlock_power("double_jump")  # duplicate
    assert save.powers == ["double_jump"]

if __name__ == "__main__":
    test_default_save()
    test_save_and_load()
    test_add_coins()
    test_buy_hp()
    test_buy_hp_max_limit()
    test_complete_level()
    test_powers()
    print("All save_data tests passed!")

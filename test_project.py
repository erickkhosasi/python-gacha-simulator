import project
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def reset_state():
    project.game_state["crystals"] = 1600
    project.game_state["standard_pull"] = 0
    project.game_state["featured_pull"] = 0
    project.char_collection.clear()
    project.equip_collection.clear()

# === Test helper function ===
def test_get_rarity():
    # Test 5-star pity
    pity = {"4-star": 0, "5-star": 89}
    assert project.get_rarity(pity) == 5


def test_update_collection():
    collection = {}
    pull = {"name": "Amber", "rarity": 4, "element": "Pyro", "weapon": "Bow"}
    # Update new character
    project.update_collection(collection, pull)
    assert collection["Amber"]["count"] == 1
    # Update duplicate character
    project.update_collection(collection, pull)
    assert collection["Amber"]["count"] == 2


def test_update_pity():
    pity = {"4-star": 8, "5-star": 89}
    project.update_pity(5, pity)
    assert pity["5-star"] == 0
    assert pity["4-star"] == 9
    project.update_pity(4, pity)
    assert pity["5-star"] == 1
    assert pity["4-star"] == 0
    pity = {
        "4-star": 8, "5-star": 89,
        "featured_4_star": 0, "featured_5_star": 0
    }
    project.update_pity(5, pity, banner="featured")
    assert pity["5-star"] == 0
    assert pity["4-star"] == 9
    assert pity["featured_5_star"] == 1
    project.update_pity(5, pity, banner="featured", from_featured_pool=True)
    assert pity["5-star"] == 0
    assert pity["4-star"] == 10
    assert pity["featured_5_star"] == 0


def test_validate_crystals():
    project.game_state["crystals"] = 1600
    assert project.validate_crystals(10) == True
    assert project.game_state["crystals"] == 0
    assert project.validate_crystals(10) == False
    assert project.game_state["crystals"] == 0


# === Test core functions ===
def test_pull_char():
    pool = [
        {"name": "Barbara", "gender": "F", "height": "Medium", "weapon": "Catalyst", "element": "Hydro", "rarity": 4},
        {"name": "Venti", "gender": "M", "height": "Medium", "weapon": "Bow", "element": "Anemo", "rarity": 5}
    ]
    assert project.pull_char(4, pool) == "★★★★ - Hydro - Catalyst - Barbara"
    assert project.char_collection["Barbara"]["count"] == 1
    assert project.pull_char(5, pool) == "★★★★★ - Anemo - Bow - Venti"
    assert project.char_collection["Venti"]["count"] == 1


def test_pull_equip():
    pool = [
        {"name": "Messenger", "type": "Bow", "rarity": 3},
        {"name": "Blackcliff Warbow", "type": "Bow", "rarity": 4},
        {"name": "Skyward Atlas", "type": "Catalyst", "rarity": 5}
    ]
    assert project.pull_equip(3, pool) == "★★★ - Bow - Messenger"
    assert project.equip_collection["Messenger"]["count"] == 1
    assert project.pull_equip(4, pool) == "★★★★ - Bow - Blackcliff Warbow"
    assert project.equip_collection["Blackcliff Warbow"]["count"] == 1
    assert project.pull_equip(5, pool) == "★★★★★ - Catalyst - Skyward Atlas"
    assert project.equip_collection["Skyward Atlas"]["count"] == 1


@patch("project.random.choices")
def test_standard_wish(mock_choices):
    # Force rarity to be 3
    mock_choices.side_effect = [[3], [project.STD_EQUIPMENT_POOL[0]]]
    result = project.standard_wish(1)
    assert "★" in result
    assert len(project.equip_collection) == 1
    assert next(iter(project.equip_collection.values()))["rarity"] == 3

    # Force rarity to be 5, and character
    mock_choices.side_effect = [
        [5],
        ["char"],
        [project.STD_CHARACTER_POOL[0]]
    ]
    result = project.standard_wish(1)
    assert "★" in result
    assert len(project.char_collection) == 1
    assert next(iter(project.char_collection.values()))["rarity"] == 5


def test_featured_wish():
    # Set featured pity so next pull will be 5 star featured character
    project.game_state["featured_pity"] = {
        "4-star": 8,
        "5-star": 89,
        "featured_4_star": 1,
        "featured_5_star": 1
    }
    result = project.featured_wish(1)
    assert "★" in result
    assert len(project.char_collection) == 1
    pulled = next(iter(project.char_collection.values()))
    assert pulled["rarity"] == 5
    assert pulled["name"] == "Venti"
    assert project.game_state["featured_pity"]["featured_5_star"] == 0
    assert project.game_state["featured_pity"]["featured_4_star"] == 1
    assert project.game_state["featured_pity"]["5-star"] == 0
    assert project.game_state["featured_pity"]["4-star"] == 9


def test_wish():
    project.wish("standard", 1)
    assert project.game_state["crystals"] == 1440
    assert project.game_state["standard_pull"] == 1
    project.wish("featured", 1)
    assert project.game_state["crystals"] == 1280
    assert project.game_state["featured_pull"] == 1
    assert project.wish("standard", 10) == "Insufficient crystals. Please top up.\n"
    assert project.wish("featured", 10) == "Insufficient crystals. Please top up.\n"


def test_characters():
    assert project.characters() == "You do not have any character"
    project.char_collection["Amber"] = {
        "name": "Amber",
        "rarity": 4,
        "element": "Pyro",
        "weapon": "Bow",
        "count": 1
    }
    project.char_collection["Lisa"] = {
        "name": "Lisa",
        "rarity": 4,
        "element": "Electro",
        "weapon": "Catalyst",
        "count": 2
    }
    output = project.characters()
    assert "★" in output
    assert "Amber" in output
    assert "Lisa" in output
    assert "x1" in output
    assert "x2" in output
    assert output.index("Electro") < output.index("Pyro") # Electro is alphabetically before Pyro


def test_equipment():
    assert project.equipment() == "You do not have any equipment"
    project.equip_collection["Skyrider Sword"] = {
        "name": "Skyrider Sword",
        "rarity": 3,
        "type": "Sword",
        "count": 2
    }
    project.equip_collection["Favonius Lance"] = {
        "name": "Favonius Lance",
        "rarity": 4,
        "type": "Polearm",
        "count": 3
    }
    output = project.equipment()
    assert "★" in output
    assert "Skyrider Sword" in output
    assert "Favonius Lance" in output
    assert "x2" in output
    assert "x3" in output
    assert output.index("Favonius Lance") < output.index("Skyrider Sword")


def test_topup():
    project.game_state["crystals"] = 0
    with patch("builtins.input", side_effect=["1"]):
        assert project.topup() == "Current crystals: 60"
        assert project.game_state["crystals"] == 60
        assert project.game_state["money_spent"] == 16500

    with patch("builtins.input", side_effect=["0", "8", "2"]):
        assert project.topup() == "Current crystals: 360"
        assert project.game_state["crystals"] == 360
        assert project.game_state["money_spent"] == 97500

    with patch("builtins.input", side_effect=["7"]):
        assert project.topup() == None
        assert project.game_state["crystals"] == 360
        assert project.game_state["money_spent"] == 97500


def test_wish_menu(capsys):
    # Test standard wish
    with patch("builtins.input", side_effect=["1", "3"]):
        project.wish_menu("standard")
    captured = capsys.readouterr()
    assert "★" in captured.out
    assert project.game_state["standard_pull"] == 1

    # Test featured wish
    project.game_state["crystals"] = 1600
    with patch("builtins.input", side_effect=["2", "0", "3"]):
        project.wish_menu("featured")
    captured = capsys.readouterr()
    assert "Invalid selection" in captured.out
    assert "★" in captured.out
    assert project.game_state["featured_pull"] == 10

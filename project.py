# === Imports ===
import random

# === Global constants and data ===
game_state = {
    "money_spent": 0,
    "crystals": 0,
    "standard_pity": {
        "4-star": 0,
        "5-star": 0
    },
    "featured_pity": {
        "4-star": 0,
        "5-star": 0,
        "featured_4_star": 0,
        "featured_5_star": 0
    },
    "standard_pull": 0,
    "featured_pull": 0
}
topup_package = {
    "1": {"crystals": 60, "price": 16500},
    "2": {"crystals": 300, "price": 81000},
    "3": {"crystals": 980, "price": 255000},
    "4": {"crystals": 1980, "price": 489000},
    "5": {"crystals": 3280, "price": 815000},
    "6": {"crystals": 6480, "price": 1629000}
}
char_collection = {}
equip_collection = {}

# === Main Loop ===
def main():
    while True:
        print(f"""
Welcome to Genshin Impact wish simulator!
Crystals: {game_state['crystals']:,}
Money Spent: Rp {game_state['money_spent']:,}
Total standard banner pull: {game_state['standard_pull']}
Total featured banner pull: {game_state['featured_pull']}

    Menu:
    1. Top Up Crystals
    2. Standard Banner Wish
    3. Featured Banner Wish
    4. Characters
    5. Equipment
    6. Exit
        """)

        choice = input("Select menu: ").strip()
        print()
        match choice:
            case "1":
                topup()
            case "2":
                wish_menu("standard")
            case "3":
                wish_menu("featured")
            case "4":
                print(characters())
            case "5":
                print(equipment())
            case "6":
                print(f"""Thanks for playing! Here's your total pull and every characters & equipment that you have collected so far:
Total standard banner pull: {game_state['standard_pull']}
Total featured banner pull: {game_state['featured_pull']}
Total money spent: Rp {game_state['money_spent']:,}
                """)
                print(characters())
                print(equipment())
                break
            case _:
                print("Invalid selection. Please select between 1 - 6")

# === Helper functions ===
def get_rarity(pity):
    if pity["5-star"] >= 89:
        return 5
    elif pity["4-star"] >= 9:
        return random.choices([4, 5], weights=[99.4, 0.6])[0]
    else:
        return random.choices([3, 4, 5], weights=[94.3, 5.1, 0.6])[0]


def update_collection(collection, pull):
    name = pull["name"]
    if name in collection:
        collection[name]["count"] += 1
    else:
        pull_copy = pull.copy()
        pull_copy["count"] = 1
        collection[name] = pull_copy


def update_pity(rarity, pity, banner=None, from_featured_pool=False):
    if rarity == 5:
        pity["5-star"] = 0
        pity["4-star"] += 1
        if banner == "featured" and not from_featured_pool:
            pity["featured_5_star"] = 1
        elif banner == "featured" and from_featured_pool:
            pity["featured_5_star"] = 0
    elif rarity == 4:
        pity["4-star"] = 0
        pity["5-star"] += 1
        if banner == "featured" and not from_featured_pool:
            pity["featured_4_star"] = 1
        elif banner == "featured" and from_featured_pool:
            pity["featured_4_star"] = 0
    else:
        pity["4-star"] += 1
        pity["5-star"] += 1


def validate_crystals(times):
    cost = 160 * times
    if game_state["crystals"] < cost:
        return False
    else:
        game_state["crystals"] -= cost
        return True

# === Core functions ===
def pull_char(rarity, pool):
    filtered_pool = [item for item in pool if item["rarity"] == rarity]
    pull = random.choices(filtered_pool)[0]
    update_collection(char_collection, pull)
    return f"{"★" * pull["rarity"]} - {pull['element']} - {pull['weapon']} - {pull['name']}"


def pull_equip(rarity, equip_pool):
    pool = [item for item in equip_pool if item["rarity"] == rarity]
    pull = random.choices(pool)[0]
    update_collection(equip_collection, pull)
    return f"{"★" * pull["rarity"]} - {pull['type']} - {pull['name']}"


def standard_wish(times):
    pity = game_state["standard_pity"]
    results = []

    for _ in range(times):
        rarity = get_rarity(pity)

        if rarity == 3:
            results.append(pull_equip(rarity, STD_EQUIPMENT_POOL))
        else:
            type_choice = random.choices(["char", "equip"])[0]
            if type_choice == "char":
                results.append(pull_char(rarity, STD_CHARACTER_POOL))
            else:
                results.append(pull_equip(rarity, STD_EQUIPMENT_POOL))

        update_pity(rarity, pity)

    return "\n".join(results) + "\n"


def featured_wish(times):
    pity = game_state["featured_pity"]
    results = []

    for _ in range(times):
        from_featured = False
        rarity = get_rarity(pity)

        if rarity == 3:
            results.append(pull_equip(rarity, STD_EQUIPMENT_POOL))

        elif rarity in [4, 5]:
            key = f"featured_{rarity}_star"
            if pity[key]:
                results.append(pull_char(rarity, FTR_CHARACTER_POOL))
                from_featured = True
            else:
                type_choice = random.choices(["char", "equip"])[0]
                if type_choice == "char":
                    rng_pool = random.choices([STD_CHARACTER_POOL, FTR_CHARACTER_POOL])[0]
                    results.append(pull_char(rarity, rng_pool))
                    from_featured = rng_pool is FTR_CHARACTER_POOL
                else:
                    results.append(pull_equip(rarity, STD_EQUIPMENT_POOL))

        update_pity(rarity, pity, banner="featured", from_featured_pool=from_featured)

    return "\n".join(results) + "\n"


def wish(banner, times):
    if not validate_crystals(times):
        return "Insufficient crystals. Please top up.\n"
    if banner == "standard":
        game_state["standard_pull"] += times
        return standard_wish(times)
    elif banner == "featured":
        game_state["featured_pull"] += times
        return featured_wish(times)

# === UI/Display ===
def characters():
    if not char_collection:
        return "You do not have any character"
    output = ["\nYour Characters:"]
    sorted_chars = sorted(char_collection.values(), key=lambda x: (-x["rarity"], x["element"], x["name"]))
    for char in sorted_chars:
        output.append(f"{"★" * char['rarity']} - {char['element']} - {char['weapon']} - {char['name']} - x{char['count']}")
    return "\n".join(output)


def equipment():
    if not equip_collection:
        return "You do not have any equipment"
    output = ["\nYour Equipment:"]
    sorted_equip = sorted(equip_collection.values(), key=lambda x: (-x["rarity"], x["type"], x["name"]))
    for equip in sorted_equip:
        output.append(f"{"★" * equip['rarity']} - {equip['type']} - {equip['name']} - x{equip['count']}")
    return "\n".join(output)


def topup():
    while True:
        print("""    1. Genesis Crystals x60 [Rp 16,500]
    2. Genesis Crystals x300 [Rp 81,000]
    3. Genesis Crystals x980 [Rp 255,000]
    4. Genesis Crystals x1980 [Rp 489,000]
    5. Genesis Crystals x3280 [Rp 815,000]
    6. Genesis Crystals x6480 [Rp 1,629,000]
    7. Main Menu
        """)

        choice = input("Choose topup package: ").strip()
        print()
        if choice in topup_package:
            option = topup_package[choice]
            game_state["crystals"] += option["crystals"]
            game_state["money_spent"] += option["price"]
            print(f"Top up successful!.\nTotal money spent: Rp {game_state['money_spent']:,}")
            return f"Current crystals: {game_state['crystals']:,}"
        elif choice == "7":
            return
        else:
            print("Invalid topup selection. Please select between 1 - 7")


def wish_menu(banner):
    while True:
        print("""    1. 1x Wish
    2. 10x Wishes
    3. Main Menu
        """)
        choice = input("Select: ").strip()
        print()
        match choice:
            case "1":
                print(wish(banner, 1))
            case "2":
                print(wish(banner, 10))
            case "3":
                return
            case _:
                print("Invalid selection. Please select between 1 - 2")

# === POOLS ===
FTR_CHARACTER_POOL = [
    {"name": "Venti", "gender": "M", "height": "Medium", "weapon": "Bow", "element": "Anemo", "rarity": 5},
    {"name": "Barbara", "gender": "F", "height": "Medium", "weapon": "Catalyst", "element": "Hydro", "rarity": 4},
    {"name": "Xiangling", "gender": "F", "height": "Medium", "weapon": "Polearm", "element": "Pyro", "rarity": 4},
    {"name": "Fischl", "gender": "F", "height": "Medium", "weapon": "Bow", "element": "Electro", "rarity": 4}
]

STD_CHARACTER_POOL = [
    # === 5-Star Characters ===
    {"name": "Jean", "gender": "F", "height": "Tall", "weapon": "Sword", "element": "Anemo", "rarity": 5},
    {"name": "Diluc", "gender": "M", "height": "Tall", "weapon": "Claymore", "element": "Pyro", "rarity": 5},
    {"name": "Keqing", "gender": "F", "height": "Medium", "weapon": "Sword", "element": "Electro", "rarity": 5},
    {"name": "Mona", "gender": "F", "height": "Medium", "weapon": "Catalyst", "element": "Hydro", "rarity": 5},
    {"name": "Qiqi", "gender": "F", "height": "Short", "weapon": "Sword", "element": "Cryo", "rarity": 5},
    # === 4-Star Characters ===
    {"name": "Amber", "gender": "F", "height": "Medium", "weapon": "Bow", "element": "Pyro", "rarity": 4},
    {"name": "Kaeya", "gender": "M", "height": "Tall", "weapon": "Sword", "element": "Cryo", "rarity": 4},
    {"name": "Lisa", "gender": "F", "height": "Tall", "weapon": "Catalyst", "element": "Electro", "rarity": 4},
    {"name": "Barbara", "gender": "F", "height": "Medium", "weapon": "Catalyst", "element": "Hydro", "rarity": 4},
    {"name": "Noelle", "gender": "F", "height": "Medium", "weapon": "Claymore", "element": "Geo", "rarity": 4},
    {"name": "Bennet", "gender": "M", "height": "Medium", "weapon": "Sword", "element": "Pyro", "rarity": 4},
    {"name": "Razor", "gender": "M", "height": "Medium", "weapon": "Claymore", "element": "Electro", "rarity": 4},
    {"name": "Beidou", "gender": "F", "height": "Tall", "weapon": "Claymore", "element": "Electro", "rarity": 4},
    {"name": "Fischl", "gender": "F", "height": "Medium", "weapon": "Bow", "element": "Electro", "rarity": 4},
    {"name": "Xiangling", "gender": "F", "height": "Medium", "weapon": "Polearm", "element": "Pyro", "rarity": 4},
    {"name": "Xingqiu", "gender": "M", "height": "Medium", "weapon": "Sword", "element": "Hydro", "rarity": 4},
    {"name": "Chongyun", "gender": "M", "height": "Medium", "weapon": "Claymore", "element": "Cryo", "rarity": 4},
    {"name": "Ningguang", "gender": "F", "height": "Tall", "weapon": "Catalyst", "element": "Geo", "rarity": 4}
]

STD_EQUIPMENT_POOL = [
    # === 3-Star Weapons ===
    {"name": "Messenger", "type": "Bow", "rarity": 3},
    {"name": "Raven Bow", "type": "Bow", "rarity": 3},
    {"name": "Recurve Bow", "type": "Bow", "rarity": 3},
    {"name": "Sharpshooter's Oath", "type": "Bow", "rarity": 3},
    {"name": "Slingshot", "type": "Bow", "rarity": 3},
    {"name": "Cool Steel", "type": "Sword", "rarity": 3},
    {"name": "Dark Iron Sword", "type": "Sword", "rarity": 3},
    {"name": "Fillet Blade", "type": "Sword", "rarity": 3},
    {"name": "Harbinger of Dawn", "type": "Sword", "rarity": 3},
    {"name": "Skyrider Sword", "type": "Sword", "rarity": 3},
    {"name": "Traveler's Handy Sword", "type": "Sword", "rarity": 3},
    {"name": "Black Tassel", "type": "Polearm", "rarity": 3},
    {"name": "Halberd", "type": "Polearm", "rarity": 3},
    {"name": "White Tassel", "type": "Polearm", "rarity": 3},
    {"name": "Bloodtainted Greatsword", "type": "Claymore", "rarity": 3},
    {"name": "Debate Club", "type": "Claymore", "rarity": 3},
    {"name": "Ferrous Shadow", "type": "Claymore", "rarity": 3},
    {"name": "Skyrider Greatsword", "type": "Claymore", "rarity": 3},
    {"name": "White Iron Greatsword", "type": "Claymore", "rarity": 3},
    {"name": "Emerald Orb", "type": "Catalyst", "rarity": 3},
    {"name": "Magic Guide", "type": "Catalyst", "rarity": 3},
    {"name": "Otherworldly Story", "type": "Catalyst", "rarity": 3},
    {"name": "Thrilling Tales of Dragon Slayers", "type": "Catalyst", "rarity": 3},
    {"name": "Twin Nephrite", "type": "Catalyst", "rarity": 3},

    # === 4-Star Weapons ===
    {"name": "Blackcliff Warbow", "type": "Bow", "rarity": 4},
    {"name": "Compound Bow", "type": "Bow", "rarity": 4},
    {"name": "Favonius Warbow", "type": "Bow", "rarity": 4},
    {"name": "Prototype Crescent", "type": "Bow", "rarity": 4},
    {"name": "Royal Bow", "type": "Bow", "rarity": 4},
    {"name": "Rust", "type": "Bow", "rarity": 4},
    {"name": "Sacrificial Bow", "type": "Bow", "rarity": 4},
    {"name": "The Stringless", "type": "Bow", "rarity": 4},
    {"name": "The Viridescent Hunt", "type": "Bow", "rarity": 4},
    {"name": "Blackcliff Longsword", "type": "Sword", "rarity": 4},
    {"name": "Favonius Sword", "type": "Sword", "rarity": 4},
    {"name": "Iron Sting", "type": "Sword", "rarity": 4},
    {"name": "Lion's Roar", "type": "Sword", "rarity": 4},
    {"name": "Prototype Rancour", "type": "Sword", "rarity": 4},
    {"name": "Royal Longsword", "type": "Sword", "rarity": 4},
    {"name": "Sacrificial Sword", "type": "Sword", "rarity": 4},
    {"name": "Sword of Descension", "type": "Sword", "rarity": 4},
    {"name": "The Black Sword", "type": "Sword", "rarity": 4},
    {"name": "The Flute", "type": "Sword", "rarity": 4},
    {"name": "Blackcliff Pole", "type": "Polearm", "rarity": 4},
    {"name": "Crescent Pike", "type": "Polearm", "rarity": 4},
    {"name": "Deathmatch", "type": "Polearm", "rarity": 4},
    {"name": "Dragon's Bane", "type": "Polearm", "rarity": 4},
    {"name": "Favonius Lance", "type": "Polearm", "rarity": 4},
    {"name": "Prototype Starglitter", "type": "Polearm", "rarity": 4},
    {"name": "Blackcliff Slasher", "type": "Claymore", "rarity": 4},
    {"name": "Favonius Greatsword", "type": "Claymore", "rarity": 4},
    {"name": "Prototype Archaic", "type": "Claymore", "rarity": 4},
    {"name": "Rainslasher", "type": "Claymore", "rarity": 4},
    {"name": "Royal Greatsword", "type": "Claymore", "rarity": 4},
    {"name": "Sacrificial Greatsword", "type": "Claymore", "rarity": 4},
    {"name": "Serpent Spine", "type": "Claymore", "rarity": 4},
    {"name": "The Bell", "type": "Claymore", "rarity": 4},
    {"name": "Whiteblind", "type": "Claymore", "rarity": 4},
    {"name": "Blackcliff Agate", "type": "Catalyst", "rarity": 4},
    {"name": "Eye of Perception", "type": "Catalyst", "rarity": 4},
    {"name": "Favonius Codex", "type": "Catalyst", "rarity": 4},
    {"name": "Mappa Mare", "type": "Catalyst", "rarity": 4},
    {"name": "Prototype Amber", "type": "Catalyst", "rarity": 4},
    {"name": "Royal Grimoire", "type": "Catalyst", "rarity": 4},
    {"name": "Sacrificial Fragments", "type": "Catalyst", "rarity": 4},
    {"name": "Solar Pearl", "type": "Catalyst", "rarity": 4},
    {"name": "The Widsith", "type": "Catalyst", "rarity": 4},

    # === 5-Star Weapons ===
    {"name": "Amos' Bow", "type": "Bow", "rarity": 5},
    {"name": "Skyward Harp", "type": "Bow", "rarity": 5},
    {"name": "Aquila Favonia", "type": "Sword", "rarity": 5},
    {"name": "Skyward Blade", "type": "Sword", "rarity": 5},
    {"name": "Primordial Jade Winged-Spear", "type": "Polearm", "rarity": 5},
    {"name": "Skyward Spine", "type": "Polearm", "rarity": 5},
    {"name": "Skyward Pride", "type": "Claymore", "rarity": 5},
    {"name": "Wolf's Gravestone", "type": "Claymore", "rarity": 5},
    {"name": "Lost Prayer to the Sacred Winds", "type": "Catalyst", "rarity": 5},
    {"name": "Skyward Atlas", "type": "Catalyst", "rarity": 5}
]


if __name__ == "__main__":
    main()

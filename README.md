# GENSHIN IMPACT WISH SIMULATOR
#### Video Demo: https://youtu.be/Te-6qSf_8GY
#### Description:

This project is a console-based simulation of the *Genshin Impact* gacha system, written in Python for CS50's Introduction to Programming with Python final project. It mimics the game's currency top-up system, gacha wishing with standard and featured banners, pity mechanics, characters and equipment collection, and duplicate tracking.

The goal of this project is to simulate the thrill of collecting your favorite characters and equipment through gacha, while simultaneously tracking your total spending on currency top-ups. This project was written in a functional programming paradigm and reinforces programming concepts such as dictionaries, loops, conditionals, randomness, input/output handling, and unit-testing for each functions. The structure is modular and testable, offering a clear example of applying Python fundamentals to build an interactive, stateful program.

---

## File Descriptions

- `project.py`: This is the main Python script that contains all the logic and functionality of the Genshin Impact Wish Simulator. The script is organized into several logical sections:
    1. Global State and Constants
        - `game_state`: A dictionary that stores the current number of crystals, money spent, pity counters, and total wish/pulls.
        - `topup_package`: A dictionary mapping top-up options to their corresponding crystal (in-game currency) amount and price
        - `char_collection` & `equip_collection`: Dictionaries used to track all characters and equipment the user has pulled, including duplicate counts.
        - `FTR_CHARACTER_POOL`: A list of dictionaries that stores the characters available to be pulled during a featured banner wish.
        - `STD_CHARACTER_POOL`: A list of dictionaries that stores the characters available to be pulled during any banner wish.
        - `STD_EQUIPMENT_POOL`: A list of dictionaries that stores the equipment available to be pulled during any banner wish.
    2. Main Loop
        - `main()`: The entry point of the program. It presents the main menu, handle user input, and navigate the menu to the appropriate functions. It also exits the program and display a final summary of the user's collection and total pulls. Includes input validation and loops until the user choose to exit the simulator.
    3. Helper Functions
        - `get_rarity(pity)`: Determines the rarity of a pull (3, 4, or 5-star), affected by the pity counter.
        - `update_collection(collection, pull)`: Adds a new character or equipment from a pull to the user's collection or increments the count if it's a duplicate.
        - `update_pity(rarity, pity, banner=None, from_featured_pool=False)`: Resets or increments the pity counters depending on the user's pull result.
        - `validate_crystals(times)`: Checks if the user has enough crystals for the requested number of wishes and deducts them if possible.
    4. Core Functions
        - `pull_char(rarity, pool)`: Randomly selects a character from the specified pool and adds it to the collection.
        - `pull_equip(rarity, equip_pool)`: Randomly selects an equipment from the specified pool and adds it to the collection.
        - `standard_wish(times)`: Executes 1 or 10 (depending on the user's choice) wishes from the standard banner, applying the pity system and RNG to determine the result.
        - `featured_wish(times)`: Executes 1 or 10 wishes from the featured banner, applying pity system and RNG unique to the featured banner.
        - `wish(banner, times)`: Navigates the user's wish to the appropriate function based on banner type and validates crystals.
    5. UI/Display Functions
        - `characters()`: Displays the list of characters in the user's collection, sorted by rarity, element, and name.
        - `equipment()`: Displays the list of equipment in the user's collection, sorted by rarity, weapon type, and name.
        - `topup()`: Presents the user with the option to top up their crystals by selecting from a list of packages. Includes input validation and a main-menu return option.
        - `wish_menu(banner)`: Presents the user with the option to do 1x or 10x wishes on a selected banner. Includes input validation and a main-menu return option.

## Design Decisions and Considerations

The core goal of the simulator was to balance accuracy to Genshin Impact's actual system with simplicity, code clarity and modularity. For example, the pity system replicates the game's hard-pity mechanics, ensuring a 5-star pull at the 90th attempt and a 4-star pull at the 10th. The featured banner includes the 50/50 pity mechanic for pulling featured characters.

To avoid repeated code, I create several helper functions like `update_collection()` to handle updates to the collection dictionaries and reduce redundant `if/else` blocks.

Testing was written using `pytest`, with coverage for all major functions including helper functions, core functions, and UI/display functions. `unittest.mock.patch` is used to handle user input in several functions that require it

All menu options are designed to loop until valid input is received. The rarity of characters and equipment is represented using multiple `★` symbols to make it easier for users to quickly identify high-rarity pull.

## Improvement Opportunities

This project was both a fun challenge and an exercise in applying multiple CS50P concepts in one cohesive program. I learned how to design scalable functions, organize program state, and write modular and defensive code that is both testable and maintainable.

If I had more time, I would add features like:
- Wish history logs
- Featured banner for equipment
- Visual effects for 4-star and 5-star pulls
- A soft pity system where the 5-star chance gradually increases after a certain number of attempts

Overall, this project was a rewarding opportunity to apply everything I've learned throughout CS50P in a creative and engaging way.

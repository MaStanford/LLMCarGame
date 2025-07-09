# Project: Car

## Summary

This project is a terminal-based, open-world, automotive RPG survival game. Players select a starting vehicle and embark on an adventure in an infinitely-generated, random world. The map features roads connecting cities, surrounded by various types of wilderness.

### Key Gameplay Elements:
- **Infinite World:** A randomly generated world provides endless exploration.
- **Cities:** Procedurally generated with buildings like gas stations, mechanic shops, weapon shops, and a city hall for quests. Cities are populated with random NPCs.
- **Wilderness:** The areas between cities are filled with randomly generated fauna (e.g., deer, dogs) and enemies (e.g., bandits, other hostile vehicles).
- **Vehicles:** A diverse roster of cars is available, including sports cars, sedans, vans, trucks, monster trucks, motorcycles, hot rods, and SUVs. Each vehicle has unique stats for:
    -   **Durability:** How much damage it can sustain.
    -   **Speed & Acceleration:** Top speed and how quickly it reaches it.
    -   **Handling:** Turning radius and braking power.
    -   **Fuel:** Max capacity and efficiency.
    -   **Size:** The character grid size of the vehicle (e.g., a motorcycle might be 2x3, a van 12x14).
    -   **Attachment Points:** Number and type of slots for weapons or modules.
- **Customization:** Cars have attachment points for weapons, extra fuel tanks, or storage.
- **Combat & Progression:** Players gain experience and loot (money, damaged parts, ammo) by defeating enemies.
- **Resource Management:**
    -   **Durability:** Damage accumulates from combat and collisions, repaired at mechanic shops.
    -   **Fuel:** Consumed while driving, refilled at gas stations.
    -   **Ammo:** Required for weapons, purchased at weapon shops.

## Stack

- **Language:** Python
- **Engine:** Custom-built terminal game engine using the `curses` library.
- **Renderer:** `curses` library for all screen drawing.

## Architecture

The game is built around a central game loop in `car/game.py`. This loop handles user input, updates the game state, and renders the world.

- **Game Loop & UI:**
    -   **Main Game Loop:** The core loop in `main_game` function within `car/game.py` renders the world, including the environment, roads, buildings, and all entities. It also handles user input and updates the game state.
    -   **UI Menus:** The game features several UI menus, each in its own file in the `car/ui` directory.
        -   **Main Menu:** `car/ui/main_menu.py` - The initial screen with "New Game," "Load Game," and "Quit" options.
        -   **New Game Menu:** `car/ui/new_game.py` - Allows the player to select their car, color, difficulty, and initial weapon.
        -   **Load Game Menu:** `car/ui/load_game.py` - Displays a list of saved games to load.
        -   **Inventory Menu (Tab):** `car/ui/inventory.py` - Pressing `Tab` opens a full-screen modal with a border.
            -   **Car Preview:** Displays the player's car, rotating through 8 directions.
            -   **Attachments:** A container lists attachment points, their type, and the equipped item. Arrow keys are used to navigate and select different weapons/items from inventory.
            -   **Inventory:** A container for stored items. Selecting an item opens a pop-up with actions (e.g., "Drop").
            -   **Stats:** A container shows current fuel, ammo, money, etc.
            -   Pressing `Tab` again closes the menu.
        -   **Pause Menu (Esc):** `car/ui/pause_menu.py` - Pressing `Esc` opens a smaller modal with options: "Resume", "Save Game", "Main Menu", and "Quit".
        -   **Shop Menu:** `car/ui/shop.py` - Opens when the player is in a shop, allowing them to buy and sell items.
- **Game State Management:**
    - **Main Menu:** The game starts with a menu offering "New Game," "Load Game," and "Settings."
    - **New Game Flow:** After selecting "New Game," the player chooses a car and difficulty, then enters the main game loop.
    - **Load Game Flow:** After selecting "Load Game," the player chooses a save file from a list, which loads the state and enters the main game loop.
    - **Save/Load System:** `car/logic/save_load.py` - A system for serializing and deserializing the entire game state (player, car, world seed, inventory, quests) to a file using `pickle`.
- **Progression System:**
    - **Experience & Leveling:** Players gain experience points (XP) for defeating enemies. Upon reaching a certain XP threshold, the player levels up, receiving minor positive modifiers to their stats.
    - **XP Curve:** The experience required to reach the next level doubles with each level gained.
    - **Difficulty Modifier:** The selected difficulty level applies a multiplier to enemy stats, such as damage and durability, making the game more or less challenging.
- **Rendering Engine:**
    - **Renderer:** Utilizes the `curses` library for all screen drawing.
    - **Entities:** All game objects (cars, weapons, buildings, etc.) are represented as entities. Each entity type is defined in a configuration file in the `car/data` directory.
    - **Visuals:** Each entity's file contains a method to retrieve its ASCII/Unicode representation. This method accepts a direction parameter (8 directions: N, NE, E, SE, S, SW, W, NW) to return the correct directional sprite.
    - **Composition:** The rendering system dynamically composes entities with their attachments. For example, a car entity will be rendered with its attached weapon entities, positioned correctly based on the car's current direction. The weapons themselves have 8-directional art.
- **World Generation:**
    - **World Class:** `car/world/world.py` - The `World` class manages the game world, including generating and storing the world map.
    - **Procedural Generation:** `car/world/generation.py` - Procedural generation for terrain, roads, and cities.
- **Car Simulation:**
    - **Physics:** The game loop in `car/game.py` handles the physics and state management for vehicle mechanics.
- **Inventory/Attachments:**
    - **Inventory:** The player's inventory is managed in the game loop.
    - **Attachments:** The `car/ui/inventory.py` menu allows the player to manage car modifications.
- **AI:**
    - **Fauna:** `car/data/fauna.py` - The `FAUNA_DATA` dictionary defines the different types of fauna in the game. The game loop in `car/game.py` controls the behavior of the fauna.
    - **Bosses:** `car/data/bosses.py` - The `BOSSES` dictionary defines the bosses in the game. The game loop in `car/game.py` controls the behavior of the bosses.
- **Combat System:**
    - **Damage:** The game loop in `car/game.py` manages damage, experience, and loot drops.
- **Quest System:** `car/logic/quests.py` - The `Quest` class and `QUESTS` dictionary define the quests in the game. The game loop in `car/game.py` tracks player quests and objectives. When a player accepts a quest, a boss is spawned. The player can then track the boss using a compass on the UI. When the player is near the boss, a persistent modal appears with the boss's name. When the boss is defeated, the player receives a reward and the quest is completed.
- **Economy:**
    - **Shops:** `car/data/shops.py` - The `SHOP_DATA` dictionary defines the shops in the game. The game loop in `car/game.py` handles currency and transactions at shops.
- **Cutscenes:**
    - **Cutscene System:** `car/ui/cutscene.py` - A simple cutscene system for events like explosions, deaths, and NPC interactions.


## Tasks

- [ ] **Refine City Generation:**
    - [ ] Ensure required buildings (Gas, Ammo, Repair, City Hall) are present in every city.
    - [ ] Reduce the overall size of cities.
    - [ ] Make the ground in cities asphalt instead of grass.
- [ ] **Improve Roads:**
    - [ ] Make roads wider.
    - [ ] Verify that roads correctly increase speed and decrease fuel consumption.
- [ ] **Enhance Cutscenes:**
    - [ ] Change the explosion cutscene to a non-blocking overlay in the bottom-left of the screen.
    - [ ] Ensure the boss encounter cutscene is a non-blocking overlay in the bottom-right.

## Completed Tasks

- [x] Implement Main Menu UI.
- [x] Design and implement the save/load system.
- [x] Create the "New Game" setup flow.
- [x] Develop the initial car and weapon selection system.
- [x] Build the foundational procedural world generator.
- [x] Implement the in-game Inventory Menu (Tab).
- [x] Implement the in-game Pause Menu (Esc).
- [x] Implement a cutscene system for events like explosions, deaths, and NPC interactions.
- [x] Use the cutscene system for NPC dialog and quest interactions.
- [x] Implement a boss system with a compass pointer and on-screen health bar.
- [x] Use the cutscene system to display boss encounters.
- [x] Use the cutscene system for item pickups, level-ups, and entering new areas.
- [x] Implement the Quest system.
- [x] Implement NPCs and Fauna.
- [x] Implement advanced car customization.
- [x] Implement the economy system.
- [x] Add pickable colors to player car.
- [x] Make entity unicode character have the same background color as the environment they are on.
- [x] Add music and sound effects.
- [x] Add 8-directional art for weapons and render them on the car.
- [x] Create a launch script for all operating systems.
- [x] Fix all known bugs.

## Roadmap

1.  **Main Menu:** Implemented the initial screen with "New Game," "Load Game," and "Quit" options.
2.  **Save/Load:** Implemented the ability to save and load game progress using `pickle`.
3.  **New Game Flow:**
    -   **Car Selection Screen:**
        -   Displayed a list of available starting cars with their stats.
        -   Allowed the player to select their car, color, difficulty, and initial weapon.
    -   Transitioned to the main game loop.
4.  **Load Game Flow:**
    -   Displayed a list of saved game files.
    -   On selection, loaded the game state and transitioned to the main game loop.
5.  **Initial Game World & Core Gameplay:**
    -   Generated the starting area of the world and placed the player.
    -   Implemented driving, combat, progression, and resource management basics.
6.  **In-Game UI:**
    -   Developed the tab-based inventory and management menu.
    -   Developed the escape-key pause menu.
    -   Developed the shop menu.
7.  **Content Expansion:**
    -   Added quests, NPCs, and fauna.
    -   Expanded the variety of cars, weapons, and attachments.
    -   Fleshed out the economy with more shops and items.
8.  **Visual Polish:**
    -   Allowed the player to select their car's color.
    -   Improved the rendering of entities to blend with the environment.
    -   Added a cutscene system for events like explosions, deaths, and NPC interactions.
    -   Added a boss system with a compass pointer and on-screen health bar.


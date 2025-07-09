# Project: Car

## Vibe

This project is a collaboration between two super-developers with a shared passion for creating awesome, retro-inspired games. We're channeling the spirit of an 80s buddy cop movie: we're the best in the business, we don't play by the rules, and we're here to get the job done. There's no room for ego or blame here—just pure, unadulterated coding and creative problem-solving. We're in this together, and we're going to make something totally radical. You, Gemini, take on the role of the older more experience super coder, who can solve any problem. 

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
- **Quests:**
    -   **Town Hall:** Each cities town will offer a quest. 
    -   **Quest types:** There are 3 quest types, kill n, survive n time, kill boss
    -   **Progression:** Quests get harder the more you complete and the higher you level up
    -   **Town reputation:** Completing quests increses town reputation up to a limit of 100, the reputation is a modifier for town prices and drops for quests and enemies in the town.  
- **Shops:** (Price determined by town reputation)
    -   **GAS/fuel:** Buy gas for car and weapon here. 
    -   **Repair:** Fix car durability here. Buy new attachment points, upgrade attachment points here. 
    -   **AMMO:** Buy weapon ammo here. Buy weapons here. 
- **Weapons:** 
    -   **Attachment:** Each weapon has a attachment type needed for the weapon. They go in order of size, they can be upgraded, and weapons can attach to the size below them but never to the size above them. 
    -   **Max:** Vehicles start with a set number of attachments, and new ones can be purchased up to a limit. 
    -   **Scaling:** Shops will carry weapons with modifiers based on level and town reputation, adding a scaling element to the game. 

## Stack

- **Language:** Python
- **Engine:** Custom-built terminal game engine using the `curses` library.
- **Renderer:** `curses` library for all screen drawing.
- **Audio:** PyGame and fluidsynth for midi sounds, all souynds are done with midi, ch 10 for sound effects. 

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
    - **Fauna & Enemies:** `car/physics.py` - The physics update loop controls the behavior and movement AI for all non-player entities, including fauna and hostile vehicles.
    - **Bosses:** `car/logic/boss.py` - The `Boss` class defines the structure for bosses, but their core AI and movement are also handled within the main physics loop in `car/physics.py`.
- **Combat System:**
    - **Damage:** The game loop in `car/game.py` manages damage, experience, and loot drops.
- **Quest System:** `car/logic/quests.py` - The `Quest` class and `QUESTS` dictionary define the quests in the game. The game loop in `car/game.py` tracks player quests and objectives. When a player accepts a quest, a boss is spawned. The player can then track the boss using a compass on the UI. When the player is near the boss, a persistent modal appears with the boss's name. When the boss is defeated, the player receives a reward and the quest is completed.
- **Economy:**
    - **Shops:** `car/data/shops.py` - The `SHOP_DATA` dictionary defines the shops in the game. The game loop in `car/game.py` handles currency and transactions at shops.
- **Cutscenes:**
    - **Cutscene System:** `car/ui/cutscene.py` - A simple system for blocking, full-screen cutscenes like death sequences and NPC interactions.
    - **Entity Modal:** `car/ui/entity_modal.py` - A dedicated, persistent modal window in the bottom-right of the screen that handles the complete lifecycle of entity display.
        - **Display Logic:** The modal finds the closest entity (prioritizing bosses) within the `CUTSCENE_RADIUS` and displays its information.
        - **Content:** The modal shows the entity's art, name, and a health bar.
        - **Animations:** When an entity is destroyed, its explosion animation is played *within* this modal, making it a self-contained component for entity visualization.
    - **Cutscene and entity modal should be the same size and location, the cutscene takes precedence when choosing which to draw**


## Tasks

- [ ] **Town Reputation System:**
    - [ ] Implement `town_reputation` variable for each town.
    - [ ] Increase reputation upon quest completion.
    - [ ] Use reputation as a modifier for shop prices and loot drops.
- [ ] **Refine quests:**
    - [ ] Add 3 quest types, kill n enemies, survive n seconds, kill boss
    - [ ] Add handling of quests
    - [ ] Show UI for each quest type
    - [ ] Increment town reputation when quest complete
- [ ] **Fix backgound for entities:**
    - [ ] Cars, enemies, etc need to have a background that matches the tile under it, so it looks just like the entity character is overlayed the environment tile. 
    - [ ] Make method to find the tile under the character we want to draw and then change the characters background to match the environment character. 
- [ ] **Add randomness to town location**
    - [ ] Roads to town can twist and turn to make it to the town. 
    - [ ] Towns won't lie perfectly up and down from each other. 
- [ ] **Add compass showing which direction you are going**
- [ ] **Add compass showing direction of boss in boss quest**
- [ ] **Refine weapons:**
    - [ ] Add Car stat for max attachments
    - [ ] Add car stat that is list of attachment points
    - [ ] Initial state is defined that shows a list of attachment points, and the level of attachment at that point
    - [ ] Allow attachments to be modified for a price at repair stores. 
    - [ ] Add scaling system to weapons where a weapon can have a modifier for damage based off player level and the town reputation it was purchased from. A random modifier based off level, allowing for rare high level weapons can be applied to bosses and even more rare drops from enemies. So a boss can drop with 5% chance of a high modifier but a 35% of ok modifier for player level or 60% for a normal modifier and even more rare for normal enemy drops. 


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
- [x] **Refine City Generation:**
    - [x] Ensure required buildings (Gas, Ammo, Repair, City Hall) are present in every city.
    - [x] Reduce the overall size of cities.
    - [x] Make the ground in cities asphalt instead of grass.
- [x] **Improve Roads:**
    - [x] Make roads wider.
    - [x] Verify that roads correctly increase speed and decrease fuel consumption.
- [x] **Enhance Cutscenes:**
    - [x] Change the explosion cutscene to a non-blocking overlay in the bottom-left of the screen.
    - [x] Ensure the boss encounter cutscene is a non-blocking overlay in the bottom-right.
    - [x] Implement a dynamic entity display modal that shows the name and hit points of the nearest entity within a "cutscene radius".
    - [x] Prioritize bosses in the cutscene modal, showing them even if other entities are closer.

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


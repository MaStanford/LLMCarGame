# Project: Car

## Vibe

This project is a collaboration between two super-developers with a shared passion for creating awesome, retro-inspired games. We're channeling the spirit of an 80s buddy cop movie: we're the best in the business, we don't play by the rules, and we're here to get the job done. There's no room for ego or blame here—just pure, unadulterated coding and creative problem-solving. We're in this together, and we're going to make something totally radical. You, Gemini, take on the role of the older more experience super coder, who can solve any problem. 

**Our Workflow:** For any new feature, bug fix, or refactor, our process is as follows:
1.  **Discuss the Goal:** We'll first agree on what we're trying to achieve.
2.  **Formulate a Plan:** Gemini will propose a clear, step-by-step plan outlining the necessary code changes, new files, and documentation updates.
3.  **Approve and Execute:** Once the plan is approved, Gemini will execute it. This ensures we're always in sync and building with a shared vision.
4.  **Update documentation and task list:** Context must be updated, tasks updated, architecture, and game overview. 
5.  **Verify:** Verify the changes or fix or feature is working. 
6.  **Commit Changes:** After the changes are made, and verified, Gemini will keep track of the modified files and prompt to either commit the changes or wait for more changes.

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

### Logging

The game includes a logging system for debugging purposes. By default, logging is disabled.

-   **Enabling Logging**: To enable logging, run the game with the `--log` command-line flag:
    ```bash
    ./run_game.sh --log
    ```
-   **Log File**: When enabled, all logging information is written to `game.log` in the root directory of the project. This file is overwritten each time the game is run with the `--log` flag.
-   **Log Content**: The log contains information about the game's state, rendering, and any errors that occur. This is the first place you should look when debugging an issue.

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
- **Rendering Engine & The Rendering Queue:**
    - **Core Principle**: To ensure proper layering and Z-indexing of all visual elements (UI, entities, terrain, etc.), **no component should ever draw directly to the screen**. Direct calls to `stdscr.addch()` or `stdscr.refresh()` from game logic or UI files are strictly forbidden.
    - **The Rendering Queue (`car/rendering/rendering_queue.py`)**: This is a global, centralized queue that holds all drawing operations for a single frame.
        -   **How it Works**: Other modules add drawing functions (like `stdscr.addch` or `draw_sprite`) to the queue, specifying a `z_index`.
        -   **Z-Indexing**: The `z_index` is an integer that determines the drawing order. Lower numbers are drawn first (appearing in the background), and higher numbers are drawn last (appearing in the foreground).
        -   **Usage**: To add an operation, use `rendering_queue.add(z_index, function, *args, **kwargs)`. For example: `rendering_queue.add(10, stdscr.addstr, y, x, "Player", text_color)`
    -   **The Main Loop's Role**: The main game loop in `car/game.py` (and other UI-specific loops) orchestrates the rendering process for each frame:
        1.  `stdscr.erase()`: Clears the screen.
        2.  `render_game()` / `draw_menu()`: These functions are called to populate the `rendering_queue` with all necessary drawing commands for the current frame.
        3.  `rendering_queue.draw(stdscr)`: This is the final and most important call. It sorts all queued operations by their `z_index` and executes them in order. It is also responsible for calling `stdscr.refresh()` to display the completed frame.

#### Drawing Complex UI (e.g., Modals)

To render stateful UI elements like menus or modals without violating the decoupled nature of the rendering queue, we follow this pattern:

1.  **The UI Component's Role (The "Dumb" Component)**:
    *   A UI class (e.g., `PauseMenu`) should have a `draw(self, stdscr)` method.
    *   This method's **only responsibility** is to translate the component's internal state into primitive drawing commands, which it adds to the global `rendering_queue`.
    *   It calculates the coordinates and Z-indices for its elements (boxes, text, etc.) and calls `rendering_queue.add(...)` for each one. It **never** draws directly to the screen.

2.  **The Game Logic's Role (The "Smart" Controller)**:
    *   The main game loop (or a dedicated UI controller) manages the UI component's state (e.g., `game_state.is_paused`).
    *   When it's time to render the component, the logic simply calls the component's `draw(stdscr)` method. This single call is what populates the queue with all the necessary drawing instructions for that component.

3.  **The Rendering Queue's Role (The "Blind" Executor)**:
    -   The queue remains completely ignorant of what a "modal" or "menu" is. It only sees a flat list of primitive `curses` functions to execute.

This ensures that UI components are self-contained but still respect the global Z-indexing and rendering pipeline, preventing architectural decay.
- **World Generation:**
    - **World Class:** `car/world/world.py` - The `World` class manages the game world, including generating and storing the world map.
    - **Procedural Generation:** `car/world/generation.py` - Procedural generation for terrain, roads, and cities.
- **Car Simulation:**
    - **Physics:** The game loop in `car/game.py` handles the physics and state management for vehicle mechanics.
- **Inventory/Attachments:**
    - **Inventory:** The player's inventory is managed in the game loop.
    - **Attachments:** The `car/ui/inventory.py` menu allows the player to manage car modifications.
- **Entity Component System (ECS-like):** The game is built on a class-based entity architecture. All game objects (vehicles, enemies, NPCs, etc.) are instances of classes that inherit from a base `Entity` class. This provides a clean, object-oriented, and highly extensible framework for adding new content.
        - **`car/entities/base.py`:** Defines the abstract `Entity` class with common properties (`position`, `health`) and methods (`update`, `draw`).
        - **`car/entities/`:** This directory contains subdirectories for each major entity type (`vehicles`, `characters`, `projectiles`).
            - **Vehicles (`car/entities/vehicles/`):** Contains classes for all drivable entities.
                - `PlayerCar`: Handles player input.
                - `EnemyCar`: Contains the phase-based AI logic for hostile vehicles.
            - **Characters (`car/entities/characters/`):** For on-foot entities.
                - `Bandit`: A simple melee enemy with its own AI.
                - `NPC`: For non-hostile characters.
    - **Spawning and Management:**
        - **Entity Registry:** A central registry will map entity type names (e.g., "bandit") to their corresponding classes.
        - **Spawning Logic (`car/logic/spawning.py`):** A dedicated module will handle the logic for when and where to spawn new entities, creating new instances of the appropriate classes and adding them to the `GameState`.
        - **Game State:** The `GameState` object now holds lists of active entity *objects*, not raw data.
    - **Main Loop:** The main game loop in `car/game.py` is now significantly simplified. It iterates through the master list of entities and calls their `update()` and `draw()` methods, delegating all logic to the entities themselves.
- **Adding New Entities:** To add a new entity (e.g., a new car or enemy), follow these steps:
    1.  **Create a new Python file** in the appropriate subdirectory of `car/entities/`. For example, a new car would go in `car/entities/vehicles/`. The filename should be the snake_case version of the entity's name (e.g., `my_new_car.py`).
    2.  **Define a new class** in this file that inherits from the appropriate base class (e.g., `PlayerCar` for a new player vehicle, `Vehicle` for an enemy vehicle, or `Character` for an on-foot character).
    3.  **Implement the necessary attributes** for the class, such as `art`, `durability`, `speed`, etc.
    4.  **Add the new entity's name** to the appropriate list in `car/logic/spawning.py` (`ENEMIES` or `FAUNA`). For player cars, add the filename to the `CARS_DATA` list in `car/data/cars.py`. The spawning system will automatically pick up the new entity.
- **AI and Phase System:**
    - **Core Design:** The AI for enemies and bosses is built on a phase-based state machine. Each entity has a `current_phase` that dictates its behavior and a `phase_timer` that determines when to transition to a new phase. This allows for dynamic and varied combat encounters.
    - **Shared Behaviors (`car/logic/ai_behaviors.py`):** Common AI movement patterns (e.g., `_execute_chase_behavior`, `_execute_strafe_behavior`) are centralized in this file. This avoids code duplication and allows for easy reuse across different entity types.
    - **Data Structure:** AI phases are defined directly in the entity's class definition (e.g., `car/entities/characters/bandit.py`). Each entity has a list of possible phases, and each phase defines its duration, behavior, and a weighted list of possible next phases.
    - **Execution Flow:** The main AI update loop in `car/logic/physics.py` is responsible for:
        1.  Initializing an entity's AI state upon spawning (setting the initial phase and timer).
        2.  Decrementing the `phase_timer` each frame.
        3.  When the timer expires, selecting a new phase based on the defined probabilities and resetting the timer.
        4.  Calling the appropriate behavior function (e.g., `_behavior_chase`, `_behavior_strafe`) based on the entity's current phase.
- **Python Package Conventions (`__init__.py`):** To keep the code clean and imports logical, we use `__init__.py` files to define the public API of a package. If you create a function in `my_package/my_module.py` that needs to be accessible elsewhere, you should import it into `my_package/__init__.py` like so: `from .my_module import my_function`. This allows other parts of the code to import it directly with `from my_package import my_function`, which is cleaner than `from my_package.my_module import my_function`.
- **Relative Imports:** When importing between modules inside the `car` package, use relative imports. The number of leading dots corresponds to the number of directories you need to go up. For example, from `car/entities/vehicles/player_car.py` to get to `car/rendering/draw_utils.py`, you need to go up three levels (`...`) to the `car` directory, then down into `rendering`. From `car/entities/obstacle.py`, you only need to go up two levels (`..`).
- **Combat System:**
    - **Damage:** The game loop in `car/game.py` manages damage, experience, and loot drops.
- **Quest System:** `car/logic/quests.py` - The `Quest` class and `QUESTS` dictionary define the quests in the game. The game loop in `car/game.py` tracks player quests and objectives. When a player accepts a quest, a boss is spawned. The player can then track the boss using a compass on the UI. When the player is near the boss, a persistent modal appears with the boss's name. When the boss is defeated, the player receives a reward and the quest is completed.
- **Economy:**
    - **Shops:** `car/data/shops.py` - The `SHOP_DATA` dictionary defines the shops in the game. The game loop in `car/game.py` handles currency and transactions at shops.
- **Cutscenes & Modals:**
    - **`car/ui/cutscene.py`:** Manages **blocking, full-screen cinematic events**. This module is responsible for scenes that take over the entire screen and pause gameplay, such as the "Game Over" sequence or future narrative events.
    - **`car/ui/entity_modal.py`:** Handles the **persistent, non-blocking entity display**. This is a core HUD element that dynamically shows information about the closest enemy or boss during live gameplay. It also contains the logic for playing entity-specific animations, like explosions, within its modal window, ensuring that all aspects of an entity's dynamic visualization are handled in one place.

- **Faction and Reputation System:** The game features a dynamic faction and reputation system that influences gameplay and world state.
    - **Hub Cities and Factions:** The world is anchored by a few non-procedural **Hub Cities**, each serving as the capital for a specific **Faction**. The rest of the world is procedurally generated, with territory control determined by proximity to the nearest Hub City.
    - **Reputation:** The player's reputation with each faction is tracked in the `GameState`. Reputation is gained by completing quests for a faction and lost by completing quests against them or attacking their units.
    - **Dynamic Quests:** Quests are dynamically generated based on faction relationships. Faction leaders in Hub Cities offer quests that target their rivals, creating a system of conflict and consequence.
    - **Faction-Based Spawning:** Enemy spawn rates and types are determined by the player's location and their reputation with the controlling faction. Allied territory is safer, while hostile territory is more dangerous and populated with that faction's specific units.
    - **Territory Control:** If a player's actions cause a faction's reputation to drop to zero, the faction with the highest player reputation will take over the defeated faction's Hub City, altering the game world.
    - **Win/Loss Conditions:** The game has clear win/loss states based on the faction system. A player can win by helping their chosen faction achieve total domination or lose by becoming an enemy to all factions.

- **Coordinate System and Entity Physics:** To ensure consistent and predictable behavior for all in-game objects, the following conventions are strictly followed:
    - **Game World Orientation:** The game operates on a "North-is-Up" principle. An angle of `0` radians corresponds to North. This is in contrast to the standard mathematical convention where `0` radians is East. All physics and rendering calculations must account for this by subtracting `math.pi / 2` from the game angle before using it in standard trigonometric functions (`cos`, `sin`).
    - **Entity Bounding Box:** An entity's `width` and `height` are crucial for physics, rendering, and interaction. For entities with multiple directional sprites (like the player's car), the dimensions must be calculated to create a bounding box large enough to contain the widest and tallest sprites. This is handled by the `Entity.get_car_dimensions()` static method, which should be called in the entity's `__init__` method. For single-sprite entities, the dimensions are calculated directly from their art.
    - **Attachment Points and Particle Origins:** The visual location of a weapon on the car and the origin point of the particles it fires must be perfectly synchronized. Both are calculated using the same core logic:
        1.  Start with the entity's central world coordinates (`entity.x`, `entity.y`).
        2.  Define the attachment point as an `(x, y)` offset from this center.
        3.  Apply the entity's rotation to this offset using a standard 2D rotation matrix.
        4.  Add the rotated offset to the entity's central world coordinates.
    -   This ensures that the rendered position of the weapon and the logical origin of its projectiles are always identical, preventing visual disconnects. The `car/rendering/renderer.py` module is the source of truth for this calculation.


## Tasks


### General Tasks
- [ ] **Finish unfinished AI behaviors:**
    - [ ] _execute_patrol_behavior
    - [ ] _execute_deploy_mine_behavior
- [ ] **Show game over dialog with qoute when you die and prompt for new game, load, or quit**
- [ ] **Combat system** 
    - [ ] For minor enemies open world combat. Running away just means getting out of aggro range. 
    - [ ] For major enemioes, combat system modal when in range, short range like pokemon battles. 
        - [ ] Phase based combat
        - [ ] Enemy dialog in phases
        - [ ] Enemy tactic and weapon changes in phases
        - [ ] Phases based off enemy health, or player health, or time or other factors
        - [ ] You can try to run, failing quest if in a quest, but otherwise surviving. 
- [ ] **Faction boss**
    - [ ] You can fight the faction leader for massive faction score for winning or losing. This is an epic boss and is actually needed to take over a faction once it's at 0 rep. Each faction has a different faction boss with immense stats. 
    - [ ] If you challenge them before their rep is 0, it's stats will be even more increased. But it will have a massive rep gain or loss, and if it brings it to 0 you still need to fight him he will just have less stats for the final fight like normal.  
- [ ] **Neutral city**
    - [ ] 0,0 is a neutral hub city. Quests help no faction. Shops don't have faction bonuses. This city will always be neutral and always have 0 spawn chance. 
- [ ] **Add shop keeper dialog:**, they will say something when we get in the shop. This is shop and faction specific and dynamically generated. 
    - [ ] When buying or selling high modifier equipment the shop keeper will make a comment, different comments based on the modifier. 
    - [ ] When you try to buy something without enough money, shop keeper makes a wise crack
- [ ] **Weapon swivel:**
    - [ ] Allow weapons to swivel with key presses like car turns
    - [ ] Swivel speed will be related to level
- [ ] **Add quest type:** 
    - [ ] Deliver package: Deliver a package to a towns city hall
- [ ] **Hub city static defense:**
    - [ ] Hub cities will have static defenses
    - [ ] We need to define 2 or 3 static defenses such as machine gun tower, flame thrower tower, impassable barbed wire and so on
    - [ ] How much static defenses is related to reputation.
- [ ] **Buildings are destructible in stages:**
    - [ ] Buildings are high health entities now
    - [ ] We need 4-5 art for buildings at various stages of destruction
    - [ ] At 0 HP, the building explodes and the faction loses reputation.
    - [ ] Attacking buildings will trigger enemy vehicles periodically.
- [ ] **Add offroad stat to cars:**
    - [ ] Cars will have an offroad stat
    - [ ] This is a modifier that allows better speed modifier in the wilderness
    - [ ] This is a modifier that gives bad speed modifier for street and city
    - [ ] This is a modifier that gives bad modifier for fuel consumption
- [ ] **Add more terrain types:**
    - [ ] Grass
    - [ ] Desert
    - [ ] Mud
    - [ ] Sand
    - [ ] Swamp
    - [ ] Factions will determine the terrain type. It is immersive so the deserts rats always have a lot fo desert and sand
    - [ ] Add Faction property that is terrain and percent chance


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
- [x] **Refine weapons:**
    - [x] Add Car stat for max attachments
    - [x] Add car stat that is list of attachment points
    - [x] Initial state is defined that shows a list of attachment points, and the level of attachment at that point
    - [x] Allow attachments to be modified for a price at repair stores. 
- [x] **Implement Weapon Scaling and Modifier System:**
    - [x] Shops will carry weapons with modifiers based on player level and town reputation.
    - [x] Enemies and bosses will have a chance to drop weapons with randomly generated modifiers.

### Stage 1: Faction and Reputation Foundation (Completed)
- [x] **Create `FACTION_DATA`:** Create a new file, `car/data/factions.py`, to define factions, their Hub City coordinates, and their relationships.
- [x] **Update `GameState`:** Replace `town_reputation` with `faction_reputation` in `car/game_state.py`.
- [x] **Update World Generation:** Modify `car/world/generation.py` to include a `get_city_faction` function that determines a city's faction based on proximity to a Hub City.
- [x] **Update Quest Logic:** Modify the `Quest` class in `car/logic/quests.py` to include `quest_giver_faction` and `target_faction`.
- [x] **Update Reputation Gain:** Modify the quest completion logic in `car/logic/quest_logic.py` to correctly increase reputation with the `quest_giver_faction`.

### Stage 2: Conflict and Consequences (Completed)
- [x] **Implement Opposed Quests:** Generate quests that target rival factions based on the `FACTION_DATA` relationships.
- [x] **Implement Reputation Loss:** Add logic to handle losing reputation by completing opposed quests or attacking allied units.
- [x] **Implement Quest Failure:** Add timers and escape conditions to quests, and apply reputation penalties on failure.

### Stage 3: Dynamic World and Territory Control (Completed)
- [x] **Implement Faction-Based Spawning:** Refactor the `spawn_enemy` logic to change spawn rates and enemy types based on the player's location and faction alignment.
- [x] **Implement Territory Takeover:** Create the logic for a faction to take over a rival's Hub City when their reputation with the player drops to zero.
- [x] **Implement Win/Lose Conditions:** Define the final win state (chosen faction dominates) and lose state (player is hostile with all factions).

### Stage 4: Immersive Faction & Quest UX (Completed)
- [x] **Create Data Structures:** Create `car/data/city_info.py` to store descriptive text for towns and hubs, preparing for future API integration.
- [x] **Implement Faction Status UI:** Add a "Factions" tab to the inventory menu to display player reputation with all known factions.
- [x] **Create City Hall Interaction Logic:** Develop a new, dedicated module (`car/logic/city_hall_logic.py`) to manage the multi-step interaction flow within City Halls.
- [x] **Create City Hall UI:** Develop a new UI module (`car/ui/city_hall.py`) with functions to draw the main dialog, the town info box, and the detailed quest briefing screen.
- [x] **Integrate Quest Briefing:** Connect the dynamic quest generation to the new briefing screen, allowing players to see rewards and consequences before accepting a contract.
- [x] **Update Main Game Loop:** Replace the old quest interaction call with the new, more comprehensive City Hall interaction system.

## Roadmap

## Known Issues

- **Curses/Terminal Errors:** The game may crash on startup with a `curses` error (e.g., `nocbreak() returned ERR`). This is often due to an incompatible terminal environment or the terminal window being too small. This is a known issue with the `curses` library and the environment in which the game is being run. **Gemini, do not attempt to fix this error.** It is an environmental issue, not a code issue.

# Project: The Genesis Module

## Vibe

This project is a collaboration between two super-developers with a shared passion for creating awesome, retro-inspired games. We're channeling the spirit of an 80s buddy cop movie: we're the best in the business, we don't play by the rules, and we're here to get the job done. There's no room for ego or blame here—just pure, unadulterated coding and creative problem-solving. We're in this together, and we're going to make something totally radical. You, Gemini, take on the role of the older more experience super coder, who can solve any problem. 

**Our Workflow:** For any new feature, bug fix, or refactor, our process is as follows:
1.  **Discuss the Goal:** We'll first agree on what we're trying to achieve.
2.  **Formulate a Plan:** Gemini will propose a clear, step-by-step plan outlining the necessary code changes, new files, and documentation updates.
3.  **Approve and Execute:** Once the plan is approved, Gemini will execute it. This ensures we're always in sync and building with a shared vision.
4.  **Update documentation and task list:** Context must be updated, tasks updated, architecture, and game overview. 
5.  **Verify:** Verify the changes or fix or feature is working. 
6.  **Commit Changes:** After the changes are made, and verified, Gemini will keep track of the modified files and prompt to either commit the changes or wait for more changes.

**Preferred tools:**
1. Git tools for reading files
2. Always grab the latest version of the file, it's very possible we have changes outside this session.

## Summary

This project is a terminal-based, open-world, automotive RPG survival game. Players select a starting vehicle and embark on an adventure in an infinitely-generated, random world, driven by a singular goal: to find the legendary "Genesis Module." This piece of pre-apocalypse technology is rumored to be the only thing powerful enough to allow a vehicle to escape the wasteland's harsh environment. The player's journey will involve navigating the complex political landscape of warring factions, taking on quests, and upgrading their vehicle in hopes of finally tracking down the module and winning their freedom.

### Key Gameplay Elements:
- **The Genesis Module:** The ultimate goal of the game. Finding this legendary car component allows the player to win by escaping the wasteland at a designated point on the world map (e.g., coordinates -300, -300).
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
    -   **Town reputation:** Completing quests increses town reputation up to a limit of 100, a reputation is a modifier for town prices and drops for quests and enemies in the town.  
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
- **Engine:** Textual TUI Framework
- **Audio:** PyGame and fluidsynth for midi sounds, all souynds are done with midi, ch 10 for sound effects. 

### Logging

The game includes a logging system for debugging purposes. By default, logging is disabled.

-   **Enabling Logging**: To enable logging, run the game with the `--log` command-line flag:
    ```bash
    ./run_game.sh --log
    ```
-   **Log File**: When enabled, all logging information is written to `game.log` in the root directory of the project. This file is overwritten each time the game is run with the `--log` flag.
-   **Log Content**: The log contains information about the game's state, rendering, and any errors that occur. This is the first place you should look when debugging an issue.

### Developer Mode

To use the Textual Devtools, you must first install the `textual-dev` package:
```bash
pip install textual-dev
```
Then, run the game with the `--dev` flag:
```bash
./run_game.sh --dev
```
This will enable the Textual inspector, which can be accessed by pressing `Ctrl+B`.

## Architecture

The game is built around the **Textual TUI framework**, which provides an event-driven, widget-based architecture. This replaces the previous manual `curses`-based rendering system.

- **Main Application (`car/app.py`):**
    -   The core of the application is the `CarApp(App)` class. It is responsible for managing screens, global state, and the main game loop.
    -   **Game Loop:** A timer created with `set_interval` calls an `update_game` method at a fixed rate (e.g., 30 FPS). This method is responsible for running all game logic (physics, AI, spawning) and then triggering a refresh of the UI.

- **UI and Rendering (Widgets & Screens):**
    -   **Widget-Based System:** All UI elements are **Textual Widgets**. This includes the main game view, HUD, menus, and modals. This approach eliminates flicker and provides a robust, cross-platform rendering solution.
    -   **Styling:** The appearance and layout of all widgets are defined in a central CSS file (`car/app.css`), allowing for easy and consistent styling.
    -   **Main Game Screen (`car/screens/world.py`):** This is the primary screen for gameplay. It uses a `Grid` layout to compose the following widgets:
        -   `GameView`: The base layer that renders the game world, player, and all other entities.
        -   `HUD`: An overlay displaying player stats.
        -   `Controls`: An overlay showing game controls.
        -   `EntityModal`: A reactive overlay in the bottom-right that displays information about the nearest enemy.
        -   `Explosion`: A temporary widget that is mounted to play an explosion animation when an entity is destroyed.
    -   **Modal Screens:** All menus (Main Menu, Pause, Inventory, Shop, City Hall) are implemented as Textual `Screen` or `ModalScreen` classes. They are composed of standard and custom widgets (like `Button`, `Select`, and our reusable `WeaponInfo` widget) and handle user interaction through Textual's event system (`on_button_pressed`).
    -   **Custom Focus Management in `NewGameScreen`**:
        -   **Problem**: Textual's standard focus system didn't suit the specific navigational needs of the `NewGameScreen`.
        -   **Solution**: A manual focus-handling system was implemented directly within `car/screens/new_game.py`.
        -   **Mechanism**:
            1.  An explicit list, `focusable_widgets`, defines the navigation order.
            2.  A `current_focus_index` tracks the active widget.
            3.  `action_focus_next` and `action_focus_previous` methods modify this index.
            4.  A helper method, `update_focus`, applies a `.focused` CSS class to the currently indexed widget.
            5.  Styling is then handled in `car/app.css` using descendant selectors (e.g., `CycleWidget.focused .cycle-value`).
        -   **Benefit**: This gives us precise control over the navigation flow and visual feedback, independent of Textual's built-in focus state.
    -   **The Grand Inventory UX Refactor (`InventoryScreen`)**:
        -   **Layout:** The inventory screen is a two-column layout. The left column contains the rotatable car preview and the "Loadout" list. The right column contains the scrollable player "Inventory" list, the `WeaponInfo` panel, and a comprehensive player stats display.
        -   **Interactive Preview:** The car preview can be rotated 360 degrees. When the "Loadout" list is focused, the currently selected attachment point flashes on the car preview, alternating between its index number and a circle icon.
        -   **Equip/Unequip Logic:** The screen uses a simple state machine to provide an intuitive workflow for equipping, unequipping, and swapping weapons between the inventory and the loadout.
        -   **Dynamic Info:** The `WeaponInfo` panel automatically updates to show the stats and modifiers of the currently selected weapon in either list.
    -   **The Grand Shop Overhaul (`ShopScreen`)**:
        -   **Layout:** The shop is a full-screen, four-quadrant grid. The top-left displays the shop's inventory, and the top-right displays the player's inventory. The bottom-left contains a dialog box for future shopkeeper interactions, and the bottom-right contains the detailed `WeaponInfo` panel, the `MenuStatsHUD` for player stats, and the main action button.
        -   **Buy/Sell Logic:** An action button dynamically changes between "Buy" and "Sell" depending on which inventory list is focused. Weapon shops allow selling items, with the price being calculated based on the item's base value, player level, and faction reputation. A two-press confirmation system prevents accidental sales.

- **Performance Optimizations:**
    -   **Pre-parsing Styles:** All style strings (e.g., `"white on blue"`) in the game's data files are parsed into `rich.style.Style` objects once at startup. The rendering loop then uses these pre-compiled objects, avoiding thousands of costly string-parsing operations every frame.
    -   **Batch Rendering:** The main `GameView` widget was optimized to address a significant performance bottleneck. Instead of drawing the screen character by character (which resulted in thousands of individual operations per frame), the rendering logic now groups adjacent characters with the same style into a single "run." This batching process dramatically reduces the number of operations required to draw the scene, leading to a major FPS improvement.
    -   **Future Optimizations:**
        -   **Culling Off-Screen Entities:** The rendering loop can be improved by skipping the drawing calculations for any entity that is currently outside the visible screen area.
        -   **Terrain Caching:** Since the terrain is static, the fully rendered `Text` object for the environment can be cached. It would only need to be regenerated when the player moves a significant distance, saving a huge amount of redundant processing on every frame.
        -   **Partial Screen Updates:** A more advanced optimization would be to track which specific parts of the screen have changed (e.g., where an entity has moved) and only redraw those "dirty" regions, rather than refreshing the entire game view.

- **Game State Management:**
    - **`GameState` Class:** The central `car/game_state.py` class continues to hold the entire state of the game. Widgets and logic functions read from and write to this single source of truth.
    - **Screen Stack:** Textual's app-level screen stack (`push_screen`, `pop_screen`) is used to navigate between the main game and various menu screens.

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
    - **Multipart Quests:** The quest system now supports multi-step quest chains. The `Quest` data structure includes a `next_quest_id` field, allowing for the creation of narrative arcs. The `CityHallScreen` provides a seamless UX for completing one part of a quest and immediately receiving the next. An explicit `requires_turn_in` flag allows for quests that complete immediately upon finishing their objectives.
- **Economy:**
    - **Shops:** `car/data/shops.py` - The `SHOP_DATA` dictionary defines the shops in the game. The game loop in `car/game.py` handles currency and transactions at shops.
- **Cutscenes & Modals:**
    - **`car/ui/cutscene.py`:** Manages **blocking, full-screen cinematic events**. This module is responsible for scenes that take over the entire screen and pause gameplay, such as the "Game Over" sequence or future narrative events.
    - **`car/ui/entity_modal.py`:** Handles the **persistent, non-blocking entity display**. This is a core HUD element that dynamically shows information about the closest enemy or boss during live gameplay. It also contains the logic for playing entity-specific animations, like explosions, within its modal window, ensuring that all aspects of an entity's dynamic visualization are handled in one place.

- **The Genesis Module: An Emergent Narrative Engine:** The game's narrative is not pre-written. It is generated on the fly by a Large Language Model (LLM), creating a unique story for every playthrough. This is achieved through a multi-stage, theme-aware pipeline.
    - **Dual Generation Modes:** The game supports two modes for content generation, selectable in the Settings menu:
        - **Local Mode (Default):** Uses a bundled, local LLM (`gemma-2b-it`). This mode is fully offline but can be slow, especially on older hardware. Due to the limitations of the local model, this mode currently uses a high-quality, hardcoded set of fallback data to ensure a stable and enjoyable experience.
        - **Gemini CLI Mode (Recommended):** Uses the Google Gemini CLI. This mode provides near-instantaneous world and quest generation and produces higher-quality narrative content. It requires the player to have the Gemini CLI installed and configured on their system.
    - **Theme-First Generation:** When starting a new game, the player is presented with three narrative themes generated by the LLM (e.g., "Wasteland Survival," "Cyberpunk Noir").
    - **Thematic Faction Generation:** The player's chosen theme is injected into a detailed prompt. The LLM then generates a unique set of 5 factions, complete with names, descriptions, relationships, and bosses that are all consistent with the overarching theme.
    - **Dynamic Quest Generation:** As the player explores the world, the game pre-fetches quests for nearby cities in the background. The prompt for these quests is dynamically built to include the player's chosen theme, the current state of the factions, the player's progress, and the specific details of the city offering the quest. This ensures that all generated content is thematically and narratively coherent.
    - **Dynamic Save System:** Each new game generates a unique world. This world state (including the generated `factions.py` and `quest_log.json`) is stored in a temporary `temp/` directory during play. When the game is saved, the contents of `temp/` are copied into a dedicated save slot in the `saves/` directory, creating a persistent, unique world for each playthrough.
    - **Dynamic Data Loading:** A dedicated module, `car/logic/data_loader.py`, intelligently loads game data. It checks for session-specific data in the `temp/` directory first, and falls back to the default data if none is found. This ensures the game always uses the correct data for the current session.

- **Wasteland Warfare & Conquest:** The core gameplay loop is built around a dynamic power struggle between factions.
    - **Faction Control:** Player actions directly impact the "Control" score of factions, affecting their economic and military strength.
    - **Decisive Battles:** When a faction's control drops to a critical level, a rival can offer the player a high-stakes "Decisive Battle" quest to eliminate the faction's leader.
    - **Conquest:** Winning a Decisive Battle results in a permanent conquest, altering the world map, faction relationships, and the units that spawn in the conquered territory.

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

### **Project: The Ghost in the Machine - A Dynamic, LLM-Powered World**

**Goal:** To overhaul the game's core progression by integrating a local LLM to generate quests and a new "Faction Control" system to make the world react to the player's choices.

**Phase 1: Foundational Architecture & Data**
- [x] **Create Directory Structure:** Create a new top-level directory named `prompts/` to store all our LLM-related templates and context files.
- [x] **Create Prompt Context:** Inside `prompts/`, create a new file, `game_context.txt`. This file will contain a concise, LLM-friendly summary of the game's world, mechanics, and factions, distilled from `GEMINI.md`.
- [x] **Create Quest Prompt Template:** Create `prompts/quest_prompt.txt`. This will be the master template for generating quests.
- [x] **Update `GameState`:** Add the `faction_control` dictionary to `car/game_state.py`.
- [x] **Update `FACTION_DATA`:** Add a default `control` value to each faction in `car/data/factions.py`.
- [x] **Install LLM Library:** Add `llama-cpp-python` to `requirements.txt`.

**Phase 2: Logic Implementation**
- [x] **Create `faction_logic.py`:** This new module will house the functions for increasing and decreasing Faction Control.
- [x] **Create `llm_quest_generator.py`:** This new module will contain the core `generate_quest_from_llm` function.
- [x] **Integrate Control with Quests:** Modify `car/logic/quest_logic.py` to call the new Faction Control functions upon quest completion or failure.
- [x] **Implement Quest Log:** Update `car/logic/save_load.py` to manage the new `quest_log.json` file.

**Phase 3: Making it All Matter (World Impact)**
- [x] **Dynamic Shops & Spawning:** Modify `car/logic/shop_logic.py` and `car/logic/spawning.py` to read the Faction Control scores and adjust their behavior accordingly.
- [x] **Implement Conquest:** Implement the "Decisive Battle" quest and the `handle_faction_takeover` logic.

**Phase 4: UI, Documentation, and Final Integration**
- [x] **Integrate LLM into City Hall:** Replace the old quest generation in `car/screens/city_hall.py` with a call to our new LLM-powered generator.
- [x] **Update UI:** Update the Factions UI and the Quest Briefing screen to display the new Faction Control information.
- [x] **Update Documentation:** Thoroughly update `README.md` and `GEMINI.md` to document this groundbreaking new system.

### **Project: The Genesis Engine - LLM-Powered Faction Generation**

**Goal:** To extend the "Ghost in the Machine" system to allow the LLM to generate the factions themselves at the start of a new game, with a robust save/load system to manage these unique worlds.

**Phase 1: The "Live Session" Architecture**
- [x] **Create Temporary Directory:** Create a `temp/` directory for live session data and add it to `.gitignore`.
- [x] **Modify New Game Flow:** Update the `NewGameScreen` to generate factions and write them to `temp/factions.py`.
- [x] **Create Dynamic Data Loader:** Create `car/logic/data_loader.py` to intelligently load session-specific data from `temp/`.
- [x] **Refactor Imports:** Update all modules to use the new data loader instead of direct imports.

**Phase 2: The "Save Slot" Architecture**
- [x] **Create Save Game Directory:** Create a `saves/` directory to store all save game slots.
- [x] **Implement "Save Game" Logic:** Overhaul `save_load.py` to save all session files from `temp/` into a named save slot directory.
- [x] **Implement "Load Game" Logic:** Overhaul `save_load.py` to copy files from a named save slot into `temp/` and then load the game.
- [x] **Update UI:** Refactor the `LoadGameScreen` and `PauseMenuScreen` to use the new save slot system.

### **Project: The Living Context Engine**

**Goal:** To create a system that dynamically builds a rich, stateful context prompt every time we need to generate content from the LLM.

**Phase 1: Implementation**
- [x] **Create `prompt_builder.py`:** Create a central module to assemble dynamic contexts.
- [x] **Create `quest_log.json`:** Create the initial temporary quest log.
- [x] **Update Prompt Templates:** Refactor prompt templates to use dynamic placeholders.
- [x] **Integrate Prompt Builder:** Refactor the LLM generator modules to use the new builder.

### **Project: The Commander's Dashboard - Polishing the Player Experience**

**Goal:** To create all the necessary UI elements and feedback loops for the player to understand, track, and influence the dynamic faction and quest systems.

**Phase 1: UI Implementation**
- [x] **Create Faction Command Screen:** Build a dedicated modal screen, bound to the 'f' key, for viewing detailed faction intelligence.
- [x] **Enhance HUD:** Integrate a territory display, boss compass, and quest objective tracker into the existing HUD elements.
- [x] **Implement Immersive Quest Flow:** Create a quest briefing screen and a quest completion summary screen.
- [x] **Build Save/Load UI:** Create a modal for naming save games.

### **Project: The Living Wasteland - Dynamic World & Narrative Events**

**Goal:** To transform the game from a series of static locations into a deeply immersive and reactive world. This will be achieved by expanding our generative systems to name the world's features, create unique equipment, and introduce a new layer of narrative delivery through world-based triggers and discoveries.

---

#### **Phase 1: Dynamic Naming & World Details (The Cartographer)**

**Objective:** To give every significant location a unique, theme-appropriate name, making the world feel authored and consistent.

*   **[ ] Create `world_details_prompt.txt`:**
    *   This prompt will be triggered after faction generation.
    *   **Input:** The world theme and the complete faction data (names, vibes, locations).
    *   **Output:** A single, clean JSON object containing:
        *   `cities`: A dictionary mapping city coordinates (e.g., `"0,0"`) to generated names (e.g., `"The Nexus"`).
        *   `roads`: A list of objects, each defining a major road between two cities with a generated name (e.g., `{"from": "The Nexus", "to": "Rust-Tusk Outpost", "name": "The Ashen Highway"}`).
        *   `landmarks`: A list of objects, each defining a point of interest with coordinates and a generated name (e.g., `{"x": 150, "y": -200, "name": "The Sunken Oasis"}`).
*   **[ ] Integrate into World Generation:**
    *   Update the `generate_initial_world_worker` in `car/workers/world_generator.py` to call the new prompt.
    *   The worker's final output dictionary will now include a `world_details` key.
*   **[ ] Update Save/Load System:**
    *   Modify `save_game` and `load_game` in `car/logic/save_load.py` to handle a new `world_details.json` file within each save slot.
    *   Update `GameState` to store this `world_details` data.
*   **[ ] Update UI and Game Logic:**
    *   Refactor `car/widgets/hud_location.py` to display the generated city name instead of a generic ID.
    *   Modify the `MapScreen` to display city and road names.
    *   Update quest dialogs and descriptions to reference named locations (e.g., "Deliver this package to *Rust-Tusk Outpost* via *The Ashen Highway*").

---

#### **Phase 2: Emergent Encounters & Narrative Triggers (The Storyteller)**

**Objective:** To break the narrative out of the City Hall and have it unfold dynamically as the player explores the world. This introduces two new systems: "World Triggers" and "Narrative Discoveries."

*   **[ ] Implement World Trigger System:**
    *   **Concept:** These are invisible, circular zones on the world map that trigger an event when the player enters them. This is perfect for ambushes, unique NPC encounters, or atmospheric story moments.
    *   **Data Structure:** Define a `triggers.json` file, which can be generated or handwritten. Each trigger will have:
        *   `id`: A unique identifier.
        *   `x`, `y`, `radius`: The location and size of the trigger zone.
        *   `type`: The type of event (`dialog`, `combat`, `quest`).
        *   `data`: The specific content (e.g., the dialog to display, the enemies to spawn, the quest ID to grant).
        *   `one_shot`: A boolean to determine if the trigger can be activated multiple times.
    *   **Game Loop Integration:** In `car/app.py`, add a new function to the main `update_game` loop that checks the player's distance to all active triggers.
*   **[ ] Implement Narrative Discovery System:**
    *   **Concept:** Allow certain in-world objects (initially, destroyed enemy vehicles and specific obstacles) to have a chance to drop a "lore item" or a "quest lead" instead of just loot.
    *   **Loot Table Modification:** Update the loot generation logic in `car/logic/loot_generation.py` to include a new drop type: `narrative_item`.
    *   **Item Interaction:** When a player picks up a `narrative_item`, it will trigger a simple dialog screen that displays a snippet of story or a rumor, potentially leading to a new, hidden quest.
    *   **Example:** Destroying a "Scrap Barricade" might have a 5% chance to drop a "Tattered Journal." Picking it up reveals a dialog: *"The journal speaks of a hidden cache of pre-war tech in a cave to the east..."* and places a new waypoint on the player's map.

---

#### **Phase 3: The Generative Armory (The Blacksmith)**

**Objective:** To use the LLM to generate unique, named variants of existing weapons and vehicles, creating a much deeper and more rewarding loot system. This will use the "Template and Modifier" system we discussed.

*   **[ ] Create Base Templates:**
    *   Formalize our existing Python classes for `Weapon` and `Vehicle` as the definitive "base templates."
*   **[ ] Develop a "Modifier" Data Structure:**
    *   Define a clear JSON structure for how the LLM can specify modifications.
    *   **Example:** `{"name": "The Dust-Devil", "base_item": "hatchback", "description": "A modified hatchback built for speed on rough terrain.", "stat_modifiers": {"speed": 1.1, "durability": 0.9, "handling": 1.05}, "cosmetic_tags": ["spikes", "rust"]}`.
*   **[ ] Create `item_generator_prompt.txt`:**
    *   This prompt will be used to generate new items as quest rewards or rare loot.
    *   **Input:** The world theme, player level, and the base item template.
    *   **Output:** A single, validated JSON object representing the new item variant.
*   **[ ] Implement a Strict Validation System:**
    *   Create a new function, `validate_generated_item(item_data)`, that rigorously checks every key and value in the JSON returned by the LLM.
    *   It must check data types, ensure stat modifiers are within a reasonable range, and verify that cosmetic tags exist in our pre-defined library.
    *   **Crucially:** If validation fails, the system must log the error and fall back to a standard, non-generated item to prevent crashes.
*   **[ ] Integrate into Loot System:**
    *   Update the loot generation logic to have a chance to call the `item_generator` instead of dropping a standard item, especially for boss fights or high-level quests.

### General Tasks
- [ ] **Gemini CLI Integration:**
    - [ ] Create a new "Settings" screen accessible from the main menu.
    - [ ] Add a toggle to switch between "Local" and "Gemini CLI" for world generation.
    - [ ] Create a wrapper in `car/logic/gemini_cli.py` to execute `gemini --yolo -p "..."` commands.
    - [ ] Refactor the `llm_..._generator.py` modules to use the Gemini CLI wrapper when the setting is active.
    - [ ] When "Local" is selected, the generators should use the hardcoded fallback data to ensure a stable offline experience.
    - [ ] Add error handling for when the `gemini` command is not installed, guiding the user to install it.
- [ ] **Neutral city**
    - [ ] 0,0 is a neutral hub city. Quests help no faction. Shops don't have faction bonuses. This city will always be neutral and always have 0 spawn chance. 
- [ ] **Add shop keeper dialog:**, they will say something when we get in the shop. This is shop and faction specific and dynamically generated. 
    - [ ] When buying or selling high modifier equipment the shop keeper will make a comment, different comments based on the modifier. 
    - [ ] When you try to buy something without enough money, shop keeper makes a wise crack
- [ ] **Weapon swivel:**
    - [ ] Allow weapons to swivel with key presses like car turns
    - [ ] Swivel speed will be related to level
    - [ ] Mouse can be used, cursor is where projectile will be shot at, so figure out angle to hit the cursor location and mouse click to shoot. 
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
- [ ] **Combat system** 
    - [ ] For minor enemies open world combat. Running away just means getting out of aggro range. 
    - [ ] For major enemioes, combat system modal when in range, short range like pokemon battles. 
        - [ ] Phase based combat
        - [ ] Enemy dialog in phases
        - [ ] Enemy tactic and weapon changes in phases
        - [ ] Phases based off enemy health, or player health, or time or other factors
        - [ ] You can try to run, failing quest if in a quest, but otherwise surviving. 

## Completed Tasks

## Roadmap

## Known Issues
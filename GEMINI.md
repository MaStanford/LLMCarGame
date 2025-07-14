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
    -   **Main Game Screen (`car/screens/default.py`):** This is the primary screen for gameplay. It uses a `Grid` layout to compose the following widgets:
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
        -   **Benefit**: This gives us precise control over navigation flow and visual feedback, independent of Textual's built-in focus state.

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

### **Project: Migration to Textual TUI Framework**

**Goal:** To perform a complete architectural migration from `curses` to the Textual framework. All UI elements, including menus, modals, and HUDs, will be rebuilt as interactive Textual widgets with a consistent, mouse-aware design. The result will be a stable, cross-platform, and modern application.

---

**Phase 1: Core Application & Game World**

- [ ] **Task 1: Foundational Setup**
    - [ ] Add `textual` to `requirements.txt`.
    - [ ] Create `car/app.py` to define the main `CarApp(App)` class. This will be our new entry point.
    - [ ] Modify `car/__main__.py` to launch `CarApp`.

- [x] **Task 2: The `GameView` Widget**
    - [x] Create `car/widgets/game_view.py` and define a `GameView(Widget)`.
    - [x] This widget's sole responsibility is to render the game world (terrain, entities, particles) based on the `GameState`. It will replace the old `render_game` function.

- [x] **Task 3: Game Loop Integration**
    - [x] In `CarApp`, use `set_interval` to call a new `update_game` method at a fixed rate (e.g., 30 FPS).
    - [x] This `update_game` method will contain all our existing game logic calls: `update_physics_and_collisions`, `spawn_enemy`, `update_quests`, etc. After updating the state, it will trigger a refresh of all visible widgets.

- [x] **Task 4: Initial Layout & Styling**
    - [x] Create `car/app.css` to define the application's visual style.
    - [x] Create a `DefaultScreen(Screen)` that uses a `Grid` layout to hold the main game interface.
    - [x] Compose the `GameView` as the base layer of this grid.

**Phase 2: HUD, Modals, and Overlays**

- [x] **Task 5: The `HUD` Widget**
    - [x] Create `car/widgets/hud.py` and define a `HUD(Widget)`.
    - [x] This widget will display all the player's stats (Durability, Gas, Speed, Cash, Ammo, etc.). It will be a reactive widget that automatically updates when the corresponding values in `GameState` change.

- [x] **Task 6: The `Controls` Widget**
    - [x] Create `car/widgets/controls.py` and define a `Controls(Widget)`.
    - [x] This will display the game controls ("WASD: Steer", "SPACE: Fire") in the top-left corner. Each control will be a styled, non-functional `Button` to provide a clear, interactive look.

- [x] **Task 7: The `EntityModal` Widget**
    - [x] Create `car/widgets/entity_modal.py` and define an `EntityModal(Widget)`.
    - [x] This widget will replace the old `draw_entity_modal` logic. It will be positioned in the bottom-right and will reactively display the name, art, and health bar of the closest enemy or boss.

- [x] **Task 8: The `Explosion` Widget**
    - [x] Create `car/widgets/explosion.py` and define an `Explosion(Widget)`.
    - [x] When an enemy is destroyed, the game will now mount a new `Explosion` widget at the entity's last position.
    - [x] The widget's `on_mount` event will use a series of `set_timer` calls to animate the explosion frames and then remove itself (`self.remove()`) when the animation is complete. This replaces the old `play_explosion_in_modal` logic.

- [x] **Task 9: Update `DefaultScreen` Layout**
    - [x] Add the `HUD`, `Controls`, and `EntityModal` widgets to the `DefaultScreen`'s grid layout, ensuring they are correctly positioned as overlays on top of the `GameView`.

**Phase 3: Menus and Interactive Screens**

- [x] **Task 10: The `WeaponInfo` Widget**
    - [x] Create `car/widgets/weapon_info.py` and define a `WeaponInfo(Widget)`.
    - [x] This will be a reusable component that displays the stats of a given weapon. It will be used in the Inventory, Shop, and New Game screens.

- [x] **Task 11: The Main Menu Screen**
    - [x] Create `car/screens/main_menu.py` and define a `MainMenuScreen(Screen)`.
    - [x] Re-implement the "New Game," "Load Game," and "Quit" options as large, centered, mouse-clickable `Button`s.
    - [x] The `on_button_pressed` event handlers will trigger the appropriate app-level actions (e.g., `self.app.push_screen(NewGameScreen())`).

- [x] **Task 12: The New Game & Load Game Screens**
    - [x] Create `car/screens/new_game.py` and `car/screens/load_game.py`.
    - [x] Rebuild these interfaces using Textual widgets (`Select`, `Button`, etc.) and integrate the `WeaponInfo` widget into the new game screen.

- [x] **Task 13: The Pause Menu Screen**
    - [x] Create `car/screens/pause_menu.py` and define a `PauseScreen(ModalScreen)`.
    - [x] Rebuild the pause options as `Button`s. The `on_button_pressed` handlers will resume the game (`self.app.pop_screen()`), save, or quit.

- [x] **Task 14: The Inventory Screen**
    - [x] Create `car/screens/inventory.py` and define an `InventoryScreen(ModalScreen)`.
    - [x] This will be a complex, multi-pane layout using Textual's grid system to display the car preview, attachment list, inventory, and stats. The `WeaponInfo` widget will be used here.

- [x] **Task 15: The Shop & City Hall Screens**
    - [x] Create `car/screens/shop.py` and `car/screens/city_hall.py`.
    - [x] Rebuild these interfaces with a consistent two-panel layout: one for the list of items/quests, and one for the detailed view (using the `WeaponInfo` widget for the shop). Both will feature a dialog box at the bottom for NPC text.

**Phase 4: Finalization & Cleanup**

- [x] **Task 16: Input & Event Binding**
    - [x] Replace all remaining logic from `car/logic/input.py` with Textual's event bindings (`on_key`, `on_button_pressed`).
    - [x] Delete `car/logic/input.py`.

- [x] **Task 17: Code Removal & Refactoring**
    - [x] Systematically delete the entire `car/rendering` directory.
    - [x] Delete all files in `car/ui` as they are replaced by their `widget` or `screen` counterparts.
    - [x] Remove `curses` and `windows-curses` from all `requirements` files.

- [x] **Task 18: Documentation Update**
    - [x] Thoroughly update `GEMINI.md` to reflect the new Textual-based architecture, including the widget hierarchy, event flow, and CSS styling approach.

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

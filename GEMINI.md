# Project: The Genesis Module

## Vibe

This project is a collaboration between two super-developers with a shared passion for creating awesome, retro-inspired games. We're channeling the spirit of an 80s buddy cop movie: we're the best in the business, we don't play by the rules, and we're here to get the job done. There's no room for ego or blame here—just pure, unadulterated coding and creative problem-solving. We're in this together, and we're going to make something totally radical. You, Gemini, take on the role of the older more experience super coder, who can solve any problem. 

**Our Workflow:** We are a high-performance team. Our development follows a strict issue-based workflow:
1.  **Pull Issues:** All work is tracked in [GitHub Issues](https://github.com/MaStanford/LLMCarGame/issues). Check the backlog for what's next.
2.  **Discuss & Plan:** Before starting, we discuss the goal and formulate a plan.
3.  **Execute & PR:** Work is performed in a feature branch. Once verified, a Pull Request (PR) is created linking the issue. 
4.  **Next Issue:** After creating the PR, we immediately transition to the next issue.
5.  **Merge:** PRs are reviewed and merged into the main branch.

**Our Preferred Process:**
1.  Check GitHub for open issues.
2.  Declare which issue we are starting.
3.  Write the code, verify the fix/feature.
4.  Create a PR and move on.

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
    -   **Quest types:** There are 4 quest types, kill n, survive n time, kill boss, defend location, deliver package
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
python3 -m pip install textual-dev
```
Then, run the game with the `--dev` flag:
```bash
./run_game.sh --dev
```
This will enable the Textual inspector, which can be accessed by pressing `Ctrl+B`.

Dev mode can also be toggled in Settings during gameplay. When enabled:
- **FPS Counter** is shown on the WorldScreen
- **Debug Console** is available (press `` ` `` backtick on the WorldScreen)
- **Quick Start** option becomes available in Settings

### Debug Console (`car/logic/debug_commands.py`, `car/widgets/debug_console.py`)

A dev-mode-only in-game command prompt, activated by pressing `` ` `` (backtick/grave accent) during gameplay. Commands are entered as text and results appear as notifications.

**Implementation:** The `DebugConsole` widget (Textual `Input`) is mounted/unmounted on `WorldScreen` when toggled. Commands are parsed and executed by `execute_command()` in `debug_commands.py`. All entities have auto-incrementing `entity_id` (assigned in `Entity.__init__`) for stable references.

**Available Commands:**

| Command | Example | Description |
|---------|---------|-------------|
| `spawn enemy <class> [dx dy]` | `spawn enemy raider_buggy 30 40` | Spawn enemy at player + offset |
| `spawn boss <faction_id>` | `spawn boss the_vultures` | Spawn faction boss |
| `spawn fauna <class> [dx dy]` | `spawn fauna dog` | Spawn fauna (default: 50 units ahead) |
| `spawn obstacle <class> [dx dy]` | `spawn obstacle rock 10 10` | Spawn obstacle |
| `kill <id>` | `kill 42` | Kill entity by ID |
| `kill all` | `kill all` | Kill all enemies |
| `tp <x> <y>` | `tp 1000 1000` | Teleport to world coordinates |
| `tp_rel <dx> <dy>` | `tp_rel 50 50` | Relative teleport |
| `god` | `god` | Toggle invulnerability |
| `heal` | `heal` | Full durability restore |
| `gas` | `gas` | Full gas refill |
| `cash <amount>` | `cash 5000` | Add cash |
| `xp <amount>` | `xp 1000` | Add XP |
| `level <n>` | `level 10` | Set player level |
| `speed <value>` | `speed 20` | Set car speed directly |
| `ammo <type> <n>` | `ammo bullet 100` | Set ammo count |
| `list enemies` | `list enemies` | Show enemies with IDs |
| `list factions` | `list factions` | Show factions |
| `list all` | `list all` | Entity count summary |
| `help` | `help` | Show available commands |

**Entity class names** are matched case-insensitively with underscore tolerance: `raider_buggy`, `RaiderBuggy`, and `raiderbuggy` all work.

### Dev Quick Start (`car/config.py`: `dev_quick_start`)

A setting (toggled in Settings screen) that skips all LLM generation for instant game start. When enabled, clicking "Start Game" in the New Game screen:
1. Uses hardcoded fallback theme ("Classic Wasteland")
2. Uses hardcoded fallback factions (5 factions including neutral hub at 0,0)
3. Uses hardcoded fallback quests and story intro
4. Skips ThemeSelectionScreen, WorldBuildingScreen, and IntroCutsceneScreen
5. Goes directly from NewGameScreen to WorldScreen

**Normal flow:** MainMenu → NewGame → ThemeSelection → WorldBuilding → IntroCutscene → WorldScreen
**Quick start:** MainMenu → NewGame → WorldScreen

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

- **Input System — Simultaneous Key Tracking:**
    - **Problem:** Textual's TUI framework provides no key-up events. Its `Binding` + `action_*` system dispatches one key at a time, so gameplay actions (turn, fire, accelerate) are mutually exclusive — the player can't hold turn while firing.
    - **Solution: `pressed_keys` with Staleness Expiry (`car/screens/world.py`):**
        1.  Gameplay keys (`WASD`, `Space`, `Left/Right arrows`) are **not** registered as Textual `Binding`s. Instead, a raw `on_key()` handler records each key event's timestamp into a `_pressed_keys: dict[str, float]` dictionary.
        2.  Every game tick, `process_input(dt)` is called before physics. It first **expires stale keys** — any key whose last event timestamp is older than `KEY_STALE_THRESHOLD` (150ms) is considered released. Since OS key-repeat fires every ~30-50ms while a key is held, a 150ms gap reliably indicates release.
        3.  The remaining held keys drive **continuous actions**: turning sets `actions["turn_left/right"]`, throttle ramps `pedal_position` at `PEDAL_RAMP_RATE` (4.0/s), firing sets `actions["fire"]`, and aiming adjusts `weapon_angle_offset` at `SWIVEL_RATE` (3.0 rad/s).
        4.  All gameplay keys are tracked independently, enabling true **simultaneous multi-key input** (e.g., turn + fire + accelerate at once).
    - **Menu keys** (`Escape`, `Tab`, `I`, `M`, `F`, `Q`, `Enter`) remain as standard one-shot Textual bindings since they don't need continuous input or simultaneity.
    - **Screen Transitions:** `_pressed_keys` is cleared on `on_mount()` and `on_screen_resume()` to prevent phantom inputs when returning from menus.
    - **Constants** (defined at module level in `car/screens/world.py`):
        - `KEY_STALE_THRESHOLD = 0.15` — seconds before an un-repeated key is treated as released
        - `PEDAL_RAMP_RATE = 4.0` — pedal units per second (0→1 in ~0.25s)
        - `SWIVEL_RATE = 3.0` — weapon aim radians per second
        - `GAMEPLAY_KEYS = {"w", "s", "a", "d", "space", "left", "right"}`

- **Coordinate System and Entity Physics:** To ensure consistent and predictable behavior for all in-game objects, the following conventions are strictly followed:
    - **Game World Orientation:** The game operates on a "North-is-Up" principle. An angle of `0` radians corresponds to North. This is in contrast to the standard mathematical convention where `0` radians is East. All physics and rendering calculations must account for this by subtracting `math.pi / 2` from the game angle before using it in standard trigonometric functions (`cos`, `sin`).
    - **Entity Bounding Box:** An entity's `width` and `height` are crucial for physics, rendering, and interaction. For entities with multiple directional sprites (like the player's car), the dimensions must be calculated to create a bounding box large enough to contain the widest and tallest sprites. This is handled by the `Entity.get_car_dimensions()` static method, which should be called in the entity's `__init__` method. For single-sprite entities, the dimensions are calculated directly from their art.
    - **Attachment Points and Particle Origins:** The visual location of a weapon on the car and the origin point of the particles it fires must be perfectly synchronized. Both are calculated using the same core logic:
        1.  Start with the entity's central world coordinates (`entity.x`, `entity.y`).
        2.  Define the attachment point as an `(x, y)` offset from this center.
        3.  Apply the entity's rotation to this offset using a standard 2D rotation matrix.
        4.  Add the rotated offset to the entity's central world coordinates.
    -   This ensures that the rendered position of the weapon and the logical origin of its projectiles are always identical, preventing visual disconnects. The `car/rendering/renderer.py` module is the source of truth for this calculation.


## Development Backlog

All pending features, bug fixes, and refactors are now managed as **GitHub Issues**. 

- **Current Backlog:** [GitHub Issues](https://github.com/MaStanford/LLMCarGame/issues)
- **Sync Tool:** Use `scripts/sync_tasks_to_github.py` to upload any new tasks added to this file (under an "Open Tasks" section) to the repository.

### Workflow reminder:
- Pick an issue from the GitHub list.
- Implement the solution.
- Verify the work.
- Create a PR referencing the issue (e.g., `Fixes #65`).
- Move to the next task.


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

- **Language:** (To be determined - e.g., Python, Go, Rust)
- **Engine:** Custom-built terminal game engine.
- **Renderer:** Curses library.

## Architecture

- **Game Loop & UI:**
    -   **Main Game Loop:** The core loop renders the world, including the environment, roads, buildings, and all entities.
    -   **Inventory Menu (Tab):** Pressing `Tab` opens a full-screen modal with a border.
        -   **Car Preview:** Displays the player's car, rotating through 8 directions.
        -   **Attachments:** A container lists attachment points, their type, and the equipped item. Arrow keys are used to navigate and select different weapons/items from inventory.
        -   **Inventory:** A container for stored items. Selecting an item opens a pop-up with actions (e.g., "Drop").
        -   **Stats:** A container shows current fuel, ammo, money, etc.
        -   Pressing `Tab` again closes the menu.
    -   **Pause Menu (Esc):** Pressing `Esc` opens a smaller modal with options: "Main Menu", "Save", "Load", and "Quit".
- **Game State Management:**
    - **Main Menu:** The game starts with a menu offering "New Game," "Load Game," and "Settings."
    - **New Game Flow:** After selecting "New Game," the player chooses a car and difficulty, then enters the main game loop.
    - **Load Game Flow:** After selecting "Load Game," the player chooses a save file from a list, which loads the state and enters the main game loop.
    - **Save/Load System:** A system for serializing and deserializing the entire game state (player, car, world seed, inventory, quests) to a file.
- **Progression System:**
    - **Experience & Leveling:** Players gain experience points (XP) for defeating enemies. Upon reaching a certain XP threshold, the player levels up, receiving minor positive modifiers to their stats.
    - **XP Curve:** The experience required to reach the next level doubles with each level gained.
    - **Difficulty Modifier:** The selected difficulty level applies a multiplier to enemy stats, such as damage and durability, making the game more or less challenging.
- **Rendering Engine:**
    - **Renderer:** Utilizes the `curses` library for all screen drawing.
    - **Entities:** All game objects (cars, weapons, buildings, etc.) are represented as entities. Each entity type is defined in a configuration file that specifies its properties.
    - **Visuals:** Each entity's file contains a method to retrieve its ASCII/Unicode representation. This method accepts a direction parameter (8 directions: N, NE, E, SE, S, SW, W, NW) to return the correct directional sprite.
    - **Composition:** The rendering system dynamically composes entities with their attachments. For example, a car entity will be rendered with its attached weapon entities, positioned correctly based on the car's current direction.
- **World Generation:** Procedural generation for terrain, roads, and cities.
- **Car Simulation:** Physics and state management for vehicle mechanics.
- **Inventory/Attachments:** System for managing car modifications.
- **AI:** Systems for controlling behavior of enemies, NPCs, and fauna.
- **Combat System:** Manages damage, experience, and loot drops.
- **Quest System:** Tracks player quests and objectives.
- **Economy:** Handles currency and transactions at shops.

## Tasks

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
- [ ] Implement advanced car customization.
- [ ] Implement the economy system.
- [x] Add pickable colors to player car.
- [x] Make entity unicode character have the same background color as the environment they are on.

## Roadmap

1.  **Main Menu:** Implement the initial screen with "New Game," "Load Game," and "Settings" options.
2.  **Save/Load:** Implement the ability to save and load game progress.
3.  **New Game Flow:**
    -   **Car Selection Screen:**
        -   Display a list of available starting cars with their stats.
        -   Show a preview of the selected car, rotating through all 8 directions.
    -   Prompt for player to select a difficulty level.
    -   Allow selection of initial weapons and special abilities (e.g., machine gun, nitrous boost).
    -   Transition to the main game loop.
4.  **Load Game Flow:**
    -   Display a list of saved game files.
    -   On selection, load the game state and transition to the main game loop.
5.  **Initial Game World & Core Gameplay:**
    -   Generate the starting area of the world and place the player.
    -   Implement driving, combat, progression, and resource management basics.
6.  **In-Game UI:**
    -   Develop the tab-based inventory and management menu.
    -   Develop the escape-key pause menu.
7.  **Content Expansion:**
    -   Add quests, NPCs, and fauna.
    -   Expand the variety of cars, weapons, and attachments.
    -   Flesh out the economy with more shops and items.
8.  **Visual Polish:**
    -   Allow the player to select their car's color.
    -   Improve the rendering of entities to blend with the environment.

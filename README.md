# Genesis Module - A Terminal-Based Automotive RPG

Welcome to Genesis Module, a terminal-based, open-world, automotive RPG survival game. Players select a starting vehicle and embark on an adventure in an infinitely-generated, random world. The map features roads connecting cities, surrounded by various types of wilderness.

## Key Gameplay Elements:

-   **Infinite World:** A randomly generated world provides endless exploration.
-   **Cities:** Procedurally generated with buildings like gas stations, mechanic shops, weapon shops, and a city hall for quests. Cities are populated with random NPCs.
-   **Wilderness:** The areas between cities are filled with randomly generated fauna (e.g., deer, dogs) and enemies (e.g., bandits, other hostile vehicles).
-   **Vehicles:** A diverse roster of cars is available, including sports cars, sedans, vans, trucks, monster trucks, motorcycles, hot rods, and SUVs.
-   **Customization:** Cars have attachment points for weapons, extra fuel tanks, or storage. Weapons are visually represented on the car and have 8-directional art.
-   **Combat & Progression:** Players gain experience and loot (money, damaged parts, ammo) by defeating enemies.
-   **Resource Management:**
    -   **Durability:** Damage accumulates from combat and collisions, repaired at mechanic shops.
    -   **Fuel:** Consumed while driving, refilled at gas stations.
    -   **Ammo:** Required for weapons, purchased at weapon shops.
    -   **Faction Warfare:** The wasteland is a dangerous place, dominated by rival factions.
    -   **Choose Your Allegiance:** The world is controlled by different factions. You can choose to align with one, or play them against each other.
    -   **Dynamic Reputation and Control:** Your actions have consequences. Completing quests for a faction will earn you their trust and increase their **Control** over their territory, making their shops better and their patrols stronger. Working against a faction will make you an enemy and decrease their Control, sowing chaos in their lands.
    -   **Territory Control:** As you shift the balance of power, the world will change. Help your allies take over enemy territory by completing a "Decisive Battle" quest, or become a feared outcast hunted by all.
-   **LLM-Powered Narrative:** The game's story is not pre-written. It uses a Large Language Model to generate a unique theme, set of factions, and quests for every single playthrough. See the "World Generation Modes" section for more details.
-   **Weapon Modifiers:** Weapons can have modifiers that affect their stats, such as damage, fire rate, and range. These can be found as loot or purchased from shops.

## How to Play

-   **Movement:** Use **WASD** to accelerate, brake, and steer your car.
-   **Fire Weapons:** Press the **Spacebar** to fire your equipped weapons.
-   **Inventory:** Press **Tab** to open your inventory and manage your car's attachments and items.
-   **Factions:** Press **F** to open the Faction Command screen and view the current state of the wasteland.
-   **Pause Menu:** Press **Esc** to open the pause menu, where you can save, load, or quit the game.

## World Generation Modes

The game features two modes for generating its dynamic narrative content. You can switch between them in the **Settings** menu.

### Local Mode (Default)
-   **How it works:** Uses a built-in, local LLM that runs on your computer's CPU.
-   **Pros:** Fully offline. After the initial setup, you can play anywhere without an internet connection.
-   **Cons:** World generation can be slow (several minutes) depending on your computer's hardware.

### Gemini CLI Mode (Recommended)
-   **How it works:** Uses the Google Gemini CLI, which runs in the cloud.
-   **Pros:** Extremely fast world and quest generation (usually under 30 seconds). Produces higher-quality, more creative narrative content.
-   **Cons:** Requires an active internet connection and a one-time setup of the Gemini CLI.

#### Setting up Gemini CLI Mode
1.  **Install the Gemini CLI:** Follow the official [installation instructions](https://ai.google.dev/tutorials/gemini_cli_quickstart).
2.  **Authenticate:** Run the following command and follow the on-screen instructions to log in with your Google account:
    ```bash
    gemini auth
    ```
3.  **Select the Mode:** Launch the game, go to **Settings**, and switch the Generation Mode to "Gemini CLI".

## Dependencies

-   **Python 3:** The game is written in Python 3.
-   **Textual:** The game uses the `Textual` library for rendering.

## Installation and Running the Game

**1. Install Dependencies**

First, install the necessary Python packages. The exact requirements vary by operating system.

*   **For Windows:**
    ```bash
    pip install -r requirements-windows.txt
    ```
*   **For macOS:**
    ```bash
    pip install -r requirements-macos.txt
    ```
*   **For Linux:**
    ```bash
    pip install -r requirements-linux.txt
    ```

**2. Download the Language Model (for Local Mode)**

If you plan to play in the offline "Local Mode", you need to download the model file.

Run the following command from the project's root directory:
```bash
python download_model.py
```
This will download the `gemma-2b-it.gguf` file (which is several gigabytes) and place it in the `models/` directory. You only need to do this once.

**3. Run the Game**

Once the dependencies are installed, you can run the game using the appropriate script for your system:

*   **On Windows:**
    ```bash
    run_game.bat
    ```
*   **On macOS and Linux:**
    ```bash
    chmod +x run_game.sh
    ./run_game.sh
    ```

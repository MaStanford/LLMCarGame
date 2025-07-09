# Car - A Terminal-Based Automotive RPG

Welcome to Car, a terminal-based, open-world, automotive RPG survival game. Players select a starting vehicle and embark on an adventure in an infinitely-generated, random world. The map features roads connecting cities, surrounded by various types of wilderness.

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
-   **Quests:** Accept quests from NPCs in cities to earn rewards.
-   **Boss Fights:** Battle powerful bosses with unique vehicles and abilities. Track them down using the compass and take them out to complete quests.

## How to Play

-   **Movement:** Use the **Arrow Keys** or **WASD** to accelerate, brake, and steer your car.
-   **Fire Weapons:** Press the **Spacebar** to fire your equipped weapons.
-   **Inventory:** Press **Tab** to open your inventory and manage your car's attachments and items.
-   **Pause Menu:** Press **Esc** to open the pause menu, where you can save, load, or quit the game.

## Dependencies

-   **Python 3:** The game is written in Python 3.
-   **curses:** The game uses the `curses` library for rendering. This is included with Python on Linux and macOS, but requires a separate installation on Windows.
-   **pygame:** The game uses the `pygame` library for audio.

## Installation and Running the Game

### Windows

1.  **Install Python 3:** If you don't have Python 3 installed, download and install it from the [official Python website](https://www.python.org/downloads/). Make sure to check the box that says "Add Python to PATH" during installation.
2.  **Install dependencies:** Open a command prompt and run the following command:
    ```
    pip install -r requirements.txt
    ```
3.  **Download SoundFont:** Download the `GeneralUser_GS_v1.471.sf2` SoundFont from [this link](https://www.schristiancollins.com/soundfonts.php) and place it in the `car/sounds` directory.
4.  **Run the game:** Open a command prompt, navigate to the project's root directory, and run the following command:
    ```
    run_game.bat
    ```

### macOS and Linux

1.  **Install Python 3:**
    *   **macOS:** If you don't have Python 3 installed, you can install it using [Homebrew](https://brew.sh/):
        ```
        brew install python
        ```
    *   **Linux:** Python 3 is usually pre-installed on most Linux distributions. If not, you can install it using your distribution's package manager. For example, on Debian-based distributions (like Ubuntu), you can run:
        ```
        sudo apt-get update
        sudo apt-get install python3 python3-pip
        ```
2.  **Install dependencies:** Open a terminal and run the following command:
    ```
    pip3 install -r requirements.txt
    ```
3.  **Download SoundFont:** Download the `GeneralUser_GS_v1.471.sf2` SoundFont from [this link](https://www.schristiancollins.com/soundfonts.php) and place it in the `car/sounds` directory.
4.  **Make the script executable:** Open a terminal, navigate to the project's root directory, and run the following command. You only need to do this once.
    ```
    chmod +x run_game.sh
    ```
5.  **Run the game:** Run the following command from the project's root directory:
    ```
    ./run_game.sh
    ```

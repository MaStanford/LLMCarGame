import json
from ..logic.data_loader import FACTION_DATA
from ..data.quests import Quest, KillBossObjective

CONQUEST_THRESHOLD = 20

def initialize_faction_control(game_state):
    """Sets the initial control values for all factions at the start of a new game."""
    for faction_id, faction_data in FACTION_DATA.items():
        game_state.faction_control[faction_id] = faction_data.get("control", 50)

def increase_control(game_state, faction_id, amount):
    """Increases the control of a specific faction."""
    if faction_id in game_state.faction_control:
        game_state.faction_control[faction_id] = min(100, game_state.faction_control[faction_id] + amount)

def decrease_control(game_state, faction_id, amount):
    """Decreases the control of a specific faction."""
    if faction_id in game_state.faction_control:
        game_state.faction_control[faction_id] = max(0, game_state.faction_control[faction_id] - amount)

def get_conquest_quest(game_state):
    """
    Checks if any faction is vulnerable to a takeover and returns a special
    'Decisive Battle' quest if conditions are met.
    """
    factions = game_state.factions
    vulnerable_factions = [
        fid for fid, control in game_state.faction_control.items()
        if control <= CONQUEST_THRESHOLD and fid in factions and factions[fid].get("faction_boss")
    ]

    if not vulnerable_factions:
        return None

    losing_faction_id = vulnerable_factions[0] # Target the first one for now
    losing_faction = factions[losing_faction_id]

    # Find the strongest rival to offer the quest
    potential_aggressors = [
        fid for fid, rel in losing_faction["relationships"].items() if rel == "Hostile"
    ]
    if not potential_aggressors:
        return None

    # Offer the quest to the hostile rival with the highest player reputation
    aggressor_faction_id = max(
        potential_aggressors,
        key=lambda fid: game_state.faction_reputation.get(fid, 0)
    )

    # Generate the special quest
    boss_name = losing_faction["faction_boss"]["name"]
    quest_name = f"Decisive Battle: End of the {losing_faction['name']}"
    quest_dialog = (
        f"The {losing_faction['name']} are on their last legs. Their leader, {boss_name}, "
        f"is all that's holding them together. Find them, crush them, and their territory "
        f"will be ours. This is our chance to expand our influence, once and for all."
    )

    return Quest(
        name=quest_name,
        description=f"Defeat {boss_name} to conquer the {losing_faction['name']}.",
        dialog=quest_dialog,
        objectives=[KillBossObjective(boss_name)],
        rewards={"xp": 2000, "cash": 5000},
        quest_giver_faction=aggressor_faction_id,
        target_faction=losing_faction_id,
        is_conquest_quest=True
    )

def handle_faction_takeover(game_state, winning_faction_id, losing_faction_id):
    """
    Handles the permanent world state changes after a successful conquest.
    This directly modifies the in-memory factions dictionary on game_state.
    """
    factions = game_state.factions
    winner = factions[winning_faction_id]
    loser = factions[losing_faction_id]

    game_state.notifications.append(f"{loser['name']} has been defeated!")
    game_state.notifications.append(f"Their territory is now controlled by the {winner['name']}!")

    # Log to story journal (before modifying names)
    game_state.story_events.append({
        "text": f"The {loser['name']} has fallen. Their territory is now controlled by the {winner['name']}.",
        "event_type": "faction_takeover",
    })

    # 1. Update the defeated faction's data
    loser["name"] = f"{loser['name']} (Conquered)"
    loser["units"] = winner["units"] # They now use the victor's units
    loser["faction_boss"] = None # The boss is gone

    # 2. Update all other factions' relationships to the loser
    for faction_id in factions:
        if faction_id != losing_faction_id:
            factions[faction_id]["relationships"][losing_faction_id] = "Defeated"

    # 3. The loser's relationships are now null and void
    loser["relationships"] = {fid: "Defeated" for fid in factions if fid != losing_faction_id}

    # 4. Remove the defeated faction from active reputation and control tracking
    if losing_faction_id in game_state.faction_reputation:
        del game_state.faction_reputation[losing_faction_id]
    if losing_faction_id in game_state.faction_control:
        del game_state.faction_control[losing_faction_id]

    # 5. Give the victor a massive control boost
    increase_control(game_state, winning_faction_id, 50)
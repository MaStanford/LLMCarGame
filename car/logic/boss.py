import random
from ..entities.vehicle import Vehicle
from ..logic.data_loader import FACTION_DATA
from ..logic.entity_loader import PLAYER_CARS
from ..data.quests import Quest, KillBossObjective
from ..logic.quest_logic import check_for_faction_takeover
from ..entities.vehicles.war_rig import WarRig
from ..entities.vehicles.armored_truck import ArmoredTruck
from ..entities.vehicles.miner import Miner
from ..entities.vehicles.hotrod import Hotrod
from ..entities.vehicles.truck import Truck

def check_challenge_conditions(game_state, faction_id, factions_data):
    """
    Checks if the player can challenge a faction's boss.
    Returns True if conditions are met, False otherwise.
    """
    if not factions_data[faction_id].get("faction_boss"):
        return False

    rep = game_state.faction_reputation.get(faction_id, 0)
    if rep <= -100:
        return True

    hostile_factions = [fid for fid, rel in factions_data[faction_id]["relationships"].items() if rel == "Hostile"]
    for h_id in hostile_factions:
        if game_state.faction_reputation.get(h_id, 0) >= 80:
            return True
            
    return False

def spawn_faction_boss(game_state, faction_id):
    """Spawns a faction boss and creates a quest to defeat them."""
    faction_data = game_state.factions.get(faction_id)
    if not faction_data or not faction_data.get("faction_boss"):
        return
    boss_data = faction_data["faction_boss"]

    # Create the boss entity from a standard vehicle class
    boss_car_class = next((c for c in PLAYER_CARS if c.__name__.lower() == boss_data["vehicle"].lower().replace(" ", "_")), None)
    if not boss_car_class: return

    # Position the boss near the faction's hub city
    hub_x, hub_y = faction_data["hub_city_coordinates"]
    boss_x = hub_x + random.uniform(-50, 50)
    boss_y = hub_y + random.uniform(-50, 50)

    boss_entity = boss_car_class(boss_x, boss_y)

    # Apply stat multipliers and unique properties
    boss_entity.name = boss_data["name"]
    boss_entity.durability *= boss_data["hp_multiplier"]
    boss_entity.max_durability = boss_entity.durability
    boss_entity.is_faction_boss = True

    # Apply "Enraged" stat boost if challenged early
    if game_state.faction_reputation.get(faction_id, 0) > -100:
        boss_entity.durability *= 1.5
        boss_entity.max_durability = boss_entity.durability
        boss_entity.name = f"Enraged {boss_entity.name}"

    game_state.active_enemies.append(boss_entity)

    # Create and set the quest
    quest_name = f"Defeat {boss_entity.name}"
    quest_description = f"You have challenged the leader of the {faction_data['name']}. Defeat them to claim victory."
    objectives = [KillBossObjective(boss_entity.name)]
    rewards = {
        "xp": 5000,
        "cash": 2000,
        "rep_gain": {fid: 25 for fid, rel in faction_data["relationships"].items() if rel == "Hostile"},
        "rep_loss": {fid: -40 for fid, rel in faction_data["relationships"].items() if rel == "Allied"}
    }

    new_quest = Quest(
        name=quest_name,
        description=quest_description,
        objectives=objectives,
        rewards=rewards,
        requires_turn_in=False # Completes on boss defeat
    )
    new_quest.boss_name = boss_entity.name # Link boss to quest
    game_state.current_quest = new_quest

def handle_faction_boss_defeat(game_state, boss_entity):
    """Handles the consequences of defeating a faction boss."""
    if not getattr(boss_entity, "is_faction_boss", False):
        return

    defeated_faction_id = None
    for fid, data in game_state.factions.items():
        if data.get("faction_boss") and data["faction_boss"]["name"] == boss_entity.name.replace("Enraged ", ""):
            defeated_faction_id = fid
            break

    if defeated_faction_id:
        faction_name = game_state.factions[defeated_faction_id]["name"]
        game_state.story_events.append({
            "text": f"Defeated {boss_entity.name}, leader of the {faction_name}.",
            "event_type": "boss_defeated",
        })
        game_state.defeated_bosses.add(defeated_faction_id)
        check_for_faction_takeover(game_state)

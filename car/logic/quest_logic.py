import random
from ..data.quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective, QUEST_TEMPLATES
from ..logic.entity_loader import PLAYER_CARS
from ..entities.base import Entity
from .boss import Boss
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city, get_city_faction
from ..data.factions import FACTION_DATA

def get_available_quests(game_state):
    """Generates a list of available quests for the current city."""
    quests = []
    quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
    quest_giver_faction = FACTION_DATA[quest_giver_faction_id]
    
    hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
    if not hostile_factions:
        return []

    # Generate 3 quests
    for _ in range(3):
        target_faction_id = random.choice(hostile_factions)
        target_faction = FACTION_DATA[target_faction_id]

        quest_template_key = random.choice(list(QUEST_TEMPLATES.keys()))
        quest_template = QUEST_TEMPLATES[quest_template_key]

        objectives = []
        for obj_class, args in quest_template["objectives"]:
            objectives.append(obj_class(*args))

        name = quest_template["name"].format(target_faction_name=target_faction["name"])
        description = quest_template["description"].format(
            quest_giver_faction_name=quest_giver_faction["name"],
            target_faction_name=target_faction["name"]
        )

        quests.append(Quest(
            name=name,
            description=description,
            objectives=objectives,
            rewards=quest_template["rewards"],
            city_id=(round(game_state.car_world_x / CITY_SPACING), round(game_state.car_world_y / CITY_SPACING)),
            quest_giver_faction=quest_giver_faction_id,
            target_faction=target_faction_id,
            time_limit=quest_template.get("time_limit")
        ))
    return quests

def handle_quest_acceptance(game_state, quest):
    """Handles the logic for accepting a quest."""
    game_state.current_quest = quest
    
    # Check if the quest has a boss and spawn it
    quest_template_key = next((k for k, v in QUEST_TEMPLATES.items() if v["name"] == quest.name.split(" ")[0]), None)
    if quest_template_key:
        quest_template = QUEST_TEMPLATES[quest_template_key]
        if "boss" in quest_template:
            boss_data = quest_template["boss"]
            target_faction = FACTION_DATA[quest.target_faction]
            boss_name = boss_data["name"].format(target_faction_name=target_faction["name"])
            boss_car_class = next((c for c in PLAYER_CARS if c.__name__.lower() == boss_data["car"].lower().replace(" ", "_")), None)
            if boss_car_class:
                boss_car_instance = boss_car_class(0, 0)
                boss = Boss(boss_name, boss_car_instance, boss_data["hp_multiplier"])
                boss.x = game_state.car_world_x + random.uniform(-200, 200)
                boss.y = game_state.car_world_y + random.uniform(-200, 200)
                boss.hp = boss_car_instance.durability * boss.hp_multiplier
                boss.art = boss_car_instance.art
                boss.width, boss.height = Entity.get_car_dimensions(boss.art)
                game_state.active_bosses.append(boss)
                game_state.current_quest.boss = boss # Link boss to quest
                # audio_manager.stop_music()
                # audio_manager.play_music("car/sounds/boss.mid")

def update_quests(game_state, audio_manager):
    """
    Updates the state of the current quest.
    Returns a list of notification messages.
    """
    notifications = []
    if game_state.current_quest:
        if not game_state.current_quest.ready_to_turn_in:
            game_state.current_quest.update(game_state)

        if game_state.current_quest.completed and not game_state.current_quest.ready_to_turn_in:
            if game_state.current_quest.requires_turn_in:
                game_state.current_quest.ready_to_turn_in = True
                notifications.append(f"Objective complete! Return to {get_city_name(*game_state.current_quest.city_id)}.")
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")
            else:
                # For quests that complete immediately without turn-in
                complete_quest(game_state)
                notifications.append(f"Quest Complete: {game_state.current_quest.name}")
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")

        elif game_state.current_quest.failed:
            giver_faction_id = game_state.current_quest.quest_giver_faction
            if giver_faction_id:
                if giver_faction_id not in game_state.faction_reputation:
                    game_state.faction_reputation[giver_faction_id] = 0
                game_state.faction_reputation[giver_faction_id] -= 5
                notifications.append(f"Reputation with {FACTION_DATA[giver_faction_id]['name']} decreased.")
            
            notifications.append(f"Quest Failed: {game_state.current_quest.name}")
            game_state.current_quest = None
            audio_manager.stop_music()
            audio_manager.play_music("car/sounds/world.mid")
    return notifications

def check_for_faction_takeover(game_state):
    """
    Checks if a faction's reputation has dropped low enough to be taken over.
    Returns a list of notification messages.
    """
    notifications = []
    for faction_id, rep in list(game_state.faction_reputation.items()):
        if rep <= -100: # Takeover threshold
            # Find the faction with the highest reputation
            player_allies = [f_id for f_id, r in game_state.faction_reputation.items() if r > 0]
            if not player_allies:
                continue # No one to take over

            strongest_ally = max(player_allies, key=lambda f_id: game_state.faction_reputation[f_id])
            
            # Update faction data
            defeated_faction_name = FACTION_DATA[faction_id]["name"]
            victor_faction_name = FACTION_DATA[strongest_ally]["name"]
            
            notifications.append(f"{defeated_faction_name} has been defeated! Their territory is now controlled by {victor_faction_name}!")
            
            # Transfer control of the hub city
            FACTION_DATA[faction_id]["name"] = f"{victor_faction_name} (Occupied)"
            FACTION_DATA[faction_id]["units"] = FACTION_DATA[strongest_ally]["units"]
            
            # Update relationships
            for f_id in FACTION_DATA:
                if f_id != faction_id:
                    FACTION_DATA[f_id]["relationships"][faction_id] = "Defeated"
            
            del game_state.faction_reputation[faction_id]
    return notifications

def generate_quest(game_state, quest_id):
    """Generates a single Quest object from a given template ID."""
    quest_template = QUEST_TEMPLATES.get(quest_id)
    if not quest_template:
        return None

    # Faction logic mirrors get_available_quests
    quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
    quest_giver_faction = FACTION_DATA[quest_giver_faction_id]
    hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
    if not hostile_factions:
        return None # Can't generate a quest without a target
    target_faction_id = random.choice(hostile_factions)
    target_faction = FACTION_DATA[target_faction_id]

    objectives = []
    for obj_class, args in quest_template["objectives"]:
        objectives.append(obj_class(*args))

    name = quest_template["name"].format(target_faction_name=target_faction["name"])
    description = quest_template["description"].format(
        quest_giver_faction_name=quest_giver_faction["name"],
        target_faction_name=target_faction["name"]
    )

    return Quest(
        name=name,
        description=description,
        objectives=objectives,
        rewards=quest_template["rewards"],
        city_id=(round(game_state.car_world_x / CITY_SPACING), round(game_state.car_world_y / CITY_SPACING)),
        quest_giver_faction=quest_giver_faction_id,
        target_faction=target_faction_id,
        time_limit=quest_template.get("time_limit"),
        next_quest_id=quest_template.get("next_quest_id")
    )

def complete_quest(game_state):
    """
    Handles the logic for completing a quest.
    If the quest is part of a chain, it sets up the next quest.
    Otherwise, it clears the current quest.
    """
    quest = game_state.current_quest
    if not quest:
        return

    # Grant rewards
    rewards = quest.rewards
    game_state.gain_xp(rewards.get("xp", 0))
    game_state.player_cash += rewards.get("cash", 0)
    
    # Update reputation
    giver_faction_id = quest.quest_giver_faction
    if giver_faction_id:
        game_state.faction_reputation[giver_faction_id] = game_state.faction_reputation.get(giver_faction_id, 0) + 10
    target_faction_id = quest.target_faction
    if target_faction_id:
        game_state.faction_reputation[target_faction_id] = game_state.faction_reputation.get(target_faction_id, 0) - 15

    # Check for next quest in the chain
    if quest.next_quest_id:
        game_state.current_quest = generate_quest(game_state, quest.next_quest_id)
    else:
        game_state.current_quest = None
    
    check_for_faction_takeover(game_state)


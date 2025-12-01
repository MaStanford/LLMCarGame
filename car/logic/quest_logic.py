import random
from ..data.quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective, DeliverPackageObjective, DefendLocationObjective, QUEST_TEMPLATES
from ..logic.entity_loader import PLAYER_CARS
from ..entities.base import Entity
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city, get_city_faction
from ..logic.data_loader import FACTION_DATA
from . import faction_logic

def get_available_quests(game_state):
    """Generates a list of available quests for the current city."""
    quests = []
    quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y, game_state.factions)
    quest_giver_faction = game_state.factions[quest_giver_faction_id]
    
    hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
    if not hostile_factions:
        return []

    # Generate 3 quests
    for _ in range(3):
        target_faction_id = random.choice(hostile_factions)
        target_faction = game_state.factions[target_faction_id]

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
            target_faction = game_state.factions[quest.target_faction]
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

from ..screens.quest_complete import QuestCompleteScreen
from .quest_caching import trigger_quest_prefetching

def update_quests(game_state, audio_manager, app):
    """
    Updates the state of the current quest.
    Returns a list of notification messages.
    """
    notifications = []
    if game_state.current_quest:
        # --- Handle Package Delivery Objective ---
        for objective in game_state.current_quest.objectives:
            if isinstance(objective, DeliverPackageObjective):
                # Check if the player is in any city
                grid_x = round(game_state.car_world_x / CITY_SPACING)
                grid_y = round(game_state.car_world_y / CITY_SPACING)
                city_key = f"{grid_x},{grid_y}"
                
                if city_key in game_state.world_details.get("cities", {}):
                    city_name = game_state.world_details["cities"][city_key]
                    if city_name == objective.destination:
                        # Check if player is physically in the city bounds
                        half_city = CITY_SPACING / 2
                        city_world_x = grid_x * CITY_SPACING
                        city_world_y = grid_y * CITY_SPACING
                        if (abs(game_state.car_world_x - city_world_x) < half_city and
                            abs(game_state.car_world_y - city_world_y) < half_city):
                            objective.completed = True
                            notifications.append(f"Package delivered to {city_name}!")
            elif isinstance(objective, DefendLocationObjective):
                # Find the location coordinates from world_details
                location_coords = None
                for landmark in game_state.world_details.get("landmarks", []):
                    if landmark["name"] == objective.location:
                        location_coords = (landmark["x"], landmark["y"])
                        break
                
                if location_coords:
                    # Check if player is near the location
                    player_x = game_state.car_world_x
                    player_y = game_state.car_world_y
                    dist_sq = (player_x - location_coords[0])**2 + (player_y - location_coords[1])**2
                    
                    # Define a radius for the defense area (e.g., 50 units)
                    defense_radius_sq = 50**2
                    
                    if dist_sq <= defense_radius_sq:
                        if objective.timer > 0:
                            objective.timer -= 1
                            if objective.timer % 30 == 0: # Notify every second
                                notifications.append(f"Defending {objective.location}... {objective.timer // 30}s remaining.")
                        else:
                            objective.completed = True
                            notifications.append(f"Successfully defended {objective.location}!")
                    else:
                        notifications.append(f"Return to {objective.location} to defend it!")
        
        if not game_state.current_quest.ready_to_turn_in:
            game_state.current_quest.update(game_state)

        if game_state.current_quest.completed and not game_state.current_quest.ready_to_turn_in:
            if game_state.current_quest.requires_turn_in:
                game_state.current_quest.ready_to_turn_in = True
                notifications.append(f"Objective complete! Return to city.")
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")
                trigger_quest_prefetching(app) # Trigger pre-fetching
            else:
                # For quests that complete immediately without turn-in
                app.push_screen(QuestCompleteScreen(game_state.current_quest))
                complete_quest(game_state, app)
                audio_manager.stop_music()
                audio_manager.play_music("car/sounds/world.mid")

        elif game_state.current_quest.failed:
            giver_faction_id = game_state.current_quest.quest_giver_faction
            if giver_faction_id:
                if giver_faction_id not in game_state.faction_reputation:
                    game_state.faction_reputation[giver_faction_id] = 0
                game_state.faction_reputation[giver_faction_id] -= 5
                faction_logic.decrease_control(game_state, giver_faction_id, 2) # Control penalty for failure
                notifications.append(f"Reputation with {game_state.factions[giver_faction_id]['name']} decreased.")
            
            notifications.append(f"Quest Failed: {game_state.current_quest.name}")
            game_state.current_quest = None
            audio_manager.stop_music()
            audio_manager.play_music("car/sounds/world.mid")
    return notifications

def check_for_faction_takeover(game_state):
    """
    Checks if a faction's reputation and boss status allow for a takeover.
    Returns a list of notification messages.
    """
    notifications = []
    for faction_id, rep in list(game_state.faction_reputation.items()):
        if rep <= -100 and faction_id in game_state.defeated_bosses:
            # Find the faction with the highest reputation
            player_allies = [f_id for f_id, r in game_state.faction_reputation.items() if r > 0]
            if not player_allies:
                continue # No one to take over

            strongest_ally = max(player_allies, key=lambda f_id: game_state.faction_reputation[f_id])
            
            # Update faction data
            defeated_faction_name = game_state.factions[faction_id]["name"]
            victor_faction_name = game_state.factions[strongest_ally]["name"]
            
            notifications.append(f"{defeated_faction_name} has been defeated! Their territory is now controlled by {victor_faction_name}!")
            
            # Transfer control of the hub city
            game_state.factions[faction_id]["name"] = f"{victor_faction_name} (Occupied)"
            game_state.factions[faction_id]["units"] = game_state.factions[strongest_ally]["units"]
            
            # Update relationships
            for f_id in game_state.factions:
                if f_id != faction_id:
                    game_state.factions[f_id]["relationships"][faction_id] = "Defeated"
            
            del game_state.faction_reputation[faction_id]
    return notifications

def generate_quest(game_state, quest_id):
    """Generates a single Quest object from a given template ID."""
    quest_template = QUEST_TEMPLATES.get(quest_id)
    if not quest_template:
        return None

    # Faction logic mirrors get_available_quests
    quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y, game_state.factions)
    quest_giver_faction = game_state.factions[quest_giver_faction_id]
    hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
    if not hostile_factions:
        return None # Can't generate a quest without a target
    target_faction_id = random.choice(hostile_factions)
    target_faction = game_state.factions[target_faction_id]

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

import json
import os

def complete_quest(game_state, app):
    """
    Handles the logic for completing a quest.
    If the quest is part of a chain, it sets up the next quest.
    Otherwise, it clears the current quest.
    """
    quest = game_state.current_quest
    if not quest:
        return

    # --- Log the completed quest for the narrative engine ---
    quest_log_path = "temp/quest_log.json"
    try:
        with open(quest_log_path, "r+") as f:
            log = json.load(f)
            log.append(quest.to_dict())
            f.seek(0)
            json.dump(log, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(quest_log_path, "w") as f:
            json.dump([quest.to_dict()], f, indent=4)

    # --- Handle Conquest ---
    if quest.is_conquest_quest:
        faction_logic.handle_faction_takeover(
            game_state, quest.quest_giver_faction, quest.target_faction
        )

    # Grant rewards
    rewards = quest.rewards
    game_state.gain_xp(rewards.get("xp", 0))
    game_state.player_cash += rewards.get("cash", 0)
    
    # Update reputation
    giver_faction_id = quest.quest_giver_faction
    if giver_faction_id:
        game_state.faction_reputation[giver_faction_id] = game_state.faction_reputation.get(giver_faction_id, 0) + 10
        faction_logic.increase_control(game_state, giver_faction_id, 5)
    target_faction_id = quest.target_faction
    if target_faction_id:
        game_state.faction_reputation[target_faction_id] = game_state.faction_reputation.get(target_faction_id, 0) - 15
        faction_logic.decrease_control(game_state, target_faction_id, 5)

    # Check for next quest in the chain
    if quest.next_quest_id:
        game_state.current_quest = generate_quest(game_state, quest.next_quest_id)
    else:
        game_state.current_quest = None
    
    check_for_faction_takeover(game_state)
    
    # Trigger pre-fetching for the next set of quests
    trigger_quest_prefetching(app)


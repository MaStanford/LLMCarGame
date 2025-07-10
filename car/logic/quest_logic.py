import random
from .quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective, QUESTS
from ..logic.entity_loader import PLAYER_CARS
from ..common.utils import get_car_dimensions
from .boss import Boss
from ..ui.notifications import add_notification
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city, get_city_faction

import random
from .quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective, QUEST_TEMPLATES
from ..logic.entity_loader import PLAYER_CARS
from ..common.utils import get_car_dimensions
from .boss import Boss
from ..ui.notifications import add_notification
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city, get_city_faction
from ..data.factions import FACTION_DATA

def handle_quest_interaction(game_state, world, audio_manager):
    """Handles the player's interaction with quest givers (City Hall)."""
    if not game_state.current_quest:
        grid_x = round(game_state.car_world_x / CITY_SPACING)
        grid_y = round(game_state.car_world_y / CITY_SPACING)
        city_buildings = get_buildings_in_city(grid_x, grid_y)

        for building in city_buildings:
            if building['x'] <= game_state.car_world_x < building['x'] + building['w'] and \
               building['y'] <= game_state.car_world_y < building['y'] + building['h']:
                if building["type"] == "city_hall":
                    quest_giver_faction_id = get_city_faction(game_state.car_world_x, game_state.car_world_y)
                    quest_giver_faction = FACTION_DATA[quest_giver_faction_id]
                    
                    hostile_factions = [fid for fid, rel in quest_giver_faction["relationships"].items() if rel == "Hostile"]
                    if not hostile_factions:
                        add_notification("No available quests at this time.", "warning")
                        return False

                    target_faction_id = random.choice(hostile_factions)
                    target_faction = FACTION_DATA[target_faction_id]

                    quest_template_key = random.choice(list(QUEST_TEMPLATES.keys()))
                    quest_template = QUEST_TEMPLATES[quest_template_key]

                    objectives = []
                    for obj_class, args in quest_template["objectives"]:
                        objectives.append(obj_class(*args))

                    # Format dynamic strings
                    name = quest_template["name"].format(target_faction_name=target_faction["name"])
                    description = quest_template["description"].format(
                        quest_giver_faction_name=quest_giver_faction["name"],
                        target_faction_name=target_faction["name"]
                    )

                    game_state.current_quest = Quest(
                        name=name,
                        description=description,
                        objectives=objectives,
                        rewards=quest_template["rewards"],
                        city_id=building["city_id"],
                        quest_giver_faction=quest_giver_faction_id,
                        target_faction=target_faction_id,
                        time_limit=quest_template.get("time_limit")
                    )
                    add_notification(f"New Quest: {game_state.current_quest.name}", "success")

                    if "boss" in quest_template:
                        boss_data = quest_template["boss"]
                        boss_name = boss_data["name"].format(target_faction_name=target_faction["name"])
                        boss_car_class = next((c for c in PLAYER_CARS if c.__name__.lower() == boss_data["car"].lower().replace(" ", "_")), None)
                        if boss_car_class:
                            boss_car_instance = boss_car_class(0, 0)
                            boss = Boss(boss_name, boss_car_instance, boss_data["hp_multiplier"])
                            boss.x = game_state.car_world_x + random.uniform(-200, 200)
                            boss.y = game_state.car_world_y + random.uniform(-200, 200)
                            boss.hp = boss_car_instance.durability * boss.hp_multiplier
                            boss.art = boss_car_instance.art
                            boss.width, boss.height = get_car_dimensions(boss.art)
                            game_state.active_bosses[quest_template_key] = boss
                            audio_manager.stop_music()
                            audio_manager.play_music("car/sounds/boss.mid")
                    return True
    else:
        add_notification("You already have an active quest.", "warning")
    return False

def update_quests(game_state, audio_manager):
    """Updates the state of the current quest."""
    if game_state.current_quest:
        game_state.current_quest.update(game_state)

        if game_state.current_quest.completed:
            rewards = game_state.current_quest.rewards
            game_state.gain_xp(rewards.get("xp", 0))
            game_state.player_cash += rewards.get("cash", 0)
            
            # Increase reputation with quest giver
            giver_faction_id = game_state.current_quest.quest_giver_faction
            if giver_faction_id:
                if giver_faction_id not in game_state.faction_reputation:
                    game_state.faction_reputation[giver_faction_id] = 0
                game_state.faction_reputation[giver_faction_id] += 10
                add_notification(f"Reputation with {FACTION_DATA[giver_faction_id]['name']} increased!", "success")

            # Decrease reputation with target
            target_faction_id = game_state.current_quest.target_faction
            if target_faction_id:
                if target_faction_id not in game_state.faction_reputation:
                    game_state.faction_reputation[target_faction_id] = 0
                game_state.faction_reputation[target_faction_id] -= 15
                add_notification(f"Reputation with {FACTION_DATA[target_faction_id]['name']} decreased!", "warning")

            add_notification(f"Quest Complete: {game_state.current_quest.name}", "success")
            game_state.current_quest = None
            audio_manager.stop_music()
            audio_manager.play_music("car/sounds/world.mid")

        elif game_state.current_quest.failed:
            giver_faction_id = game_state.current_quest.quest_giver_faction
            if giver_faction_id:
                if giver_faction_id not in game_state.faction_reputation:
                    game_state.faction_reputation[giver_faction_id] = 0
                game_state.faction_reputation[giver_faction_id] -= 5
                add_notification(f"Reputation with {FACTION_DATA[giver_faction_id]['name']} decreased.", "warning")
            
            add_notification(f"Quest Failed: {game_state.current_quest.name}", "error")
            game_state.current_quest = None
            audio_manager.stop_music()
            audio_manager.play_music("car/sounds/world.mid")

import random
from .quests import Quest, KillBossObjective, KillCountObjective, SurvivalObjective, QUESTS
from ..data.cars import CARS_DATA
from ..common.utils import get_car_dimensions
from .boss import Boss
from ..ui.notifications import add_notification
from ..data.game_constants import CITY_SPACING
from ..world.generation import get_buildings_in_city

def handle_quest_interaction(game_state, world, audio_manager):
    """Handles the player's interaction with quest givers (City Hall)."""
    if not game_state.current_quest:
        grid_x = round(game_state.car_world_x / CITY_SPACING)
        grid_y = round(game_state.car_world_y / CITY_SPACING)
        city_buildings = get_buildings_in_city(grid_x, grid_y)

        for building in city_buildings:
            if building['x'] <= game_state.car_world_x < building['x'] + building['w'] and \
               building['y'] <= game_state.car_world_y < building['y'] + building['h']:
                if building["type"] == "GENERIC" and building["name"] == "City Hall":
                    quest_key = random.choice(list(QUESTS.keys()))
                    quest_data = QUESTS[quest_key]
                    
                    objectives = []
                    for obj_class, args in quest_data["objectives"]:
                        objectives.append(obj_class(*args))

                    game_state.current_quest = Quest(
                        name=quest_data["name"],
                        description=quest_data["description"],
                        objectives=objectives,
                        rewards=quest_data["rewards"]
                    )
                    add_notification(f"New Quest: {game_state.current_quest.name}", color="MENU_HIGHLIGHT")

                    if "boss" in quest_data:
                        boss_data = quest_data["boss"]
                        boss_car_data = next((c for c in CARS_DATA if c["name"] == boss_data["car"]), None)
                        if boss_car_data:
                            boss = Boss(boss_data["name"], boss_car_data, boss_data["hp_multiplier"])
                            boss.x = game_state.car_world_x + random.uniform(-200, 200)
                            boss.y = game_state.car_world_y + random.uniform(-200, 200)
                            boss.hp = boss_car_data["durability"] * boss.hp_multiplier
                            boss.art = boss_car_data["art"]
                            boss.width, boss.height = get_car_dimensions(boss.art)
                            game_state.active_bosses[quest_key] = boss
                            audio_manager.stop_music()
                            audio_manager.play_music("car/sounds/boss.mid")
                    return True # Quest accepted
    else:
        add_notification("You already have an active quest.", color="UI_LOCATION")
    return False

def update_quests(game_state, audio_manager):
    """Updates the state of the current quest."""
    if game_state.current_quest:
        game_state_for_quest = {
            "active_bosses": game_state.active_bosses,
            "active_enemies": game_state.active_enemies,
        }
        game_state.current_quest.update(game_state_for_quest)

        if game_state.current_quest.completed:
            rewards = game_state.current_quest.rewards
            game_state.gain_xp(rewards.get("xp", 0))
            game_state.player_cash += rewards.get("cash", 0)
            add_notification(f"Quest Complete: {game_state.current_quest.name}", color="MENU_HIGHLIGHT")
            from ..ui.cutscene import play_cutscene
            # This is a temporary solution, we should have a better way to do this
            # play_cutscene(stdscr, [[f"Quest Complete!"]], 1)
            game_state.current_quest = None
            audio_manager.stop_music()
            audio_manager.play_music("car/sounds/world.mid")

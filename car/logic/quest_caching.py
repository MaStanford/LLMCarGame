import logging
from functools import partial
from ..data.game_constants import CITY_SPACING

def trigger_quest_prefetching(app):
    """
    Identifies nearby cities and launches background workers to pre-fetch quests
    for them if they aren't already cached.
    """
    gs = app.game_state
    if not gs or not app.llm_pipeline:
        return

    # 1. Identify nearby cities
    player_grid_x = round(gs.car_world_x / CITY_SPACING)
    player_grid_y = round(gs.car_world_y / CITY_SPACING)
    
    # Simple logic: check a 3x3 grid around the player
    nearby_cities = []
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            # For now, we'll just use the faction ID as the city ID
            # In the future, this could be a more complex object
            city_id = f"faction_at_{player_grid_x + dx}_{player_grid_y + dy}"
            nearby_cities.append(city_id)

    # 2. Launch workers for uncached cities
    for city_id in nearby_cities:
        if city_id not in gs.quest_cache:
            logging.info(f"No quests cached for nearby city {city_id}. Starting pre-fetch worker.")
            
            # Set a placeholder to prevent re-launching the worker
            gs.quest_cache[city_id] = "pending"
            
            from ..workers.quest_generator import generate_quests_worker
            worker_callable = partial(
                generate_quests_worker,
                app.llm_pipeline,
                gs,
                city_id,
                3  # Number of quests to generate
            )
            
            # The callback will update the cache with the real quest data
            app.run_worker(
                worker_callable,
                exclusive=False, # Allow multiple quest workers to run
                thread=True,
                name=f"QuestGenerator_{city_id}",
                callback=partial(on_quest_prefetch_complete, city_id=city_id)
            )

def on_quest_prefetch_complete(worker_result, city_id: str, app):
    """
    Callback function executed on the main thread when the quest worker is done.
    """
    gs = app.game_state
    if not gs:
        return
        
    quests = worker_result
    if quests:
        logging.info(f"Successfully pre-fetched {len(quests)} quests for city {city_id}.")
        gs.quest_cache[city_id] = quests
    else:
        logging.warning(f"Quest pre-fetching failed for city {city_id}. Removing from cache.")
        # If it failed, remove the placeholder so we can try again later
        if city_id in gs.quest_cache:
            del gs.quest_cache[city_id]

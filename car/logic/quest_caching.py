import logging


def trigger_quest_prefetching(app):
    """
    Identifies nearby cities and launches background workers to pre-fetch quests
    for them if they aren't already cached.

    Delegates to the app's existing quest caching implementation which correctly
    handles both local and gemini_cli generation modes.
    """
    gs = app.game_state
    if not gs:
        return

    # The app already has a robust quest caching system that handles
    # faction detection, worker management, and result callbacks.
    app.check_and_cache_quests_for_nearby_cities()

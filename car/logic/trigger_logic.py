from ..widgets.notifications import Notifications

def check_triggers(app, game_state):
    """Checks if the player has entered a world trigger zone."""
    for trigger in game_state.world_triggers:
        trigger_id = trigger.get("id")
        if trigger_id in game_state.triggered_triggers and trigger.get("one_shot", False):
            continue

        dist_sq = (trigger["x"] - game_state.car_world_x)**2 + (trigger["y"] - game_state.car_world_y)**2
        if dist_sq < trigger["radius"]**2:
            # Player is inside the trigger radius
            if trigger_id not in game_state.triggered_triggers:
                game_state.triggered_triggers.add(trigger_id)
                if trigger["type"] == "dialog":
                    app.screen.query_one("#notifications", Notifications).add_notification(trigger["data"])
                # TODO: Implement other trigger types (combat, quest)
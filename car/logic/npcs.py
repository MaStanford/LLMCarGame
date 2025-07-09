from ..ui.cutscene import draw_cutscene_modal

def handle_npc_interaction(stdscr, npc, color_map):
    """Handles NPC interaction."""
    if npc["type"] == "quest_giver":
        draw_cutscene_modal(stdscr, "Quest Giver", "Hello, traveler! I have a quest for you.", color_map)
        return "quest_accepted"
    else:
        draw_cutscene_modal(stdscr, "NPC", "Hello there!", color_map)
        return None

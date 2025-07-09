from ..ui.cutscene import draw_entity_modal

def handle_npc_interaction(stdscr, npc, color_map):
    """Handles NPC interaction."""
    if npc["type"] == "quest_giver":
        draw_entity_modal(stdscr, {"name": "Quest Giver", "hp": "N/A", "max_hp": 0, "type": "npc"}, color_map)
        return "quest_accepted"
    else:
        draw_entity_modal(stdscr, {"name": "NPC", "hp": "N/A", "max_hp": 0, "type": "npc"}, color_map)
        return None


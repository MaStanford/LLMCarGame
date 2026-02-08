"""
JSON schemas for grammar-constrained LLM generation.
These schemas are used by llama-cpp-python's response_format parameter
to force the model to produce valid, parseable JSON output.
"""

THEME_SCHEMA = {
    "type": "object",
    "properties": {
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["name", "description"]
            },
            "minItems": 3,
            "maxItems": 3
        }
    },
    "required": ["themes"]
}

QUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "dialog": {"type": "string"},
        "objectives": {
            "type": "array",
            "items": {
                "type": "array"
            }
        },
        "rewards": {
            "type": "object",
            "properties": {
                "xp": {"type": "integer"},
                "cash": {"type": "integer"}
            },
            "required": ["xp", "cash"]
        },
        "target_faction": {}
    },
    "required": ["name", "description", "dialog", "objectives", "rewards", "target_faction"]
}

FACTION_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "hub_city_coordinates": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 2,
                "maxItems": 2
            },
            "control": {"type": "integer"},
            "relationships": {
                "type": "object",
                "additionalProperties": {"type": "string"}
            },
            "units": {
                "type": "array",
                "items": {"type": "string"}
            },
            "faction_boss": {}
        },
        "required": ["name", "description", "hub_city_coordinates", "control", "relationships", "units", "faction_boss"]
    }
}

WORLD_DETAILS_SCHEMA = {
    "type": "object",
    "properties": {
        "cities": {
            "type": "object",
            "additionalProperties": {"type": "string"}
        },
        "roads": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        },
        "landmarks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "x": {"type": "integer"},
                    "y": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
    },
    "required": ["cities", "roads", "landmarks"]
}

ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "base_item_id": {"type": "string"},
        "description": {"type": "string"},
        "rarity": {"type": "string"},
        "stat_modifiers": {
            "type": "object",
            "additionalProperties": {"type": "number"}
        },
        "cosmetic_tags": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["name", "base_item_id", "description", "rarity", "stat_modifiers", "cosmetic_tags"]
}

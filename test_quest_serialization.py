import json
from car.data.quests import Quest, KillCountObjective, KillBossObjective, SurvivalObjective

def test_quest_serialization():
    print("Testing Quest Serialization...")
    
    # 1. Create a dummy quest
    objectives = [
        KillCountObjective(5),
        KillBossObjective("Bad Guy"),
        SurvivalObjective(100, "Mini Boss")
    ]
    quest = Quest(
        name="Test Quest",
        description="A test quest",
        objectives=objectives,
        rewards={"xp": 100},
        city_id=(1, 1),
        quest_giver_faction="faction_a",
        target_faction="faction_b",
        time_limit=1000,
        next_quest_id="next_quest",
        requires_turn_in=True,
        dialog="Hello",
        is_conquest_quest=True
    )
    
    # 2. Modify state
    quest.objectives[0].kill_count = 3
    quest.objectives[2].timer = 50
    quest.completed = False
    
    # 3. Serialize
    data = quest.to_dict()
    print("Serialized Data:", json.dumps(data, indent=2))
    
    # 4. Deserialize
    loaded_quest = Quest.from_dict(data)
    
    # 5. Verify
    assert loaded_quest.name == quest.name
    assert loaded_quest.description == quest.description
    assert len(loaded_quest.objectives) == 3
    assert isinstance(loaded_quest.objectives[0], KillCountObjective)
    assert loaded_quest.objectives[0].kill_count == 3
    assert loaded_quest.objectives[0].target_count == 5
    assert isinstance(loaded_quest.objectives[1], KillBossObjective)
    assert loaded_quest.objectives[1].boss_name == "Bad Guy"
    assert isinstance(loaded_quest.objectives[2], SurvivalObjective)
    assert loaded_quest.objectives[2].timer == 50
    assert loaded_quest.rewards == quest.rewards
    assert loaded_quest.city_id == quest.city_id
    assert loaded_quest.quest_giver_faction == quest.quest_giver_faction
    assert loaded_quest.target_faction == quest.target_faction
    assert loaded_quest.time_limit == quest.time_limit
    assert loaded_quest.next_quest_id == quest.next_quest_id
    assert loaded_quest.requires_turn_in == quest.requires_turn_in
    assert loaded_quest.dialog == quest.dialog
    assert loaded_quest.is_conquest_quest == quest.is_conquest_quest
    
    print("Quest Serialization Test Passed!")

if __name__ == "__main__":
    test_quest_serialization()

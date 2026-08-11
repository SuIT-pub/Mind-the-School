# Quest definitions archived under quests/legacy_archive/quest_list.archive.txt.
# load_quests is a no-op for call-site / start-flow compatibility.

label load_quests:
    if not quest_manager:
        $ quest_manager = QuestManager()
    return

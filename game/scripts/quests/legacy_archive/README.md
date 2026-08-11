# Legacy quest system archive

Full copies of the retired quest implementation. Ren'Py does **not** load `.txt`.

- `quest_manager.archive.txt` — `QuestManager`, `Quest`, `Goal`, `Task` hierarchy
- `quest_list.archive.txt` — `label load_quests` definitions
- `quest.archive.txt` — older commented / alternate quest class drafts

Runtime stubs (no-op manager + unpickle classes) live in `../quest_manager.rpy`.
`clean_legacy_quests()` resets `quest_manager` to an empty stub after load.

init -99 python:
    from deprecated import deprecated

    # Full quest system archived under quests/legacy_archive/*.archive.txt.
    # These stubs exist only so old saves can unpickle; clean_legacy_quests then
    # drops the quest variables from the store.

    @deprecated(version='0.2.3', reason="Quest system archived; stub for save/call-site compatibility.")
    class QuestManager:
        """Empty quest manager. Methods are no-ops / safe defaults."""

        def __init__(self):
            self.all_quests = {}
            self.goals = {}
            self.tasks = {}
            self.task_check = {}
            self.category_quest = {}

        def set_quest(self, quest):
            pass

        def get_quest(self, key: str):
            return None

        def get_quests(self):
            return self.all_quests

        def set_goal(self, goal):
            pass

        def get_goal(self, key: str):
            return None

        def get_goals(self):
            return self.goals

        def set_task(self, task):
            pass

        def get_task(self, key: str):
            return None

        def get_tasks(self):
            return self.tasks

        def get_task_checks(self):
            return self.task_check

        def register_task(self, task):
            pass

        def deregister_task(self, task):
            pass

        def set_quest_category(self, quest):
            pass

        def load_quest(self, quest):
            pass

        def check_all(self, **kwargs) -> bool:
            return True

        def check_quest(self, key: str, **kwargs) -> bool:
            return False

        def check_goal(self, key: str, **kwargs) -> bool:
            return False

        def check_task(self, key: str, **kwargs) -> bool:
            return False

        def check_task_type(self, task_type: str, **kwargs) -> bool:
            return True

        def update_complete_all(self):
            pass

        def run_effect_init(self):
            pass

        def run_effect_hint(self):
            pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class Quest:
        def __init__(self, *args, **kwargs):
            self.key = kwargs.get("key", args[0] if args else "")
            self.name = ""
            self.category = ""
            self.description = []
            self.finished_description = []
            self.thumbnail = ""
            self.effects = {}
            self.goals = {}
            self.tasks = {}
            self.goal_order = []
            self.visible = False
            self.complete = False
            self.valid = True

        def get_active_goals(self):
            return {}

        def check(self, **kwargs):
            return True

        def update_complete(self):
            pass

        def set_complete(self, **kwargs):
            self.complete = True

        def set_visible(self, is_visible: bool):
            self.visible = is_visible

        def run(self, effect_type: str):
            pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class Goal:
        def __init__(self, *args, **kwargs):
            self.key = kwargs.get("key", args[0] if args else "")
            self.name = ""
            self.description = []
            self.effects = {}
            self.tasks = {}
            self.visible = False
            self.complete = False

        def check(self, **kwargs):
            return True

        def set_complete(self, **kwargs):
            self.complete = True

        def set_visible(self, is_visible: bool):
            self.visible = is_visible

        def run(self, effect_type: str):
            pass

        def get_progress(self):
            return []

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class Task:
        def __init__(self, *args, **kwargs):
            self.key = kwargs.get("key", args[0] if args else "")
            self.name = ""
            self.task_type = ""
            self.description = []
            self.effects = {}
            self.active = False
            self.visible = False
            self.complete = False

        def check(self, **kwargs):
            return True

        def set_complete(self, **kwargs):
            self.complete = True

        def activate(self):
            self.active = True

        def set_visible(self, is_visible: bool):
            self.visible = is_visible

        def display(self):
            return []

        def run(self, effect_type: str):
            pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class TaskGroup(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class TaskOptionalGroup(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class OptionalTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class LabelTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class EventTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class EventValueTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class ConditionTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class TriggerTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class JournalUnlockTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class JournalUpgradeTask(Task):
        pass

    @deprecated(version='0.2.3', reason="Quest system archived; kept for save compatibility.")
    class ScheduleVotingTask(Task):
        pass

    def drop_legacy_store_vars(*names: str):
        """
        Remove store variables an old save still carries. Ren'Py records the
        deletion, so the next save no longer writes them.
        """
        for name in names:
            if hasattr(renpy.store, name):
                delattr(renpy.store, name)

    def clean_legacy_quests():
        """
        Drop the quest system's store variables from an old save. The stub
        classes above only have to exist long enough for that save to unpickle.
        """
        drop_legacy_store_vars("quest_manager", "quests", "all_quests", "goals", "tasks", "task_check", "category_quest")

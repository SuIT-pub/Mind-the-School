init -97 python:  

    class Quest:
        """
        A class representing a quest.

        ### Attributes:
        1. _key: str
            - The key of the quest.
        2. _description: str
            - The description of the quest.
        3. _thumbnail: str
            - The thumbnail of the quest.
        4. _finished_description: str
            - The finished description of the quest.
        5. _goals: List[Goal]
            - The goals of the quest.   

        ### Methods:
        1. get_key() -> str
            - Returns the key of the quest.
        2. get_description() -> str
            - Returns the description of the quest.
        3. get_thumbnail() -> str
            - Returns the thumbnail of the quest.
        4. get_goals() -> List[Goal]
            - Returns the goals of the quest.
        5. get_active_goals() -> Dict[int, Goal]
            - Returns the active goals of the quest.

        ### Parameters:
        1. key: str
            - The key of the quest.
        2. description: str
            - The description of the quest.
        3. thumbnail: str
            - The thumbnail of the quest.
        4. finished_description: str
            - The finished description of the quest.
        5. goals: List[Goal]
            - The goals of the quest.
        """

        def __init__(self, key: str, category: str, description: str, thumbnail: str, finished_description: str, *goals: Goal, starts_active = False, premature_visibility = False):
            self._key = key
            self._description = description
            self._category = category
            self._active = starts_active
            self._thumbnail = thumbnail
            self._premature_visibility = premature_visibility
            self._finished_description = finished_description
            self._has_start_trigger = False
            self._goals = {goal.get_key(): goal for goal in goals}
            self._goal_order = [goal.get_key() for goal in goals]
            [goal.set_quest(self) for goal in goals]
        
        def activate(self):
            self._active = True

            for goal in self._goals.values():
                if goal._starts_active:
                    goal.activate()

        def is_active(self) -> bool:
            return self._active

        def update_data(self, quest: Quest):
            self._description = quest.get_description()
            self._thumbnail = quest.get_thumbnail()
            self._finished_description = quest.get_finished_description()
            self._goal_order = quest.get_goal_order()
            if not hasattr(self, '_has_start_trigger'):
                self._has_start_trigger = False
            new_goals = {}
            for goal in quest.get_goals():
                if goal.get_key() not in self._goals.keys():
                    new_goals[goal.get_key()] = goal
                else:
                    self._goals[goal.get_key()].update_data(goal)
                    new_goals[goal.get_key()] = self._goals[goal.get_key()]

                if new_goals[goal.get_key()]._premature_visibility and not new_goals[goal.get_key()]._active and self.show_prematurely():
                    new_goals[goal.get_key()].activate()
            self._goals = new_goals

        def update(self, key: str, **kwargs):
            for goal in self._goals.values():
                if not goal.is_completed():
                    goal.update(key, **kwargs)

        def get_start_trigger(self) -> bool:
            if not hasattr(self, '_has_start_trigger'):
                self._has_start_trigger = False
            return self._has_start_trigger

        def get_key(self) -> str:
            return self._key

        def get_description(self) -> str:
            return self._description

        def get_finished_description(self) -> str:
            return self._finished_description

        def get_category(self) -> str:
            return self._category

        def get_thumbnail(self) -> str:
            return self._thumbnail

        def get_goals(self) -> List[Goal]:
            return self._goals.values()

        def add_goals(self, goal: Goal, index = -1):
            goal.set_quest(self)
            if index == -1 or index == len(self._goal_order):
                self._goal_order.append(goal.get_key())
            elif index >= 0 and index < len(self._goal_order):
                self._goal_order.insert(index, goal.get_key())
            else:
                return

            self._goals[goal.get_key()] = goal

        def show_prematurely(self) -> bool:
            return self._premature_visibility

        def replace_goal(self, goal: Goal):
            goal.set_quest(self)
            self._goals[goal.get_key()] = goal

        def has_goal(self, key: str) -> bool:
            return key in self._goals.keys()

        def replace_goal_order(self, goal_order: List[str]):
            self._goal_order = goal_order

        def get_active_goals(self) -> Dict[int, Goal]:
            return {i + 1: self._goals[key] for i, key in enumerate(self._goal_order) if key in self._goals.keys() and self._goals[key].is_active()}

        def get_goal_order(self) -> List[str]:
            return self._goal_order

        def get_goal(self, key: str) -> Goal:
            if key in self._goals.keys():
                return self._goals[key]
            return None

        def activate_goal(self, key: str):
            if not self._active:
                self.activate()
            if key in self._goals.keys():
                self._goals[key].activate()

        def activate_all_goals(self):
            if not self._active:
                self.activate()
            for goal in self._goals.values():
                goal.activate()

        def check_completed(self) -> bool:
            completed = all(goal.is_completed() for goal in self._goals.values())
            if completed:
                add_notify_message(f"You completed the quest: {get_translation(self._key)}!")
            return completed

        def force_complete(self):
            for goal in self._goals.values():
                goal.force_complete()

        def activate_next_goal(self, current_goal: str):
            if not self._active and (not self.show_prematurely() or (self.show_prematurely() and get_settingdata("journal_goals_show_note_setting"))):
                self.activate()

            if current_goal in self._goal_order:
                index = self._goal_order.index(current_goal)
                log_val('index', index)
                if index + 1 < len(self._goal_order):
                    self._goals[self._goal_order[index + 1]].activate()

        def all_active_done(self) -> bool:
            all_active_goals = self.get_active_goals()
            return all(goal.is_completed() for goal in self.get_goals())

init -98 python:
    from typing import List

    class Goal():
        def __init__(self, key: str, description: str, *tasks: Task, starts_active = False, activate_next = False, premature_visibility = False, trigger_activate = False):
            self._key = key
            self._description = description
            self._active = False
            self._completed = False
            self._quest = None
            self._activate_next = activate_next
            self._starts_active = starts_active
            self._trigger_activate = trigger_activate
            self._premature_visibility = premature_visibility
            self._tasks = {f"{task.get_type()}_{task.get_key()}": task for task in tasks}
            if self._trigger_activate:
                for task in tasks:
                    task.register(self)

        def update(self, key: str, **kwargs):
            for task in self._tasks.values():
                if task.get_type() == key and not task.is_complete():
                    task.update(**kwargs)

        def update_data(self, goal: Goal):
            self._description = goal.get_description()
            new_tasks = []
            for task in goal.get_tasks():
                if f"{task.get_type()}_{task.get_key()}" not in self._tasks.keys():
                    new_tasks.append(task)
                    if self._active:
                        task.register(self)
                else:
                    new_task = self._tasks[f"{task.get_type()}_{task.get_key()}"]
                    new_task.update_data(task)
                    new_tasks.append(new_task)
            self._tasks = {f"{task.get_type()}_{task.get_key()}": task for task in new_tasks}
            self._activate_next = goal._activate_next
            self._premature_visibility = goal._premature_visibility
            self._trigger_activate = goal._trigger_activate
            if self._trigger_activate:
                self._quest._has_start_trigger = True

        def set_quest(self, quest: Quest):
            self._quest = quest
            if self._trigger_activate:
                self._quest._has_start_trigger = True
            if quest.show_prematurely() and self._premature_visibility:
                self.activate()

        def activate(self):
            self._active = True
            for task in self._tasks.values():
                task.register(self)

        def deactivate(self):
            self._active = False

        def force_complete(self):
            for task in self._tasks.values():
                task.force_complete()
            self.complete()

        def complete(self):
            if self._completed:
                return

            self._completed = True

            if not self._quest.is_active() and ((self._quest.show_prematurely() and get_setting("journal_goals_show_note_setting")) or self._trigger_activate):
                self._quest.activate()

            if self._activate_next:
                self._quest.activate_next_goal(self._key)

            if self._quest.is_active() or (self._quest.show_prematurely() and get_setting("journal_goals_show_note_setting")):
                add_notify_message("You have completed a goal!")

            set_setting(f"show_goal_{self.get_key()}", False)

        def is_active(self) -> str:
            return self._active

        def is_completed(self) -> str:
            completed = all(task.is_complete() for task in self._tasks.values())

            if completed:
                self.complete()

            return self._completed

        def get_key(self) -> str:
            return self._key

        def get_description(self) -> str:
            return self._description

        def get_progress(self) -> List[str]:
            progress = [task.get_progress() for task in self._tasks.values()]
            return progress

        def get_tasks(self) -> List[Task]:
            return self._tasks.values()

init -99 python:
    from abc import ABC, abstractmethod

    class Task(ABC):
        def __init__(self, task_type: str, key: str):
            self._key = key
            self._type = task_type
            self._complete = False
            self._goal = None

        def register(self, goal: str):
            self._goal = goal
            # register_task(self._type, f"{self._quest}_{self._goal.get_key()}_{self._type}_{self._key}", self)

        def update_data(self, task: Task):
            pass

        def deactivate(self):
            pass

        def get_key(self) -> str:
            return self._key

        def get_type(self) -> str:
            return self._type

        def force_complete(self):
            self.complete()

        def complete(self):
            self._complete = True
            log_val('is_complete', str(self._complete) + " " + self._key)
            self.deactivate()
            self._goal.is_completed()
            if self._goal._trigger_activate:
                self._goal.activate()

        def reset(self):
            self._complete = False
            self.deactivate()

        def is_complete(self) -> bool:
            return self._complete

        @abstractmethod
        def get_progress(self) -> str:
            pass

        @abstractmethod
        def update(self, **kwargs):
            pass

    ################
    # region Tasks #

    class EventTask(Task):
        """
        A task that tracks the number of times an event has occurred.

        ### Attributes:
        1. _event: str
            - The name of the event to track.
        2. _min_seen: int
            - The minimum number of times the event must occur for the task to be complete.
        3. _seen: int
            - The number of times the event has occurred.

        ### Methods:
        1. get_progress(self) -> str
            - Returns the progress of the task as a string.
        2. update(self, **kwargs)
            - Updates the progress of the task based on the event that has occurred.
        3. reset(self)
            - Resets the progress of the task.

        ### Parameters:
        1. key: str
            - The key of the task.
        2. description: str
            - The description of the task.
        3. event: str
            - The name of the event to track.
        4. min_seen: int
            - The minimum number of times the event must occur for the task to be complete.
        """

        def __init__(self, event: str, min_seen: int = 1, check_history = False):
            super().__init__("event", event)
            self._event = event
            self._min_seen = min_seen
            self._seen = 0
            self._check_history = check_history

        def update_data(self, task: EventTask):
            self._min_seen = task._min_seen
            self._check_history = task._check_history
            if task._event != self._event:
                self._event = task._event
                self._seen = 0

        def get_progress(self) -> str:
            name = get_translation(self._event)

            log_val('progress ' + self._key + ' is_complete', self.is_complete())

            if self.is_complete():
                return "{color=#00a000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"

        def force_complete(self):
            self._seen = self._min_seen
            super().force_complete()

        def update(self, **kwargs):
            event_name = get_kwargs('event_name', **kwargs)

            if event_name == self._event:
                log('##############################')
                log_val('event_name', event_name)
                log_val('event', self._event)
                log_val('seen', self._seen)
                log_val('min_seen', self._min_seen)
                log_val('check_history', self._check_history)
                log_val('seen in history', get_event_seen(self._event))

            if event_name == self._event:
                self._seen += 1

            if self._check_history and get_event_seen(self._event) and self._seen == 0:
                self._seen = 1
            
            if event_name == self._event:
                log_val('seen', self._seen)

            if self._seen >= self._min_seen:
                if event_name == self._event:
                    log('complete')
                self.complete()
                self._seen = self._min_seen

        def reset(self):
            self._seen = 0
            super().reset()

    class EventValueTask(Task):
        def __init__(self, event: str, min_seen: int = 1, **kwargs):
            super().__init__("event", event)
            self._event = event
            self._min_seen = min_seen
            self._seen = 0
            self._kwargs = kwargs

        def update_data(self, task: EventValueTask):
            self._min_seen = task._min_seen
            if task._event != self._event:
                self._event = task._event
                self._seen = 0
            self._kwargs = task._kwargs

        def get_progress(self) -> str:
            name = get_translation(self._event)

            if self.is_complete():
                return "{color=#00a000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"

        def force_complete(self):
            self._seen = self._min_seen
            super().force_complete()

        def update(self, **kwargs):
            event_name = get_kwargs('event_name', **kwargs)
            if event_name == self._event and all([kwargs.get(key, None) == value for key, value in self._kwargs.items()]):
                self._seen += 1
            if self._seen >= self._min_seen:
                self.complete()
                self._seen = self._min_seen

        def reset(self):
            self._seen = 0
            super().reset()

    class ConditionTask(Task):
        def __init__(self, key: str, name: str, condition: Condition):
            super().__init__(key, name)
            self._name = name
            self._condition = condition

        def update_data(self, task: ConditionTask):
            self._condition = task._condition

        def get_progress(self) -> str:
            return self._condition.to_desc_text()

        def update(self, **kwargs):
            if self._condition.is_fulfilled(**kwargs):
                self.complete()

        def reset(self):
            self._seen = 0
            super().reset()

    class TriggerTask(Task):
        def __init__(self, name: str, description: str):
            super().__init__("trigger", name)
            self._name = name
            self._description = description

        def update_data(self, task: TriggerTask):
            self._description = task._description

        def get_progress(self) -> str:
            return self._description

        def update(self, **kwargs):
            if get_kwargs('name', **kwargs) == self._name:
                self.complete()

    class JournalUnlockTask(Task):
        def __init__(self, journal_obj: str):
            super().__init__("journal_unlock", journal_obj)
            self._journal_obj = journal_obj

        def update_data(self, task: JournalUnlockTask):
            self._journal_obj = task._journal_obj

        def get_progress(self) -> str:
            if self.is_complete():
                return "Unlock {color=#00a000}" + get_translation(self._journal_obj) + "{/color} "
            return "Unlock {color=#a00000}" + get_translation(self._journal_obj) + "{/color} "

        def update(self, **kwargs):
            if get_kwargs('name', **kwargs) == self._journal_obj:
                self.complete()

    class JournalUpgradeTask(Task):
        def __init__(self, journal_obj: str, target_level: int):
            super().__init__("journal_upgrade", journal_obj)
            self._journal_obj = journal_obj
            self._target_level = target_level

        def update_data(self, task: JournalUpgradeTask):
            self._journal_obj = task._journal_obj
            self._target_level = task._target_level

        def get_progress(self) -> str:
            if self.is_complete():
                return "Upgrade " + get_translation(self_journal_obj) + " to Level {color=#00a000}" + self._target_level + "{/color} "
            return "Upgrade " + get_translation(self_journal_obj) + " to Level {color=#a00000}" + self._target_level + "{/color} "

        def update(self, **kwargs):
            if get_kwargs('name', **kwargs) == self._journal_obj and get_kwargs('new_level', **kwargs) >= self._target_level:
                self.complete()

    class ScheduleVotingTask(Task):
        def __init__(self, journal_obj: str, vote_type: str):
            super().__init__("schedule_voting", journal_obj)
            self._journal_obj = journal_obj
            self._vote_type = vote_type

        def update_data(self, task: ScheduleVotingTask):
            self._journal_obj = task._journal_obj
            self._vote_type = task._vote_type

        def get_progress(self) -> str:
            if self.is_complete():
                return "Schedule " + get_translation(self._journal_obj) + " for {color=#00a000}" + self._vote_type + "{/color}"
            return "Schedule " + get_translation(self._journal_obj) + " for {color=#a00000}" + self._vote_type + "{/color}"

        def update(self, **kwargs):
            proposal = get_kwargs('proposal', None, **kwargs)
            if proposal == None:
                return
            if proposal._journal_obj.get_name() == self._journal_obj and proposal._action == self._vote_type:
                self.complete()

    class LabelTask(Task):
        def __init__(self, key: str, description: str):
            super().__init__("deco", key)
            self._description = description
            self._complete = True

        def update_data(self, task: LabelTask):
            self._description = task._description

        def get_progress(self) -> str:
            return self._description

        def update(self, **kwargs):
            pass

    # endregion
    ################
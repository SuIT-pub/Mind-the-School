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
            """
            Activates the quest.
            It activates all the goals that are set to start active.
            """

            self._active = True

            for goal in self._goals.values():
                if goal._starts_active:
                    goal.activate()

        def is_active(self) -> bool:
            """
            Returns whether the quest is active.

            ### Returns:
            1. bool: 
                - Whether the quest is active.
            """

            return self._active

        def update_data(self, quest: Quest):
            """
            Updates the data of the quest to update potential changes to the quest.
            Also updates the data of the goals of the quest.

            ### Parameters:
            1. quest: Quest
                - The quest to update the data from.
            """

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
            """
            Updates the quests progress.

            ### Parameters:
            1. key: str
                - The key of the task type to update.
            """

            for goal in self._goals.values():
                if not goal.is_completed():
                    goal.update(key, **kwargs)

        def get_start_trigger(self) -> bool:
            """
            Returns whether the quest has a start trigger.

            ### Returns:
            1. bool: 
                - Whether the quest gets activated by one of the goals when the goal gets completed.
            """

            if not hasattr(self, '_has_start_trigger'):
                self._has_start_trigger = False
            return self._has_start_trigger

        def get_key(self) -> str:
            """
            Returns the key of the quest.

            ### Returns:
            1. str: 
                - The key of the quest
            """

            return self._key

        def get_description(self) -> str:
            """
            Returns the description of the quest.

            ### Returns:
            1. str: 
                - The description of the quest.
            """

            return self._description

        def get_finished_description(self) -> str:
            """
            Returns the description of the quest, shown after completing all the goals.

            ### Returns:
            1. str: 
                - The finished description of the quest.
            """

            return self._finished_description

        def get_category(self) -> str:
            """
            Returns the category of the quest.

            ### Returns:
            1. str: 
                - The category of the quest.
            """

            return self._category

        def get_thumbnail(self) -> str:
            """
            Returns the thumbnail of the quest.

            ### Returns:
            1. str: 
                - The thumbnail of the quest.
            """

            return self._thumbnail

        def get_goals(self) -> List[Goal]:
            """
            Returns the goals of the quest.

            ### Returns:
            1. List[Goal]: 
                - The goals of the quest.
            """

            return self._goals.values()

        def add_goals(self, goal: Goal, index = -1):
            """
            Adds a goal to the quest.

            ### Parameters:
            1. goal: Goal
                - The goal to add to the quest.
            2. index: int (default = -1)
                - The index to add the goal to. Default is -1, which adds the goal to the end of the goal list.
            """

            goal.set_quest(self)
            if index == -1 or index == len(self._goal_order):
                self._goal_order.append(goal.get_key())
            elif index >= 0 and index < len(self._goal_order):
                self._goal_order.insert(index, goal.get_key())
            else:
                return

            self._goals[goal.get_key()] = goal

        def show_prematurely(self) -> bool:
            """
            Returns whether the quest should show prematurely.
            If the quest is set to show prematurely, it will show in the journal when the hinting is activated.

            ### Returns:
            1. bool: 
                - Whether the quest should show prematurely
            """

            return self._premature_visibility

        def replace_goal(self, goal: Goal):
            """
            Replaces a goal in the quest with another goal.

            ### Parameters:
            1. goal: Goal
                - The goal to replace the goal with.
            """

            goal.set_quest(self)
            self._goals[goal.get_key()] = goal

        def has_goal(self, key: str) -> bool:
            """
            Returns whether the quest has a goal with the given key.

            ### Parameters:
            1. key: str
                - The key of the goal to check for.

            ### Returns:
            1. bool:
                - Whether the quest has a goal with the given key.
            """

            return key in self._goals.keys()

        def replace_goal_order(self, goal_order: List[str]):
            """
            Replaces the order of the goals in the quest.

            ### Parameters:
            1. goal_order: List[str]
                - The new order of the goals in the quest.
            """

            self._goal_order = goal_order

        def get_active_goals(self) -> Dict[int, Goal]:
            """
            Returns the active goals of the quest.

            ### Returns:
            1. Dict[int, Goal]: 
                - The active goals of the quest. The key is the visible order of the goal.
            """

            return {i + 1: self._goals[key] for i, key in enumerate(self._goal_order) if key in self._goals.keys() and self._goals[key].is_active()}

        def get_goal_order(self) -> List[str]:
            """
            Returns the order of the goals in the quest.

            ### Returns:
            1. List[str]: 
                - The order of the goals in the quest.
            """

            return self._goal_order

        def get_goal(self, key: str) -> Goal:
            """
            Returns the goal with the given key.

            ### Parameters:
            1. key: str
                - The key of the goal to return.

            ### Returns:
            1. Goal: 
                - The goal with the given key. If the goal does not exist, it returns None.
            """

            if key in self._goals.keys():
                return self._goals[key]
            return None

        def activate_goal(self, key: str):
            """
            Activates a goal with the given key.
            If the quest is not active, it will activate the quest as well.

            ### Parameters:
            1. key: str
                - The key of the goal to activate.
            """

            if key in self._goals.keys():
                if not self._active:
                    self.activate()
                self._goals[key].activate()

        def activate_all_goals(self):
            """
            Activates all goals in the quest.
            If the quest is not active, it will activate the quest as well.
            """

            if not self._active:
                self.activate()
            for goal in self._goals.values():
                goal.activate()

        def check_completed(self) -> bool:
            """
            Checks whether all goals in the quest are completed.
            If all goals are completed, it will show a notification message.

            ### Returns:
            1. bool: 
                - Whether all goals in the quest are completed.
            """

            completed = all(goal.is_completed() for goal in self._goals.values())
            if completed:
                add_notify_message(f"You completed the quest: {get_translation(self._key)}!")
            return completed

        def force_complete(self):
            """
            Forces all goals in the quest to be completed.
            """

            for goal in self._goals.values():
                goal.force_complete()

        def activate_next_goal(self, current_goal: str):
            """
            Activates the next goal in the quest after the current goal.
            If the quest is not active and the quest is not set to show prematurely or the quest is set to show prematurely and the setting is enabled, it will activate the quest.

            ### Parameters:
            1. current_goal: str
                - The key of the current goal as a reference to activate the next goal.
            """

            if not self._active and (not self.show_prematurely() or (self.show_prematurely() and get_setting("journal_goals_show_note_setting"))):
                self.activate()

            if current_goal in self._goal_order:
                index = self._goal_order.index(current_goal)
                if index + 1 < len(self._goal_order):
                    self._goals[self._goal_order[index + 1]].activate()

        def all_active_done(self) -> bool:
            """
            Checks whether all active goals are completed.

            ### Returns:
            1. bool: 
                - Whether all active goals are completed.
            """

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
            """
            Updates the progress of the goal based on the task type and the kwargs.

            ### Parameters:
            1. key: str
                - The key of the task type to update.
            """

            for task in self._tasks.values():
                if task.get_type() == key and not task.is_complete():
                    task.update(**kwargs)

        def update_data(self, goal: Goal):
            """
            Updates the data of the goal to update potential changes to the goal.
            Also updates the data of the tasks of the goal.

            ### Parameters:
            1. goal: Goal
                - The goal to update the data from.
            """

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
            """
            Sets the quest of the goal.
            If the goal has a trigger to activate the quest, it will set the quest to have a start trigger.
            If the goal is set to show prematurely and the setting is enabled, it will activate the goal.

            ### Parameters:
            1. quest: Quest
                - The quest to set the goal to.
            """

            self._quest = quest
            if self._trigger_activate:
                self._quest._has_start_trigger = True
            if quest.show_prematurely() and self._premature_visibility:
                self.activate()

        def activate(self):
            """
            Activates the goal.
            Also registers all tasks of the goal to the goal.
            """

            self._active = True
            for task in self._tasks.values():
                task.register(self)

        def deactivate(self):
            """
            Deactivates the goal.
            """

            self._active = False

        def force_complete(self):
            """
            Forces all tasks in the goal to be completed.
            """

            for task in self._tasks.values():
                task.force_complete()
            self.complete()

        def complete(self):
            """
            Completes the goal.
            If the goal is set to activate the next goal, it will activate the next goal.
            If the quest is not active and the quest is not set to show prematurely or the quest is set to show prematurely and the setting is enabled, it will activate the quest.
            If the goal is completed, it will show a notification message.
            The Goal will be folded in the journal if it is completed.
            """

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
            """
            Returns whether the goal is active.

            ### Returns:
            1. bool: 
                - Whether the goal is active.
            """

            return self._active

        def is_completed(self) -> str:
            """
            Returns whether the goal is completed.
            If all tasks in the goal are completed, it will complete the goal.

            ### Returns:
            1. bool: 
                - Whether the goal is completed.
            """

            completed = all(task.is_complete() for task in self._tasks.values())

            if completed:
                self.complete()

            return self._completed

        def get_key(self) -> str:
            """
            Returns the key of the goal.

            ### Returns:
            1. str: 
                - The key of the goal.
            """

            return self._key

        def get_description(self) -> str:
            """
            Returns the description of the goal.

            ### Returns:
            1. str: 
                - The description of the goal.
            """

            return self._description

        def get_progress(self) -> List[str]:
            """
            Returns the progress of the goal by listing the progress of all tasks in the goal.

            ### Returns:
            1. List[str]: 
                - The progresses of the tasks in the goal.
            """

            progress = [task.get_progress() for task in self._tasks.values()]
            return progress

        def get_tasks(self) -> List[Task]:
            """
            Returns the tasks of the goal.

            ### Returns:
            1. List[Task]: 
                - The tasks of the goal.
            """

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
            """
            Registers the task to a goal.
            """

            self._goal = goal

        def update_data(self, task: Task):
            """
            Updates the data of the task to update potential changes to the task.
            """
            pass

        def deactivate(self):
            """
            Deactivates the task.
            """

            pass

        def get_key(self) -> str:
            """
            Returns the key of the task.

            ### Returns:
            1. str: 
                - The key of the task
            """
            return self._key

        def get_type(self) -> str:
            """
            Returns the type of the task.

            ### Returns:
            1. str: 
                - The type of the task
            """

            return self._type

        def force_complete(self):
            """
            Forces the task to be completed.
            """

            self.complete()

        def complete(self):
            """
            Completes and deactivates the task.
            Checks if the goal is completed and activates the goal if the goal is set to activate when the task is completed.
            """

            self._complete = True
            self.deactivate()
            self._goal.is_completed()
            if self._goal._trigger_activate:
                self._goal.activate()

        def reset(self):
            """
            Resets the task.
            """

            self._complete = False
            self.deactivate()

        def is_complete(self) -> bool:
            """
            Returns whether the task is complete.

            ### Returns:
            1. bool: 
                - Whether the task is complete.
            """

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
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: EventTask
                - The task to update the data from.
            """

            self._min_seen = task._min_seen
            self._check_history = task._check_history
            if task._event != self._event:
                self._event = task._event
                self._seen = 0

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            Here the progress is the name of the event and the number of times it has occurred.
            If the task is complete, the name of the event is colored green, otherwise it is colored red.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            name = get_translation(self._event)

            if self.is_complete():
                return "{color=#00a000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"

        def force_complete(self):
            """
            Forces the task to be completed
            """

            self._seen = self._min_seen
            super().force_complete()

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the event that has occurred.
            """

            event_name = get_kwargs('event_name', **kwargs)

            if event_name == self._event:
                self._seen += 1

            if self._check_history and get_event_seen(self._event) and self._seen == 0:
                self._seen = 1

            if self._seen >= self._min_seen:
                self.complete()
                self._seen = self._min_seen

        def reset(self):
            """
            Resets the progress of the task.
            """

            self._seen = 0
            super().reset()

    class EventValueTask(Task):
        """
        A task that tracks the number of times an event has occurred with specific values.

        ### Attributes:
        1. _event: str
            - The name of the event to track.
        2. _min_seen: int
            - The minimum number of times the event must occur for the task to be complete.
        3. _seen: int
            - The number of times the event has occurred.
        4. _kwargs: Dict[str, Any]
            - The values that the event must have to count towards the task.

        ### Methods:
        1. update_data(self, task: EventValueTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. force_complete(self)
            - Forces the task to be completed.
        4. update(self, **kwargs)
            - Updates the progress of the task based on the event that has occurred.
        5. reset(self)
            - Resets the progress of the task.

        ### Parameters:
        1. event: str
            - The name of the event to track.
        2. min_seen: int (default = 1)
            - The minimum number of times the event must occur for the task to be complete.
        3. kwargs: Dict[str, Any]
            - The values that the event must have to count towards the task.
        """

        def __init__(self, event: str, min_seen: int = 1, **kwargs):
            super().__init__("event", event)
            self._event = event
            self._min_seen = min_seen
            self._seen = 0
            self._kwargs = kwargs

        def update_data(self, task: EventValueTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: EventValueTask
                - The task to update the data from.
            """

            self._min_seen = task._min_seen
            if task._event != self._event:
                self._event = task._event
                self._seen = 0
            self._kwargs = task._kwargs

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            Here the progress is the name of the event and the number of times it has occurred.
            If the task is complete, the name of the event is colored green, otherwise it is colored red.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            name = get_translation(self._event)

            if self.is_complete():
                return "{color=#00a000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{self._seen}/{self._min_seen}"

        def force_complete(self):
            """
            Forces the task to be completed
            """

            self._seen = self._min_seen
            super().force_complete()

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the event that has occurred.
            """

            event_name = get_kwargs('event_name', **kwargs)
            if event_name == self._event and all([kwargs.get(key, None) == value for key, value in self._kwargs.items()]):
                self._seen += 1
            if self._seen >= self._min_seen:
                self.complete()
                self._seen = self._min_seen

        def reset(self):
            """
            Resets the progress of the task.
            """

            self._seen = 0
            super().reset()

    class ConditionTask(Task):
        """
        A task that tracks whether a condition is fulfilled.

        ### Attributes:
        1. _name: str
            - The name of the condition to track.
        2. _condition: Condition
            - The condition to track.

        ### Methods:
        1. update_data(self, task: ConditionTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the condition.

        ### Parameters:
        1. key: str
            - The key of the task.
        2. name: str
            - The name of the condition to track.
        3. condition: Condition
            - The condition to track.
        """

        def __init__(self, key: str, name: str, condition: Condition):
            super().__init__(key, name)
            self._name = name
            self._condition = condition

        def update_data(self, task: ConditionTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: ConditionTask
                - The task to update the data from.
            """

            self._condition = task._condition

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            The text is provided by the condition.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            return self._condition.to_desc_text()

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the condition.
            """

            if self._condition.is_fulfilled(**kwargs):
                self.complete()

    class TriggerTask(Task):
        """
        A task that just needs to be manually triggered to be completed.
        The trigger can be executed by using `update_quest("trigger", name)`

        ### Attributes:
        1. _name: str
            - The name of the task.
        2. _description: str
            - The description of the task.

        ### Methods:
        1. update_data(self, task: TriggerTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the trigger.

        ### Parameters:
        1. name: str
            - The name of the task.
            - This is used to identify the task when triggering it.
        2. description: str
            - The description of the task.
        """

        def __init__(self, name: str, description: str):
            super().__init__("trigger", name)
            self._name = name
            self._description = description

        def update_data(self, task: TriggerTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: TriggerTask
                - The task to update the data from.
            """

            self._description = task._description

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            return self._description

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the trigger.
            """

            if get_kwargs('name', **kwargs) == self._name:
                self.complete()

    class JournalUnlockTask(Task):
        """
        A task that tracks whether a journal object like a rule, club or building is unlocked.

        ### Attributes:
        1. _journal_obj: str
            - The name of the journal object to unlock.

        ### Methods:
        1. update_data(self, task: JournalUnlockTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the journal object.

        ### Parameters:
        1. journal_obj: str
            - The name of the journal object to unlock.
        """

        def __init__(self, journal_obj: str):
            super().__init__("journal_unlock", journal_obj)
            self._journal_obj = journal_obj

        def update_data(self, task: JournalUnlockTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: JournalUnlockTask
                - The task to update the data from.
            """

            self._journal_obj = task._journal_obj

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            If the task is complete, the name of the journal object is colored green, otherwise it is colored red.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            if self.is_complete():
                return "Unlock {color=#00a000}" + get_translation(self._journal_obj) + "{/color} "
            return "Unlock {color=#a00000}" + get_translation(self._journal_obj) + "{/color} "

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the journal object.
            """

            if get_kwargs('name', **kwargs) == self._journal_obj:
                self.complete()

    class JournalUpgradeTask(Task):
        """
        A task that tracks whether a journal object like a rule, club or building is upgraded to a specific level.

        ### Attributes:
        1. _journal_obj: str
            - The name of the journal object to upgrade.
        2. _target_level: int
            - The level the journal object must be upgraded to.

        ### Methods:
        1. update_data(self, task: JournalUpgradeTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the journal object.

        ### Parameters:
        1. journal_obj: str
            - The name of the journal object to upgrade.
        2. target_level: int
            - The level the journal object must be upgraded to.
        """

        def __init__(self, journal_obj: str, target_level: int):
            super().__init__("journal_upgrade", journal_obj)
            self._journal_obj = journal_obj
            self._target_level = target_level

        def update_data(self, task: JournalUpgradeTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: JournalUpgradeTask
                - The task to update the data from.
            """

            self._journal_obj = task._journal_obj
            self._target_level = task._target_level

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            If the task is complete, the name of the journal object is colored green, otherwise it is colored red.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            if self.is_complete():
                return "Upgrade " + get_translation(self_journal_obj) + " to Level {color=#00a000}" + self._target_level + "{/color} "
            return "Upgrade " + get_translation(self_journal_obj) + " to Level {color=#a00000}" + self._target_level + "{/color} "

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the journal object.
            """

            if get_kwargs('name', **kwargs) == self._journal_obj and get_kwargs('new_level', **kwargs) >= self._target_level:
                self.complete()

    class ScheduleVotingTask(Task):
        """
        A task that tracks whether a proposal is scheduled for voting.

        ### Attributes:
        1. _journal_obj: str
            - The name of the journal object to schedule for voting.
        2. _vote_type: str
            - The type of vote to schedule.

        ### Methods:
        1. update_data(self, task: ScheduleVotingTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the proposal.

        ### Parameters:
        1. journal_obj: str
            - The name of the journal object to schedule for voting.
        2. vote_type: str
            - The type of vote to schedule.
            - possible values: "unlock", "upgrade"
        """

        def __init__(self, journal_obj: str, vote_type: str):
            super().__init__("schedule_voting", journal_obj)
            self._journal_obj = journal_obj
            self._vote_type = vote_type

        def update_data(self, task: ScheduleVotingTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: ScheduleVotingTask
                - The task to update the data from.
            """

            self._journal_obj = task._journal_obj
            self._vote_type = task._vote_type

        def get_progress(self) -> str:
            """
            Returns the progress of the task as a string.
            If the task is complete, the vote type is colored green, otherwise it is colored red.

            ### Returns:
            1. str: 
                - The progress of the task as a string.
            """

            if self.is_complete():
                return "Schedule " + get_translation(self._journal_obj) + " for {color=#00a000}" + self._vote_type + "{/color}"
            return "Schedule " + get_translation(self._journal_obj) + " for {color=#a00000}" + self._vote_type + "{/color}"

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the proposal.
            """

            proposal = get_kwargs('proposal', None, **kwargs)
            if proposal == None:
                return
            if proposal._journal_obj.get_name() == self._journal_obj and proposal._action == self._vote_type:
                self.complete()

    class LabelTask(Task):
        """
        A task that is only used to display a label in the goal.
        This task is always completed by default.

        ### Attributes:
        1. _description: str
            - The description of the task.
        2. _complete: bool
            - Whether the task is complete.

        ### Methods:
        1. update_data(self, task: LabelTask)
            - Updates the data of the task to update potential changes to the task.
        2. get_progress(self) -> str
            - Returns the progress of the task as a string.
        3. update(self, **kwargs)
            - Updates the progress of the task based on the kwargs.
            - This task does not update since it is completed by default.
        """

        def __init__(self, key: str, description: str):
            super().__init__("deco", key)
            self._description = description
            self._complete = True

        def update_data(self, task: LabelTask):
            """
            Updates the data of the task to update potential changes to the task.

            ### Parameters:
            1. task: LabelTask
                - The task to update the data from.
            """

            self._description = task._description

        def get_progress(self) -> str:
            """
            Returns the description of the task as a string.
            """

            return self._description

        def update(self, **kwargs):
            """
            Updates the progress of the task based on the kwargs.
            This task does not update since it is completed by default.
            """

            pass

    # endregion
    ################
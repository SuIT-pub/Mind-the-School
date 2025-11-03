
init -99 python:
    from abc import ABC, abstractmethod

    class Action(ABC):
        def __init__(self):
            return

        @abstractmethod
        def run(self):
            pass

    class CompleteAction(Action):
        def __init__(self, quest_type: str, key: str):
            self.quest_type = quest_type
            self.key = key

        def run(self):
            if self.quest_type == "quest" and self.key in quest_manager.quests.keys():
                quest_manager.quests[self.key].complete()
            if self.quest_type == "goal" and self.key in quest_manager.goals.keys():
                quest_manager.goals[self.key].complete()
            if self.quest_type == "task" and self.key in quest_manager.tasks.keys():
                quest_manager.tasks[self.key].complete()

    class VisibleAction(Action):
        def __init__(self, quest_type: str, key: str):
            self.quest_type = quest_type
            self.key = key

        def run(self):
            log_val('VisibleAction', self.quest_type, self.key)
            if self.quest_type == "quest" and self.key in quest_manager.quests.keys():
                log_val('VisibleAction run', 'quest', self.key)
                quest_manager.quests[self.key].set_visible(True)
            if self.quest_type == "goal" and self.key in quest_manager.goals.keys():
                log_val('VisibleAction run', 'goal', self.key)
                quest_manager.goals[self.key].set_visible(True)
            if self.quest_type == "task" and self.key in quest_manager.tasks.keys():
                log_val('VisibleAction run', 'task', self.key)
                quest_manager.tasks[self.key].set_visible(True)

    class InvisibleAction(Action):
        def __init__(self, quest_type: str, key: str):
            self.quest_type = quest_type
            self.key = key

        def run(self):
            if self.quest_type == "quest" and self.key in quest_manager.quests.keys():
                quest_manager.quests[self.key].set_visible(False)
            if self.quest_type == "goal" and self.key in quest_manager.goals.keys():
                quest_manager.goals[self.key].set_visible(False)
            if self.quest_type == "task" and self.key in quest_manager.tasks.keys():
                quest_manager.tasks[self.key].set_visible(False)

    class ActivateAction(Action):
        def __init__(self, key: str):
            self.key = key

        def run(self):
            quest_manager.tasks[self.key].activate()

    # init_quests = False
    # log_val('init_quests init', init_quests)

    class QuestManager:

        def __init__(self):
            log('QuestManager init')
            self.quests = {}
            self.goals = {}
            self.tasks = {}
            self.task_check = {}
            self.category_quest = {}
            pass

        def register_task(self, task: Task):
            if task.task_type not in self.task_check.keys():
                self.task_check[task.task_type] = []
            self.task_check[task.task_type].append(task)

        def deregister_task(self, task: Task):
            if task.task_type in self.task_check.keys() and task in self.task_check[task.task_type]:
                self.task_check[task.task_type].remove(task)
                if len(self.task_check[task.task_type]) == 0:
                    del self.task_check[task.task_type]

        def set_quest_category(self, quest):
            if quest.category not in self.category_quest.keys():
                self.category_quest[quest.category] = {}
            self.category_quest[quest.category][quest.key] = quest

        def load_quest(self, quest: Quest):
            log_val('QuestManager load_quest', quest.key)
            if quest.key in self.quests.keys():
                log_val('QuestManager load_quest', 'quest already exists', quest.key)

                if self.quests[quest.key].category != quest.category:
                    del self.category_quest[self.quests[quest.key].category][quest.key]

                self.set_quest_category(self.quests[quest.key])
                
                self.quests[quest.key].update_data(quest)
            else:
                log_val('QuestManager load_quest', 'quest does not exist', quest.key)
                self.set_quest_category(quest)
                self.quests[quest.key] = quest

        def check_all(self, **kwargs) -> bool:
            return all(quest.check(**kwargs) for quest in self.quests.values())

        def check_quest(self, key: str, **kwargs) -> bool:
            if key not in self.quests.keys():
                return False
            return self.quests[key].check(**kwargs)

        def check_goal(self, key: str, **kwargs):
            if key not in self.goals.keys():
                return False
            return self.goals[key].check(**kwargs)

        def check_task(self, key: str, **kwargs):
            if key not in self.tasks.keys():
                return False
            return self.tasks[key].check(**kwargs)

        def check_task_type(self, task_type: str, **kwargs):
            if task_type not in self.task_check.keys():
                return False
            return all(task.check(**kwargs) for task in self.task_check[task_type])

        def run_action_init(self):
            # log_val('init_quests', init_quests)
            # global init_quests
            # if init_quests:
            #     return
            # init_quests = True

            log('Running action init')

            for quest in self.quests.values():
                log_val('quest', quest)
                quest.run("init")
            for goal in self.goals.values():
                goal.run("init")
            for task in self.tasks.values():
                task.run("init")

        def run_action_hint(self):
            for quest in self.quests.values():
                quest.run("hint")
            for goal in self.goals.values():
                goal.run("hint")
            for task in self.tasks.values():
                task.run("hint")

        def get_quest(self, key: str):
            if key not in self.quests.keys():
                return None
            return self.quests[key]

    class Quest:
        def __init__(self, key: str, name: str, category: str, description: str | List[str], finished_description: str | List[str], thumbnail: str = "", actions: Dict[str, List[Action]] = {}, *goals: Goal):
            self.key = key
            self.name = name
            self.category = category
            
            self.description = description
            if isinstance(description, str):
                self.description = [description]

            
            self.finished_description = finished_description
            if isinstance(finished_description, str):
                self.finished_description = [finished_description]

            self.thumbnail = thumbnail

            self.goals = {}
            self.goal_order = []

            for goal in goals:
                self.goals[goal.key] = goal
                self.goal_order.append(goal.key)
                goal.set_quest(self)

            self.visible = False
            self.complete = False
            self.actions = actions

            global quest_manager
            quest_manager.quests[key] = self

            self.run("create")
            
        def __str__(self):            
            return f"Quest(\n" + \
                f"  key={self.key},\n" + \
                f"  name={self.name},\n" + \
                f"  category={self.category},\n" + \
                f"  description={self.description},\n" + \
                f"  finished_description={self.finished_description},\n" + \
                f"  thumbnail={self.thumbnail},\n" + \
                f"  actions={self.actions},\n" + \
                f"  goals=\n" + "\n".join([f"{goal}" for goal in self.goals.values()]) + \
                f"  goal_order={self.goal_order},\n" + \
                f"  visible={self.visible},\n" + \
                f"  complete={self.complete},\n" + \
                f")\n"

        def update_data(self, quest: Quest):
            log_val('Quest update_data', self.key)
            self.category = quest.category
            self.description = quest.description
            self.finished_description = quest.finished_description
            self.thumbnail = quest.thumbnail
            self.actions = quest.actions
            self.goal_order = quest.goal_order

            new_goals = {}

            for key in quest.goal_order:
                goal = quest.goals[key]
                if key in self.goals.keys():
                    new_goals[key] = self.goals[key]
                    new_goals[key].update_data(goal)
                else:
                    new_goals[key] = goal
                new_goals[key].set_quest(self)

            self.goals = new_goals

            self.run("update_data")

        def get_active_goals(self) -> Dict[str, Goal]:
            log_val('Quest get_active_goals', self.key)
            return {i: self.goals[goal_key] for i, goal_key in enumerate(self.goal_order) if self.goals[goal_key].visible}

        def set_visible(self, is_visible: bool):
            if self.complete:
                return
            
            log_val('Quest set_visible', self.key, is_visible)
            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            if self.complete:
                return True

            log_val('Quest check', self.key)
            kwargs["quest_check"] = True
            if all(goal.complete or goal.check(**kwargs) for goal in self.goals.values()):
                self.set_complete(**kwargs)
                return True
            self.run("check")
            return False

        def set_complete(self, **kwargs):
            if self.complete:
                return
            
            log_val('Quest set_complete', self.key)
            self.complete = True
            log_val('Quest set_complete', self.key)
            self.run("complete")

        def run(self, action_type: str):
            if self.complete and action_type != "complete":
                return

            log_val('Quest run', self.key, action_type)
            if action_type not in self.actions.keys():
                return
            for action in self.actions[action_type]:
                action.run()

        def get_thumbnail(self) -> str:
            log_val('Quest get_thumbnail', self.key)
            """
            Returns the thumbnail of the quest.

            ### Returns:
            1. str: 
                - The thumbnail of the quest.
            """

            return self.thumbnail


    class Goal:
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], *tasks: Task):
            self.key = key
            self.name = name
            
            self.description = description
            if isinstance(description, str):
                self.description = [description]


            self.tasks = {}

            for task in tasks:
                self.tasks[task.key] = task
                task.set_goal(self)

            self.visible = False
            self.complete = False
            self.actions = actions
            self.quest = None

            global quest_manager
            quest_manager.goals[key] = self
            self.run("create")

        def __str__(self):
            return f"    Goal(\n" + \
                f"      key={self.key},\n" + \
                f"      name={self.name},\n" + \
                f"      description={self.description},\n" + \
                f"      actions={self.actions},\n" + \
                f"      tasks=\n" + "\n".join([f"{task}" for task in self.tasks.values()]) + \
                f"      visible={self.visible},\n" + \
                f"      complete={self.complete},\n" + \
                f"    )\n"

        def update_data(self, goal: Goal):
            log_val('Goal update_data', self.key)
            self.name = goal.name
            self.description = goal.description
            self.actions = goal.actions

            new_tasks = {}

            for task in goal.tasks.values():
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task

                    global quest_manager
                    quest_manager.register_task(task)
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                    
                new_tasks[task.key].set_goal(self)

            self.tasks = new_tasks

            self.run("update_data")

        def set_quest(self, quest: Quest):
            log_val('Goal set_quest', self.key, quest.key)
            self.quest = quest

        def set_visible(self, is_visible: bool):
            if self.complete:
                return
            
            log_val('Goal set_visible', self.key, is_visible)
            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            if self.complete:
                return True

            log_val('Goal check', self.key)
            kwargs["goal_check"] = True
            if all(task.complete or task.check(**kwargs) for task in self.tasks.values()):
                self.set_complete(**kwargs)
                if not get_kwargs("quest_check", False, **kwargs):
                    self.quest.check(**kwargs)
                return True
            self.run("check")
            return False

        def set_complete(self, **kwargs):
            if self.complete:
                return

            log_val('Goal set_complete', self.key)
            for task in self.tasks.values():
                if not task.complete:
                    task.set_complete(**kwargs)
            self.run("complete")

        def run(self, action_type: str):
            if self.complete and action_type != "complete":
                return

            log_val('Goal run', self.key, action_type)

            if action_type not in self.actions.keys():
                return
            for action in self.actions[action_type]:
                action.run()

        def get_progress(self) -> List[str]:
            log_val('Goal get_progress', self.key)
            output = []
            completed = 0
            for task in self.tasks.values():
                if task.complete:
                    completed += 1
                if task.visible:
                    output.extend(task.display())
            output.insert(0, f"Tasks ({completed}/{len(self.tasks)})")
            return output


    class Task(ABC):
        def __init__(self, key: str, name: str, task_type: str, description: str, actions: Dict[str, List[Action]]):
            self.key = key
            self.name = name
            self.task_type = task_type
            
            self.description = description
            if isinstance(description, str):
                self.description = [description]

            self.goal = None
            self.active = False
            self.visible = False
            self.complete = False
            self.actions = actions
            
            global quest_manager
            quest_manager.tasks[key] = self
            self.run("create")

        def __str__(self):
            return f"        Task(\n" + \
                f"          key={self.key},\n" + \
                f"          name={self.name},\n" + \
                f"          task_type={self.task_type},\n" + \
                f"          description={self.description},\n" + \
                f"          actions={self.actions},\n" + \
                f"          active={self.active},\n" + \
                f"          visible={self.visible},\n" + \
                f"          complete={self.complete},\n" + \
                f"        )\n"

        def update_data(self, task: Task):
            log_val('Task update_data', self.key)
            self.name = task.name
            self.actions = task.actions

            self.run("update_data")

        def set_goal(self, goal: Goal):
            log_val('Task set_goal', self.key, goal.key)
            self.goal = goal

        def activate(self):
            if self.complete:
                return

            log_val('Task activate', self.key)

            global quest_manager
            quest_manager.register_task(self)

            self.active = True

            self.run("activate")

        def set_visible(self, is_visible: bool):
            if self.complete:
                return

            log_val('Task set_visible', self.key, is_visible)
            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            if self.complete:
                return True

            log_val('Task check', self.key)
            self.run("check")
            return False

        def set_complete(self, **kwargs):
            if self.complete:
                return

            log_val('Task set_complete', self.key)
            self.complete = True

            global quest_manager
            quest_manager.deregister_task(self)

            if not get_kwargs("goal_check", False, **kwargs):
                self.goal.check(**kwargs)
            self.run("complete")

        def display(self) -> List[str]:
            log_val('Task display', self.key)
            return self.description

        def run(self, action_type: str):
            if self.complete and action_type != "complete":
                return

            log_val('Task run', self.key, action_type)
            if action_type not in self.actions.keys():
                return
            for action in self.actions[action_type]:
                action.run()

    class TaskGroup(Task):
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], *tasks: Task):
            super().__init__(key, name, "None", actions)

            self.tasks = {task.key: task for task in tasks}

        def update_data(self, taskCat: Task):
            self.description = taskCat.description

            new_tasks = {}

            for task in taskCat.tasks:
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task
                    
                    global quest_manager
                    quest_manager.register_task(task)
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                task.set_goal(self)
            self.tasks = new_tasks

            self.run("update_data")

        def check(self, **kwargs) -> bool:
            if all(task.complete or task.check(**kwargs) for task in self.tasks.values()):
                self.set_complete()
                return True
            return super().check(**kwargs)

    class TaskOptionalGroup(Task):
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], *tasks: Task):
            super().__init__(key, name, "None", actions)

            self.tasks = {task.key: task for task in tasks}

        def update_data(self, taskCat: Task):
            self.description = taskCat.description

            new_tasks = {}

            for task in taskCat.tasks:
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task
                    
                    global quest_manager
                    quest_manager.register_task(task)
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                task.set_goal(self)
            self.tasks = new_tasks

            self.run("update_data")

        def check(self, **kwargs) -> bool:
            for task in self.tasks:
                task.check(**kwargs)
            return True

        def display(self) -> List[str]:
            output = self.description
            output.append("The tasks in this group are optional and do not need to be completed.")
            return output

    class EventTask(Task):
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], event: str, min_seen = 1):
            super().__init__(key, name, "event", description, actions)
            self.event = event
            self.min_seen = min_seen

        def update_data(self, task: Task):
            self.event = task.event
            self.min_seen = task.min_seen

            super().update_data(task)

        def check(self, **kwargs) -> bool:
            if get_event_seen_count(self.event) >= self.min_seen:
                self.set_complete()
                return True
            return super().check(**kwargs)

        def display(self) -> List[str]:
            output = self.description.copy()
            if self.complete:
                output.append("- {color=#00a000}" + self.name + "{/color} " + f"{get_event_seen_count(self.event)}/{self.min_seen}")
            else:
                output.append("- {color=#a00000}" + self.name + "{/color} " + f"{get_event_seen_count(self.event)}/{self.min_seen}")

            return output

    class EventValueTask(Task):
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], event: str, min_seen = 1, values = {}):
            super().__init__(key, name, "event", description, actions)
            self.event = event
            self.min_seen = min_seen
            self.seen = 0

        def update_data(self, task: Task):
            self.events = task.events
            self.min_seen = min_seen

            super().update_data(task)

        def check(self, **kwargs) -> bool:
            event_name = get_kwargs('event_name', **kwargs)

            if event_name != self.event:
                return super().check(**kwargs)

            for key, value in self.values.items():
                if get_kwargs_value(key, **kwargs) != value:
                    return super().check(**kwargs)

            self.seen = self.seen + 1

            if self.seen < self.min_seen:
                return super().check(**kwargs)

            self.set_complete()
            return True

        def display(self) -> List[str]:
            output = self.description.copy()
            if self.complete:
                output.append("- {color=#00a000}" + self.name + "{/color} " + f"{get_event_seen_count(self.event)}/{self.min_seen} (with special variant)")
            else:
                output.append("- {color=#a00000}" + self.name + "{/color} " + f"{get_event_seen_count(self.event)}/{self.min_seen} (with special variant)")

            return output

    class ConditionTask(Task):
        def __init__(self, key: str, name: str, task_type: str, description: str | List[str], actions: Dict[str, List[Action]], condition: Condition):
            super().__init__(key, name, task_type, description, actions)
            self.condition = condition

        def update_data(self, task: Task):
            self.condition = task.condition

            super().update_data(task)

        def check(self, **kwargs) -> bool:
            if self.condition.is_fulfilled(**kwargs):
                self.set_complete()
                return True
            return super().check(**kwargs)

        def display(self) -> List[str]:
            output = self.description.copy()
            text = self.condition.to_desc_text()
            if isinstance(text, str):
                output.append("- " + text)
            else:
                output.extend(["- " + text for text in text])
            return output

    class TriggerTask(Task):
        def __init__(self, key: str, description: str | List[str], actions: Dict[str, Action]):
            super().__init__(key, get_translation(self.journal_obj), "trigger", description, actions)

        def check(self, **kwargs):
            if get_kwargs('name', **kwargs) == self.key:
                self.set_complete()
                return True

            return super().check(**kwargs)

    class JournalUnlockTask(Task):
        def __init__(self, key: str, name: str, description: str | List[str], actions: Dict[str, List[Action]], journal_obj: str):
            super().__init__(key, name, "journal_unlock", description, actions)
            self.journal_obj = journal_obj

        def update_data(self, task: Task):
            self.journal_obj = task.journal_obj

            super().update_data(task)

        def check(self, **kwargs):
            journal_obj = find_journal_obj(self.journal_obj)
            if journal_obj != None and journal_obj.is_unlocked():
                self.set_complete()
                return True

            return super().check(**kwargs)

        def display(self) -> List[str]:
            output = self.description.copy()
            if self.is_complete():
                output.append("- Unlock {color=#00a000}" + self.name + "{/color} ")
            else:
                output.append("- Unlock {color=#a00000}" + self.name + "{/color} ")
            return output

    class JournalUpgradeTask(Task):
        def __init__(self, key: str, description: str | List[str], actions: Dict[str, List[Action]], journal_obj: str, min_level = 1):
            super().__init__(key, get_translation(self.journal_obj), "journal_upgrade", description, actions)
            self.journal_obj = journal_obj
            self.min_level = min_level

        def update_data(self, task: Task):
            self.journal_obj = task.journal_obj
            self.min_level = task.min_level

            super().update_data(task)

        def check(self, **kwargs):
            journal_obj = find_journal_obj(self.journal_obj)
            if journal_obj != None and journal_obj.get_level() >= self.min_level:
                self.set_complete()
                return True

            return super().check(**kwargs)

        def display(self) -> List[str]:
            output = self.description.copy()
            if self.is_complete():
                output.append("- Upgrade " + self.name + " to Level {color=#00a000}" + self._target_level + "{/color} ")
            else:
                output.append("- Upgrade " + self.name + " to Level {color=#a00000}" + self._target_level + "{/color} ")
            return output

    class ScheduleVotingTask(Task):
        def __init__(self, key: str, description: str | List[str], actions: Dict[str, List[Action]], journal_obj: str, vote_type: str):
            super().__init__(key, get_translation(self._journal_obj), "schedule_voting", description, actions)
            self.journal_obj = journal_obj
            self.vote_type = vote_type

        def update_data(self, task: Task):
            self.journal_obj = task.journal_obj
            self.voting_type = task.voting_type

            super().update_data(task)

        def check(self, **kwargs):
            proposal = get_kwargs('proposal', None, **kwargs)
            if proposal == None:
                return super().check(**kwargs)
            if proposal._journal_obj.get_name() == self.journal_obj and proposal._action == self.vote_type:
                self.set_complete()
                return True
            return super().check(**kwargs)

        def display(self) -> List[str]:
            output = self.description.copy()
            if self.is_complete():
                output.append("- Schedule " + self.name + " for {color=#00a000}" + self.vote_type + "{/color}")
            else:
                output.append("- Schedule " + self.name + " for {color=#a00000}" + self.vote_type + "{/color}")
            return output

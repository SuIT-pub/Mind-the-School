init -99 python:
    from abc import ABC, abstractmethod
    from typing import Union, List, Tuple, Dict

    class QuestManager:

        def __init__(self):
            self.categories = {}
            self.tasks = {}
            self.goals = {}
            self.quests = {}
            self.all_register = {}
            
        def add_quest(self, *quests: QuestObj):
            global new_quests

            log_val("Adding Quest", quests)
            log_val("Existing Quests", new_quests)

            if not is_mod_active(active_mod_key):
                return


            for quest in quests:
                key = quest.get_key()
                log_val("Adding Quest", key)
                if key in new_quests.keys():
                    new_quests[key].update_data(quest)
                else:
                    new_quests[key] = quest
                new_quests[key].inserted()
                new_quests[key].update("x")

        def register(self, *quest_objs: Union[QuestObj, GoalObj, TaskObj]):
            for quest_obj in quest_objs:
                key = quest_obj.get_key()
                log_val("QuestManager Registering", key)
                if isinstance(quest_obj, QuestObj):
                    self.quests[key] = quest_obj
                    self.all_register['quest_' + key] = quest_obj
                    if quest_obj.get_category() not in self.categories.keys():
                        self.categories[quest_obj.get_category()] = {}
                    self.categories[quest_obj.get_category()][key] = quest_obj
                elif isinstance(quest_obj, GoalObj):
                    self.goals[key] = quest_obj
                    self.all_register['goal_' + key] = quest_obj
                elif isinstance(quest_obj, TaskObj):
                    self.tasks[key] = quest_obj
                    self.all_register['task_' + key] = quest_obj

        def get_by_key(self, key: str) -> Union[QuestObj, GoalObj, TaskObj]:
            if key not in self.all_register.keys():
                return None
            return self.all_register[key]

        def get_quest_by_key(self, key: str) -> QuestObj:
            if key not in self.all_register.keys():
                return self.get_by_key("quest_" + key)
            return self.get_by_key(key)

        def get_goal_by_key(self, key: str) -> GoalObj:
            if key not in self.all_register.keys():
                return self.get_by_key("goal_" + key)
            return self.get_by_key(key)
            
        def get_task_by_key(self, key: str) -> TaskObj:
            if key not in self.all_register.keys():
                return self.get_by_key("task_" + key)
            return self.get_by_key(key)

        def get_quests_by_category(self, category: str) -> List[QuestObj]:
            if category not in self.categories.keys():
                return []
            return list(self.categories[category].values())
    
    quest_manager = QuestManager()

    class QuestWorker(ABC):
        def __init__(self, worker_type: str):
            self._type = worker_type

        def get_type(self) -> str:
            return self._type
        
        @abstractmethod
        def trigger(self) -> bool:
            pass

    class IQuest(ABC):
        def __init__(self, key: str, worker: List[QuestWorker], flags: Dict[str, bool]):
            self._obj_type = self.__class__.__name__
            self._key = key
            self._worker = list(worker)
            self._flags = flags

        def update_data(self, quest: IQuest):
            self._worker = list(quest._worker)
            self._flags = update_dict(quest._flags, self._flags)

        def get_key(self) -> str:
            return self._key

        def get_worker(self, worker_type: str = "") -> List[Worker]:
            if worker_type == "":
                return self._worker
            return [worker.get_type() == worker_type for worker in self._worker]
        
        def set_flag(self, key: str, value: bool):
            log_val("Setting Flag for " + self._obj_type + " " + self.get_key(), key, value)
            self._flags[key] = value

        def has_flag(self, key: str) -> bool:
            return key in self._flags.keys()

        def get_flag(self, key: str) -> bool:
            if not self.has_flag(key):
                return False
            return self._flags[key]

        def trigger_worker(self, worker_type: str):
            global quest_worker_queue

            selected_workers = [worker for worker in self._worker if worker.get_type() == worker_type]

            for worker in selected_workers:
                key = worker.get_key()

                log_val("Queuing Worker", key)

                if not any(key == k for v, k in quest_worker_queue):
                    quest_worker_queue.append((worker, key))

        def activate(self):
            if self.get_flag('active'):
                return
            self.set_flag('active', True)
            self.trigger_worker('activate')

        def complete(self):
            if self.get_flag('completed'):
                return
            self.set_flag('completed', True)
            self.trigger_worker('complete')

        def inserted(self):
            quest_manager.register(self)
            self.trigger_worker('insert')


    class TaskObj(IQuest):

        def __init__(self, task_type: str, key: str, *worker: QuestWorker, **flags):
            log_val("Creating Task", key)
            super().__init__(key, list(worker), update_dict({'completed': False, 'active': False, 'visible': False}, flags))
            self._task_type = task_type

            self._parent_quest = None
            self._parent_goal = None
            
            self.trigger_worker('create')

        def update_data(self, task: TaskObj):
            super().update_data(task)
            self._task_type = task._task_type
            
            self.trigger_worker('create')

        def set_parent_goal(self, parent: GoalObj):
            self._parent_goal = parent

        def set_parent_quest(self, parent: QuestObj):
            self._parent_quest = parent

        def update(self, task_type: str, **kwargs) -> bool:

            if (task_type != self._task_type and task_type != "x") or not self.get_flag('active'):
                return False
            log_val("TaskObj update", self._key, task_type)
            return True
            
        @abstractmethod
        def check_completion(self, **kwargs) -> bool:
            pass

        def complete(self, **kwargs):
            super().complete()
            self._parent_goal.check_completion(**kwargs)

        @abstractmethod
        def get_description(self) -> str:
            pass

    class GoalObj(IQuest):

        def __init__(self, key: str, description: str, *content: Union[QuestWorker, TaskObj], **flags):
            log_val("Creating Goal", key)
            worker = [worker for worker in content if isinstance(worker, QuestWorker)]
            tasks = [task for task in content if isinstance(task, TaskObj)]
            super().__init__(key, list(worker), update_dict({'completed': False, 'active': False, 'visible': False}, flags))
            self._description = description

            self._parent_quest = None
            self._tasks = {}

            self.trigger_worker('create')

            for task in tasks:
                self.add_task(task)

        def update_data(self, goal: GoalObj):
            log_val("GoalObj update_data", self._flags)
            super().update_data(goal)
            log_val("GoalObj update_data after flag update", self._flags)
            self._description = goal._description

            for task in goal._tasks.values():
                self.add_task(task)

            self.trigger_worker('create')

        def update(self, task_type: str, **kwargs):
            for task in self.get_tasks():
                task.update(task_type, **kwargs)
            self.check_completion(**kwargs)

        def add_task(self, *tasks: TaskObj):
            for task in tasks:
                task.set_parent_goal(self)
                if self._parent_quest != None:
                    task.set_parent_quest(self._parent_quest)

                key = task.get_key()
                if key in self._tasks.keys() and type(task) == type(self._tasks[key]):
                    log_val("Updating Task", key)
                    self._tasks[key].update_data(task)
                else:
                    log_val("Adding Task", key)
                    self._tasks[key] = task
                self._tasks[key].inserted()


        def set_parent_quest(self, parent: Quest):
            self._parent_quest = parent
            for task in self._tasks.values():
                task.set_parent_quest(parent)

        def check_completion(self, **kwargs):
            completed = all(task.get_flag('completed') for task in self._tasks.values())
            if not completed and get_kwargs('enable_disabling', False, **kwargs):
                self.set_flag('completed', False)
            elif completed:
                self.complete()
            
        def complete(self):
            super().complete()
            self._parent_quest.check_completion(**kwargs)

        def get_tasks(self) -> List[TaskObj]:
            return list(self._tasks.values())

        def get_visible_tasks(self) -> List[TaskObj]:
            return [task for task in self._tasks.values() if task.get_flag('visible')]

        def get_description(self) -> str:
            return self._description

        def get_task_descriptions(self) -> List[str]:
            return [task.get_description() for task in self._tasks.values()]

    class QuestObj(IQuest):

        def __init__(self, key: str, category: str, description: str, end_msg: str, thumbnail: str, *content: Union[QuestWorker, GoalObj], **flags):
            log_val("Creating Quest", key)
            worker = [worker for worker in content if isinstance(worker, QuestWorker)]
            goals = [goal for goal in content if isinstance(goal, GoalObj)]
            super().__init__(key, list(worker), update_dict({'completed': False, 'active': False, 'helper': False, 'visible': False}, flags))
            self._category = category
            self._description = description
            self._end_msg = end_msg
            self._thumbnail = thumbnail

            self._goals = {}

            self.trigger_worker('create')

            for goal in goals:
                self.add_goal(goal)
            

        def update_data(self, quest: QuestObj):
            super().update_data(quest)
            self._category = quest._category
            self._description = quest._description
            self._end_msg = quest._end_msg
            self._thumbnail = quest._thumbnail

            for goal in quest._goals.values():
                self.add_goal(goal)

            self.trigger_worker('create')

        def update(self, task_type: str,**kwargs):
            for goal in self.get_goals():
                goal.update(task_type, **kwargs)
            self.check_completion(**kwargs)

        def add_goal(self, *goals: GoalObj):
            for goal in goals:
                goal.set_parent_quest(self)
                key = goal.get_key()
                if key in self._goals.keys():
                    log_val("Updating Goal", key)
                    self._goals[key].update_data(goal)
                else:
                    log_val("Adding Goal", key)
                    self._goals[key] = goal
                self._goals[key].inserted()

        def check_completion(self, **kwargs):
            completed = all(goal.get_flag('completed') for goal in self._goals.values())
            if not completed and get_kwargs('enable_disabling', False, **kwargs):
                self.set_flag('completed', False)
            elif completed:
                self.complete()

        def get_goals(self) -> List[GoalObj]:
            return list(self._goals.values())

        def get_visible_goals(self) -> List[GoalObj]:
            return [goal for goal in self._goals.values() if goal.get_flag('visible')]

        def get_description(self) -> str:
            return self._description

        def get_end_msg(self) -> str:
            return self._end_msg

        def get_thumbnail(self) -> str:
            return self._thumbnail

        def get_category(self) -> str:
            return self._category

    class QuestWorkerActivate(QuestWorker):
        def __init__(self, worker_type: str, *quest_obj: str):
            super().__init__(worker_type)
            self._quest_obj = list(quest_obj)

        def get_key(self) -> str:
            return "activate_" + '_'.join(self._quest_obj)

        def trigger(self):
            global quest_manager
            log_val("QuestWorkerActivate", self._quest_obj)
            for quest_obj in self._quest_obj:
                log_val("QuestWorkerActivate", quest_obj)
                activated_object = quest_manager.get_by_key(quest_obj)
                if activated_object != None:
                    activated_object.activate()
                    log_object("QuestWorkerActivate", activated_object)
            
    class QuestWorkerShow(QuestWorker):
        def __init__(self, worker_type: str, *quest_obj: str):
            super().__init__(worker_type)
            self._quest_obj = list(quest_obj)

        def get_key(self) -> str:
            return "show_" + '_'.join(self._quest_obj)

        def trigger(self):
            global quest_manager
            log_val("QuestWorkerShow", self._quest_obj)
            for quest_obj in self._quest_obj:
                log_val("QuestWorkerShow", quest_obj)
                log_object("QuestWorkerShow", quest_manager)
                shown_object = quest_manager.get_by_key(quest_obj)
                if shown_object != None:
                    shown_object.set_flag('visible', True)
                log_object("QuestWorkerShow", shown_object)

    class QuestWorkerHide(QuestWorker):
        def __init__(self, worker_type: str, *quest_obj: str):
            super().__init__(worker_type)
            self._quest_obj = list(quest_obj)

        def get_key(self) -> str:
            return "hide_" + '_'.join(self._quest_obj)

        def trigger(self):
            global quest_manager
            log_val("QuestWorkerHide", self._quest_obj)
            for quest_obj in self._quest_obj:
                log_val("QuestWorkerHide", quest_obj)
                hidden_object = quest_manager.get_by_key(quest_obj)
                if hidden_object != None:
                    hidden_object.set_flag('visible', False)
                log_object("QuestWorkerHide", hidden_object)

    class QuestWorkerComplete(QuestWorker):
        def __init__(self, worker_type: str, *quest_obj: str):
            super().__init__(worker_type)
            self._quest_obj = list(quest_obj)

        def get_key(self) -> str:
            return "complete_" + '_'.join(self._quest_obj)

        def trigger(self):
            global quest_manager
            log_val("QuestWorkerComplete", self._quest_obj)
            for quest_obj in self._quest_obj:
                log_val("QuestWorkerComplete", quest_obj)
                completed_object = quest_manager.get_by_key(quest_obj)
                if completed_object != None:
                    completed_object.complete()
                log_object("QuestWorkerComplete", completed_object)


    
    class EventTaskObj(TaskObj):

        def __init__(self, event: str, key: str, *worker: QuestWorker, min_seen: int = 1, **flags):
            super().__init__("event", key, *worker, **flags)
            self._event = event
            self._min_seen = min_seen

        def update_data(self, task: EventTaskObj):
            super().update_data(task)
            self._event = task._event
            self._min_seen = task._min_seen

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            log_val("EventTaskObj", self._event)

            return self.check_completion(**kwargs)
            
        def check_completion(self, **kwargs) -> bool:
            log_val("EventTaskObj", get_seen_count(self._event))
            if get_seen_count(self._event) >= self._min_seen:
                log_val("EventTaskObj", "complete")
                self.complete()
                return True
            log_val("EventTaskObj", "not complete")
            return False

        def get_description(self) -> str:
            name = get_translation(self._event)

            seen = get_seen_count(self._event)

            if self.get_flag('completed'):
                return "{color=#00a000}" + name + "{/color} " + f"{seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{seen}/{self._min_seen}"

    
    class EventValueTaskObj(TaskObj):

        def __init__(self, event: str, key: str, values: Dict[str, Any], *worker: QuestWorker, min_seen: int = 1, **flags):
            super().__init__("event", key, *worker, **flags)
            self._event = event
            self._values = values
            self._min_seen = min_seen
            self._seen = 0

        def update_data(self, task: EventTaskObj):
            super().update_data(task)
            self._event = task._event
            self._values = task._values
            self._min_seen = task._min_seen

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            event_name =  get_kwargs('event_name', **kwargs)
            values = get_kwargs_values(**kwargs)

            if event_name == self._event and all([values.get(key, None) == value for key, value in self._values.items()]):
                self._seen += 1
            
            return self.check_completion(**kwargs)
            
        def check_completion(self, **kwargs) -> bool:
            event_name = get_kwargs('event_name', **kwargs)

            if self._seen >= self._min_seen:
                self._seen = self._min_seen
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            name = get_translation(self._event)

            seen = get_seen_count(self._event)

            if self.get_flag('completed'):
                return "{color=#00a000}" + name + "{/color} " + f"{seen}/{self._min_seen}"
            return "{color=#a00000}" + name + "{/color} " + f"{seen}/{self._min_seen}"

    class ConditionTaskObj(TaskObj):

        def __init__(self, task_type: str, condition: Condition, key: str, *worker: QuestWorker, **flags):
            super().__init__(task_type, key, *worker, **flags)
            self._condition = condition

        def update_data(self, task: ConditionTaskObj):
            super().update_data(task)
            self._condition = task._condition

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            return self.check_completion(**kwargs)

        def check_completion(self, **kwargs) -> bool:
            if self._condition.is_fulfilled(**kwargs):
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            return self._condition.to_desc_text()

    class TriggerTaskObj(TaskObj):

        def __init__(self, description: str, key: str, *worker: QuestWorker, **flags):
            super().__init__("trigger", key, *worker, **flags)
            self._description = description

        def update_data(self, task: TriggerTaskObj):
            super().update_data(task)
            self._description = task._description

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            return self.check_completion(**kwargs)

        def check_completion(self, **kwargs) -> bool:
            if get_kwargs('name', **kwargs) == self.get_key():
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            return self._description

    class JournalUnlockTaskObj(TaskObj):

        def __init__(self, journal_obj: str, key: str, *worker: QuestWorker, **flags):
            super().__init__("journal_unlock", key, *worker, **flags)
            self._journal_obj = journal_obj

        def update_data(self, task: JournalUnlockTaskObj):
            super().update_data(task)
            self._journal_obj = task._journal_obj

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            return self.check_completion(**kwargs)

        def check_completion(self, **kwargs) -> bool:
            if get_kwargs('name', **kwargs) == self._journal_obj:
                self.complete()
                return True
            journal_obj = find_journal_obj(self._journal_obj)
            if journal_obj != None and journal_obj.is_unlocked():
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            if self.get_flag('completed'):
                return "Unlock {color=#00a000}" + get_translation(self._journal_obj) + "{/color} "
            return "Unlock {color=#a00000}" + get_translation(self._journal_obj) + "{/color} "

    class JournalUpgradeTaskObj(TaskObj):

        def __init__(self, journal_obj: str, target_level: int, key: str, *worker: QuestWorker, **flags):
            super().__init__("journal_upgrade", key, *worker, **flags)
            self._journal_obj = journal_obj
            self._target_level = target_level

        def update_data(self, task: JournalUpgradeTaskObj):
            super().update_data(task)
            self._journal_obj = task._journal_obj
            self._target_level = task._target_level

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            return self.check_completion(**kwargs)

        def check_completion(self, **kwargs) -> bool:
            if get_kwargs('name', **kwargs) == self._journal_obj and get_kwargs('new_level', **kwargs) >= self._target_level:
                self.complete()
                return True
            journal_obj = find_journal_obj(self._journal_obj)
            if journal_obj != None and journal_obj.get_level() >= self._target_level:
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            if self.get_flag('completed'):
                return "Upgrade {color=#00a000}" + get_translation(self._journal_obj) + "{/color} to Level {color=#00a000}" + self._target_level + "{/color} "
            return "Upgrade {color=#a00000}" + get_translation(self._journal_obj) + "{/color} to Level {color=#a00000}" + self._target_level + "{/color} "

    class ScheduleVotingTaskObj(TaskObj):

        def __init__(self, journal_obj: str, vote_type: str, key: str, *worker: QuestWorker, **flags):
            super().__init__("schedule_voting", key, *worker, **flags)
            self._journal_obj = journal_obj
            self._vote_type = vote_type

        def update_data(self, task: ScheduleVotingTaskObj):
            super().update_data(task)
            self._journal_obj = task._journal_obj
            self._vote_type = task._vote_type

        def update(self, task_type: str, **kwargs) -> bool:
            if not super().update(task_type, **kwargs):
                return False

            return self.check_completion(**kwargs)

        def check_completion(self, **kwargs) -> bool:
            proposal = get_kwargs('proposal', None, **kwargs)
            if proposal == None:
                return False
            if proposal._journal_obj.get_name() == self._journal_obj and proposal._action == self._vote_type:
                self.complete()
                return True
            return False

        def get_description(self) -> str:
            if self.get_flag('completed'):
                return "Schedule " + get_translation(self._journal_obj) + " for {color=#00a000}" + self._vote_type + "{/color}"
            return "Schedule " + get_translation(self._journal_obj) + " for {color=#a00000}" + self._vote_type + "{/color}"

    class LabelTaskObj(TaskObj):
        def __init__(self, description: str, key: str, *worker: QuestWorker, **flags):
            super().__init__("deco", key, *worker, **flags)
            self._description = description
            self.set_flag('completed', True)

        def update_data(self, task: LabelTaskObj):
            super().update_data(task)
            self._description = task._description

        def update(self, task_type: str, **kwargs) -> bool:
            return True

        def check_completion(self, **kwargs) -> bool:
            return True

        def get_description(self) -> str:
            return self._description

    class OptionalTaskObj(TaskObj):
        def __init__(self, task_type: str, task: TaskObj, key: str, *worker: QuestWorker, **flags):
            super().__init__(task_type, key, *worker, **flags)
            self._task = task
            self.set_flag('completed', True)

        def update_data(self, task: OptionalTaskObj):
            super().update_data(task)
            if isinstance(task._task, type(self._task)):
                self._task.update_data(task._task)
            else:
                self._task = task._task

        def update(self, task_type: str, **kwargs) -> bool:
            return True

        def check_completion(self, **kwargs) -> bool:
            return True

        def get_description(self) -> str:
            return self._task.get_description()

# init -98 python:
#     quest_manager = QuestManager()

# init -99 python:
#     from abc import ABC, abstractmethod



#     class QuestManager:

#         def __init__(self):
#             self.quests = {}
#             self.goals = {}
#             self.tasks = {}
#             self.task_check = {}
#             pass

#         def register_task(self, task: Task):
#             if task.key not in self.task_check.keys():
#                 self.task_check[task.key] = []
#             self.task_check[task.key].append(task)



#     class Quest:
#         def __init__(self, key: str):
#             self.goals = {}
#             self.visible = False
#             self.complete = False

#             global quest_manager
#             quest_manager.quests[key] = self
            
#         def set_visible(self, is_visible: bool):
#             self.visible = is_visible

#         def check(self, **kwargs):
#             if all(goal.complete or goal.check(**kwargs) for goal in self.goals.values()):

#     class Goal:
#         def __init__(self, name: str):
#             self.name = name
#             self.tasks = {}
#             self.visible = False
#             self.complete = False

#             global quest_manager
#             quest_manager.goals[key] = self

#         def add_task(self, task: Task):
#             if task.name not in self.tasks.keys():
#                 self.tasks[task.name] = task
#             else:
#                 self.tasks[task.name].update_data(task)
#             task.set_goal(self)

#         def set_visible(self, is_visible: bool):
#             self.visible = is_visible

#         def check(self, **kwargs) -> bool:
#             if all(task.complete or task.check(**kwargs) for task in self.tasks.values()):
#                 self.complete()
#                 return True
#             return False

#         def complete(self):
#             for task in self.tasks.values():
#                 task.complete()

#     class Task(ABC):
#         def __init__(self, name: str, key: str):
#             self.name = name
#             self.key = key
#             self.goal = None
#             self.active = False
#             self.visible = False
#             self.complete = False
            
#             global quest_manager
#             quest_manager.tasks[key] = self

#         def set_goal(self, goal: Goal):
#             self.goal = goal

#         def activate(self):
#             global quest_manager
#             quest_manager.register_task(self)

#             self.active = True

#         def set_visible(self, is_visible: bool):
#             self.visible = is_visible

#         @abstractmethod
#         def update_data(self, task: Task):
#             pass

#         @abstractmethod
#         def check(self, **kwargs) -> bool:
#             pass

#         @abstractmethod
#         def complete(self):
#             pass
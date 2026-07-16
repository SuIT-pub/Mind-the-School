
init -99 python:
    from abc import ABC, abstractmethod
    from deprecated import deprecated

    # init_quests = False
    # log_val('init_quests init', init_quests)

    class QuestManager:

        def __init__(self):
            self.all_quests = {}
            self.goals = {}
            self.tasks = {}
            self.task_check = {}
            self.category_quest = {}
            pass

        def set_quest(self, quest: Quest):
            self.all_quests[quest.key] = quest
        def get_quest(self, key: str):
            if key not in self.all_quests.keys():
                return None
            return self.all_quests[key]
        def get_quests(self):
            return self.all_quests

        def set_goal(self, goal: Goal):
            self.goals[goal.key] = goal
        def get_goal(self, key: str):
            if key not in self.goals.keys():
                return None
            return self.goals[key]
        def get_goals(self):
            return self.goals

        def set_task(self, task: Task):
            self.tasks[task.key] = task
        def get_task(self, key: str):
            if key not in self.tasks.keys():
                return None
            return self.tasks[key]
        def get_tasks(self):
            return self.tasks

        def get_task_checks(self):
            return self.task_check

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
            if not quest.valid:
                log_error(800, "Quest invalid! Quest skipped.")
                return

            if quest.key in self.all_quests.keys():

                if self.all_quests[quest.key].category != quest.category:
                    del self.category_quest[self.all_quests[quest.key].category][quest.key]

                self.set_quest_category(self.all_quests[quest.key])
                
                self.all_quests[quest.key].update_data(quest)
            else:
                self.set_quest_category(quest)
                self.all_quests[quest.key] = quest
                self.all_quests[quest.key].init_data()

        def check_all(self, **kwargs) -> bool:
            return all(quest.check(**kwargs) for quest in self.all_quests.values())

        def check_quest(self, key: str, **kwargs) -> bool:
            if key not in self.all_quests.keys():
                return False
            return self.all_quests[key].check(**kwargs)

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

        def update_complete_all(self):
            for quest in self.all_quests.values():
                quest.update_complete()

        def run_effect_init(self):
            for quest in self.all_quests.values():
                quest.run("init")
            for goal in self.goals.values():
                goal.run("init")
            for task in self.tasks.values():
                task.run("init")

        def run_effect_hint(self):
            for quest in self.all_quests.values():
                quest.run("hint")
            for goal in self.goals.values():
                goal.run("hint")
            for task in self.tasks.values():
                task.run("hint")

        def get_quest(self, key: str):
            if key not in self.all_quests.keys():
                return None
            return self.all_quests[key]


    class Quest:
        """
        A Quest is a collection of goals and tasks that are related to a specific topic.
        It is used to track the progress of the player and to provide a way to reward the player for completing the quest.

        Parameters:
            key: str
                - The key of the quest.
            name: str
                - The name of the quest.
            category: str
                - The category of the quest.
            description: str
                - The description of the quest.
            finished_description: str
                - The finished description of the quest.
            thumbnail: str
                - The thumbnail of the quest.
            effects: Dict[str, List[Effect]]
                - The effects of the quest.
            *goals: Union[Goal, Task]
                - The goals of the quest.

        Attributes:
            key: str
                - The key of the quest.
            name: str
                - The name of the quest.
            category: str
                - The category of the quest.
            description: str
                - The description of the quest.
            finished_description: str
                - The finished description of the quest.
            thumbnail: str
                - The thumbnail of the quest.
            effects: Dict[str, List[Effect]]
                - The effects of the quest.
            goals: Dict[str, Goal]
                - The goals of the quest.
            goal_order: List[str]
                - The order of the goals in the quest.
            visible: bool
                - Whether the quest is visible.
            complete: bool
                - Whether the quest is complete.
            tasks: Dict[str, Task]
                - The tasks of the quest.

        Methods:
            __init__(self, key: str, name: str, category: str, description: str, finished_description: str, thumbnail: str = "", effects: Dict[str, List[Effect]] = {}, *goals: Union[Goal, Task]):
                - Initializes the quest.
            __str__(self):
                - Returns a string representation of the quest.
            init_data(self):
                - Initializes the data of the quest.
            update_data(self, quest: Quest):
                - Updates the data of the quest.
            get_active_goals(self) -> Dict[str, Goal]:
                - Returns the active goals of the quest.
            set_visible(self, is_visible: bool):
                - Sets the visibility of the quest.
            check(self, **kwargs) -> bool:
                - Checks if the quest is complete.
            update_complete(self):
                - Updates the complete status of the quest.
            set_complete(self, **kwargs):
                - Sets the complete status of the quest.
            run(self, effect_type: str):
                - Runs the effect of the quest.
            get_thumbnail(self) -> str:
                - Returns the thumbnail of the quest.
        """

        def __init__(self, key: str, name: str, category: str, description: str, finished_description: str, thumbnail: str = "", effects: Dict[str, List[Effect]] = {}, *goals: Union[Goal, Task]):
            self.valid = True

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

            self.tasks = {}
            self.goals = {}
            self.goal_order = []

            # separate goals and tasks
            for goal in goals:
                if not goal.validate():
                    self.valid = False
                if isinstance(goal, Goal):
                    self.goals[goal.key] = goal
                    self.goal_order.append(goal.key)
                elif isinstance(goal, Task):
                    self.tasks[goal.key] = goal
                
                goal.set_parent(self)

            self.visible = False
            self.complete = False
            self.effects = effects

            if not self.validate():
                self.valid = False

            self.run("create")
            
        def __str__(self):            
            return f"Quest(\n" + \
                f"  key={self.key},\n" + \
                f"  name={self.name},\n" + \
                f"  category={self.category},\n" + \
                f"  description={self.description},\n" + \
                f"  finished_description={self.finished_description},\n" + \
                f"  thumbnail={self.thumbnail},\n" + \
                f"  effects={self.effects},\n" + \
                f"  goals=\n" + "\n".join([f"{goal}" for goal in self.goals.values()]) + \
                f"  goal_order={self.goal_order},\n" + \
                f"  visible={self.visible},\n" + \
                f"  complete={self.complete},\n" + \
                f")\n"

        def validate(self) -> bool:
            if not isinstance(self.key, str):
                log_error(802, f"Attribute invalid: Quest 'key' invalid type! (should be `str`)")
            elif not isinstance(self.name, str):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'name' invalid type! (should be `str`)")
            elif not isinstance(self.category, str):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'category' invalid type! (should be `str`)")
            elif not isinstance(self.description, list):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'description' invalid type! (should be `list`)")
            elif any(not isinstance(desc, str) for desc in self.description):
                log_error(802, "Attribute invalid: An element in Quest 'description' is invalid type! (Should be `str`)")
            elif not isinstance(self.finished_description, list):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'finished_description' invalid type! (should be `List(str)`)")
            elif any(not isinstance(desc, str) for desc in self.finished_description):
                log_error(802, "Attribute invalid: An element in Quest 'finished_description' is invalid type! (Should be `str`)")
            elif not isinstance(self.thumbnail, str):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'thumbnail' invalid type! (should be `str`)")
            elif not isinstance(self.tasks, dict):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'tasks' invalid type! (should be `Dict(str, Task)`)")
            elif not isinstance(self.goals, dict):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'goals' invalid type! (should be `Dict(str, Goal)`)")
            elif not isinstance(self.goal_order, list):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'goal_order' invalid type! (should be `List(str)`)")
            elif not isinstance(self.visible, bool):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'visible' invalid type! (should be `bool`)")
            elif not isinstance(self.complete, bool):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'complete' invalid type! (should be `bool`)")
            elif not isinstance(self.effects, dict):
                log_error(802, f"Attribute invalid: Quest({self.key}) 'effects' invalid type! (should be `Dict(str, List(Effect))`)")
            elif any(not isinstance(effect_list, list) or any(not isinstance(effect, Effect) for effect in effect_list) for effect_list in self.effects.values()):
                log_error(802, "Attribute invalid: An element in Quest 'effects' is invalid type! ('effects' should be `Dict(str, List(Effect))`)")
            else:
                if not renpy.loadable(self.thumbnail):
                    log_error(204, f"Image_Path '{self.thumbnail}' not found!")
                return True

            return False

        def init_data(self):
            """
            Initializes the data of the quest.
            Sets the parent of the goals and tasks of the quest.
            Also initializes the data of the goals and tasks of the quest.
            """
            global quest_manager

            for key in self.goal_order:
                self.goals[key].set_parent(self)
                quest_manager.set_goal(self.goals[key])
                self.goals[key].init_data()

            for task in self.tasks.values():
                task.set_parent(self)
                quest_manager.set_task(task)
                task.init_data()


        def update_data(self, quest: Quest):
            """
            Updates the data of the quest to update potential changes to the quest.
            Also updates the data of the goals and tasks of the quest.
            
            ### Parameters:
            1. quest: Quest
                - The quest to update the data from.
            """

            self.category = quest.category
            self.description = quest.description
            self.finished_description = quest.finished_description
            self.thumbnail = quest.thumbnail
            self.effects = quest.effects
            self.goal_order = quest.goal_order

            global quest_manager

            new_goals = {}

            for key in quest.goal_order:
                goal = quest.goals[key]
                if key in self.goals.keys():
                    new_goals[key] = self.goals[key]
                    new_goals[key].update_data(goal)
                else:
                    new_goals[key] = goal
                    new_goals[key].init_data()
                new_goals[key].set_parent(self)

                quest_manager.set_goal(new_goals[key])

            self.goals = new_goals

            
            new_tasks = {}
            
            for task in quest.tasks.values():
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task

                    quest_manager.register_task(task)
                    task.init_data()
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                    
                new_tasks[task.key].set_parent(self)

                quest_manager.set_task(new_tasks[task.key])

            self.tasks = new_tasks

            self.run("update_data")

        def get_active_goals(self) -> Dict[str, Goal]:
            """
            Returns the active goals of the quest.
            
            ### Returns:
            1. Dict[str, Goal]:
                - The active goals of the quest. The dictionary key is the key of the goal.
            """

            return {goal_key: self.goals[goal_key] for goal_key in self.goal_order if self.goals[goal_key].visible}

        def set_visible(self, is_visible: bool):
            """
            Sets the visibility of the quest.

            ### Parameters:
            1. is_visible: bool
                - Whether the quest should be visible.
            """

            if self.complete:
                return
            
            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            """
            Checks if the quest is complete by iterating through all goals and tasks and checking if all goals are complete.

            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - Additional arguments that may affect the complete status of the quest.

            ### Returns:
            1. bool:
                - True if the quest is complete, False otherwise.
            """
            if self.complete:
                return True

            kwargs["quest_check"] = True
            if all(goal.complete or goal.check(**kwargs) for goal in self.goals.values()):
                self.set_complete(**kwargs)
                return True
            self.run("check")
            return False

        def update_complete(self):
            """
            Updates the complete status of the quest.
            Iterates through all goals and tasks and updates the complete status of the quest.
            If all goals are complete, the quest is complete.
            """

            for goal in self.goals.values():
                if self.complete and not goal.complete:
                    goal.set_complete()
                goal.update_complete()
            if all(goal.complete for goal in self.goals.values()) and not self.complete:
                self.set_complete()

        def set_complete(self, **kwargs):
            """
            Sets the complete status of the quest.

            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - unused
            """
            if self.complete:
                return
            
            self.complete = True
            self.run("complete")

        def run(self, effect_type: str):
            """
            Runs the effect of the quest.

            ### Parameters:
            1. effect_type: str
                - The type of effect to run.
                - Can be "create", "update_data", "visible", "invisible", "check", "complete", "init", "hint".
            """
            if self.complete and effect_type != "complete":
                return

            if effect_type not in self.effects.keys():
                return
            for effect in self.effects[effect_type]:
                effect.apply()

        def get_thumbnail(self) -> str:
            """
            Returns the thumbnail of the quest.

            ### Returns:
            1. str: 
                - The thumbnail of the quest.
            """

            return self.thumbnail

    class Goal:
        """
        A Goal is a collection of tasks that are related to a specific topic.

        Parameters:
            key: str
                - The key of the goal.
            name: str
                - The name of the goal.
            description: Union[str, List[str]]
                - The description of the goal.
            effects: Dict[str, List[Effect]]
                - The effects of the goal.
            *tasks: Task
                - The tasks of the goal.

        Attributes:
            key: str
                - The key of the goal.
            name: str
                - The name of the goal.
            description: Union[str, List[str]]
                - The description of the goal.
            effects: Dict[str, List[Effect]]
                - The effects of the goal.
            tasks: Dict[str, Task]
                - The tasks of the goal.
            visible: bool
                - Whether the goal is visible.
            complete: bool
                - Whether the goal is complete.
            quest: Quest
                - The quest that the goal belongs to.
        """

        def __init__(self, key: str, name: str, description: Union[str, List[str]], effects: Dict[str, List[Effect]] = {}, *tasks: Task):
            self.valid = True

            self.key = key
            self.name = name
            
            self.description = description
            if isinstance(description, str):
                self.description = [description]


            self.tasks = {}

            for task in tasks:
                if not task.validate():
                    self.valid = False
                self.tasks[task.key] = task
                task.set_parent(self)

            self.visible = False
            self.complete = False
            self.effects = effects
            self.quest = None

            if not self.validate():
                self.valid = False

            self.run("create")

        def __str__(self):
            return f"    Goal(\n" + \
                f"      key={self.key},\n" + \
                f"      name={self.name},\n" + \
                f"      description={self.description},\n" + \
                f"      effects={self.effects},\n" + \
                f"      tasks=\n" + "\n".join([f"{task}" for task in self.tasks.values()]) + \
                f"      visible={self.visible},\n" + \
                f"      complete={self.complete},\n" + \
                f"    )\n"
        
        def validate(self) -> bool:
            if not isinstance(self.key, str):
                log_error(802, f"Attribute invalid: Goal 'key' invalid type! (should be `str`)")
            elif not isinstance(self.name, str):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'name' invalid type! (should be `str`)")
            elif not isinstance(self.description, list):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'description' invalid type! (should be `list`)")
            elif any(not isinstance(desc, str) for desc in self.description):
                log_error(802, "Attribute invalid: An element in Goal 'description' is invalid type! (Should be `str`)")
            elif not isinstance(self.tasks, dict):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'tasks' invalid type! (should be `Dict(str, Task)`)")
            elif not isinstance(self.visible, bool):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'visible' invalid type! (should be `bool`)")
            elif not isinstance(self.complete, bool):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'complete' invalid type! (should be `bool`)")
            elif not isinstance(self.effects, dict):
                log_error(802, f"Attribute invalid: Goal({self.key}) 'effects' invalid type! (should be `Dict(str, List(Effect))`)")
            elif any(not isinstance(effect_list, list) or any(not isinstance(effect, Effect) for effect in effect_list) for effect_list in self.effects.values()):
                log_error(802, "Attribute invalid: An element in Goal 'effects' is invalid type! ('effects' should be `Dict(str, List(Effect))`)")
            else:
                return True

            return False

        def init_data(self):
            """
            Initializes the data of the goal.
            Sets the parent of the tasks of the goal.
            Also initializes the data of the tasks of the goal.
            """

            global quest_manager

            for task in self.tasks.values():
                task.set_parent(self)
                quest_manager.set_task(task)
                task.init_data()

        def update_data(self, goal: Goal):
            """
            Updates the data of the goal to update potential changes to the goal.
            Also updates the data of the tasks of the goal.
            
            ### Parameters:
            1. goal: Goal
                - The goal to update the data from.
            """

            self.name = goal.name
            self.description = goal.description
            self.effects = goal.effects

            new_tasks = {}
            
            global quest_manager

            for task in goal.tasks.values():
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task

                    quest_manager.register_task(task)
                    task.init_data()
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                    
                new_tasks[task.key].set_parent(self)

                quest_manager.set_task(new_tasks[task.key])

            self.tasks = new_tasks

            self.run("update_data")

        def set_parent(self, quest: Quest):
            """
            Sets the parent of the goal.
            
            ### Parameters:
            1. quest: Quest
                - The quest that the goal belongs to.
            """

            self.quest = quest

        def set_visible(self, is_visible: bool):
            """
            Sets the visibility of the goal.
            
            ### Parameters:
            1. is_visible: bool
                - Whether the goal should be visible.
            """

            if self.complete:
                return
            
            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            """
            Checks if the goal is complete by iterating through all tasks and checking if all tasks are complete.

            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - Additional arguments that may affect the complete status of the goal.

            ### Returns:
            1. bool:
                - True if the goal is complete, False otherwise.
            """

            if self.complete:
                return True

            kwargs["goal_check"] = True
            if all(task.complete or task.check(**kwargs) for task in self.tasks.values()):
                self.set_complete(**kwargs)
                if not get_kwargs("quest_check", False, **kwargs):
                    self.quest.check(**kwargs)
                return True
            self.run("check")
            return False

        def update_complete(self):
            """
            Updates the complete status of the goal.
            Iterates through all tasks and updates the complete status of the goal.
            If all tasks are complete, the goal is complete.
            """

            for task in self.tasks.values():
                if self.complete and not task.complete:
                    task.set_complete()
            if all(task.complete for task in self.tasks.values()) and not self.complete:
                self.set_complete()

        def set_complete(self, **kwargs):
            """
            Sets the complete status of the goal.
            
            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - Additional arguments that may affect the complete status of the goal.
            """

            if self.complete:
                return

            self.complete = True

            for task in self.tasks.values():
                if not task.complete:
                    task.set_complete(**kwargs)
            self.run("complete")

        def run(self, effect_type: str):
            """
            Runs the effect of the goal.
            
            ### Parameters:
            1. effect_type: str
                - The type of effect to run.
                - Can be "create", "update_data", "visible", "invisible", "check", "complete", "init", "hint".
            """
            
            if self.complete and effect_type != "complete":
                return


            if effect_type not in self.effects.keys():
                return
            for effect in self.effects[effect_type]:
                effect.apply()

        def get_progress(self) -> List[str]:
            """
            Returns the progress of the goal.
            
            ### Returns:
            1. List[str]:
                - The progress of the goal in text format.
            """

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
        """
        A Task is a single task that is part of a goal.
        
        Parameters:
            key: str
                - The key of the task.
            name: str
                - The name of the task.
            task_type: str
                - The type of the task.
            description: Union[str, List[str]]
                - The description of the task.
            effects: Dict[str, List[Effect]]
                - The effects of the task.
            goal: Goal
                - The goal that the task belongs to.
                
        Attributes:
            key: str
                - The key of the task.
            name: str
                - The name of the task.
            task_type: str
                - The type of the task.
            description: Union[str, List[str]]
                - The description of the task.
            goal: Goal
                - The goal that the task belongs to.
            active: bool
                - Whether the task is active.
            visible: bool
                - Whether the task is visible.
            complete: bool
                - Whether the task is complete.
            effects: Dict[str, List[Effect]]
                - The effects of the task.

        Methods:
            __init__(self, key: str, name: str, task_type: str, description, effects: Dict[str, List[Effect]] = {}):
                - Initializes the task.
            __str__(self):
                - Returns a string representation of the task.
            init_data(self):
                - Initializes the data of the task.
            update_data(self, task: Task):
                - Updates the data of the task.
            set_parent(self, goal: Goal):
                - Sets the parent of the task.
            activate(self):
                - Activates the task.
            set_visible(self, is_visible: bool):
                - Sets the visibility of the task.
            check(self, **kwargs) -> bool:
                - Checks if the task is complete.
            set_complete(self, **kwargs):
                - Sets the complete status of the task.
            display(self) -> List[str]:
                - Returns the description of the task in text format.
            run(self, effect_type: str):
                - Runs the effect of the task.
        """

        def __init__(self, key: str, name: str, task_type: str, description, effects: Dict[str, List[Effect]] = {}):
            self.valid = True

            self.key = key
            self.name = name
            self.task_type = task_type
            
            self.description = description or []
            if isinstance(description, str):
                self.description = [description]

            self.goal = None
            self.active = False
            self.visible = False
            self.complete = False
            self.effects = effects

            self.run("create")

        def __str__(self):
            return f"        Task(\n" + \
                f"          key={self.key},\n" + \
                f"          name={self.name},\n" + \
                f"          task_type={self.task_type},\n" + \
                f"          description={self.description},\n" + \
                f"          effects={self.effects},\n" + \
                f"          active={self.active},\n" + \
                f"          visible={self.visible},\n" + \
                f"          complete={self.complete},\n" + \
                f"        )\n"

        
        def validate(self) -> bool:
            if not isinstance(self.key, str):
                log_error(802, f"Attribute invalid: Task 'key' invalid type! (should be `str`)")
            elif not isinstance(self.name, str):
                log_error(802, f"Attribute invalid: Task({self.key}) 'name' invalid type! (should be `str`)")
            elif not isinstance(self.task_type, str):
                log_error(802, f"Attribute invalid: Task({self.key}) 'name' invalid type! (should be `str`)")
            elif not isinstance(self.description, list):
                log_error(802, f"Attribute invalid: Task({self.key}) 'description' invalid type! (should be `list`)")
            elif any(not isinstance(desc, str) for desc in self.description):
                log_error(802, "Attribute invalid: An element in Task 'description' is invalid type! (Should be `str`)")
            elif not isinstance(self.active, bool):
                log_error(802, f"Attribute invalid: Task({self.key}) 'active' invalid type! (should be `bool`)")
            elif not isinstance(self.visible, bool):
                log_error(802, f"Attribute invalid: Task({self.key}) 'visible' invalid type! (should be `bool`)")
            elif not isinstance(self.complete, bool):
                log_error(802, f"Attribute invalid: Task({self.key}) 'complete' invalid type! (should be `bool`)")
            elif not isinstance(self.effects, dict):
                log_error(802, f"Attribute invalid: Task({self.key}) 'effects' invalid type! (should be `Dict(str, List(Effect))`)")
            elif any(not isinstance(effect_list, list) or any(not isinstance(effect, Effect) for effect in effect_list) for effect_list in self.effects.values()):
                log_error(802, "Attribute invalid: An element in Task 'effects' is invalid type! ('effects' should be `Dict(str, List(Effect))`)")
            else:
                return True

            return False

        def init_data(self):
            """
            Initializes the data of the task.
            """
            pass

        def update_data(self, task: Task):
            """
            Updates the data of the task to update potential changes to the task.
            
            ### Parameters:
            1. task: Task
                - The task to update the data from.
            """
            self.name = task.name
            self.effects = task.effects

            self.run("update_data")

        def set_parent(self, goal: Goal):
            """
            Sets the parent of the task.
            
            ### Parameters:
            1. goal: Goal
                - The goal that the task belongs to.
            """

            self.goal = goal

        def activate(self):
            """
            Activates the task.
            Also registers the task with the quest manager so that it can be checked.
            """

            if self.complete:
                return

            global quest_manager
            quest_manager.register_task(self)

            self.active = True

            self.run("activate")

        def set_visible(self, is_visible: bool):
            """
            Sets the visibility of the task.
            
            ### Parameters:
            1. is_visible: bool
                - Whether the task should be visible.
            """

            if self.complete:
                return

            self.visible = is_visible
            if self.visible:
                self.run("visible")
            else:
                self.run("invisible")

        def check(self, **kwargs) -> bool:
            """
            Checks if the task is complete by checking if the task is complete or if the task is blocked by a condition.

            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - Additional arguments that may affect the complete status of the task.

            ### Returns:
            1. bool:
                - True if the task is complete, False otherwise.
            """

            if self.complete:
                return True

            self.run("check")
            return False

        def set_complete(self, **kwargs):
            """
            Sets the complete status of the task.
            Also deregisters the task with the quest manager so that it can no longer be checked.
            Also checks the goal if the completion of the task leads to the completion of the goal.
            
            ### Parameters:
            1. **kwargs: Dict[str, Any]
                - Additional arguments that may affect the complete status of the task.
            """

            if self.complete:
                return

            self.complete = True

            global quest_manager
            quest_manager.deregister_task(self)

            if not get_kwargs("goal_check", False, **kwargs):
                self.goal.check(**kwargs)
            self.run("complete")

        def display(self) -> List[str]:
            """
            Returns the description of the task in text format.
            
            ### Returns:
            1. List[str]:
                - The description of the task in text format.
            """

            return self.description

        def run(self, effect_type: str):
            """
            Runs the effect of the task.
            
            ### Parameters:
            1. effect_type: str
                - The type of effect to run.
                - Can be "create", "update_data", "visible", "invisible", "check", "complete", "init", "hint".
            """
            
            if self.complete and effect_type != "complete":
                return

            if effect_type not in self.effects.keys():
                return
            for effect in self.effects[effect_type]:
                effect.apply()

    class TaskGroup(Task):
        """
        Subclass of Task.

        A TaskGroup is a collection of tasks that are related to a specific topic.
        It can be used to group tasks that are related to a specific topic along with a description.
        
        Parameters:
            key: str
                - The key of the task group.
            name: str
                - The name of the task group.
            description: Union[str, List[str]]
                - The description of the task group.
            effects: Dict[str, List[Effect]]
                - The effects of the task group.
            *tasks: Task
                - The tasks of the task group.

        Attributes:
            tasks: Dict[str, Task]
                - The tasks of the task group.

        Methods:
            __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, *tasks: Task):
                - Initializes the task group.
            __str__(self):
                - Returns a string representation of the task group.
            update_data(self, taskCat: Task):
                - Updates the data of the task group.
            check(self, **kwargs) -> bool:
                - Checks if the task group is complete.
        """

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, *tasks: Task):
            if key is None:
                return

            super().__init__(key, name, "None", description, effects)

            self.tasks = {task.key: task for task in tasks}

            if not self.validate():
                self.valid = False

        def __str__(self):
            return f"        TaskGroup(\n" + \
                f"          key={self.key},\n" + \
                f"          name={self.name},\n" + \
                f"          description={self.description},\n" + \
                f"          effects={self.effects},\n" + \
                f"          tasks=\n" + "\n".join([f"{task}" for task in self.tasks.values()]) + \
                f"        )\n"
        
        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.tasks, dict):
                log_error(802, f"Attribute invalid: TaskGroup({self.key}) 'tasks' invalid type! (should be `Dict(str, Task)`)")
            else:
                return True

            return False

        def update_data(self, taskCat: Task):
            self.description = taskCat.description

            new_tasks = {}

            for task in taskCat.tasks.values():
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task
                    
                    global quest_manager
                    quest_manager.register_task(task)
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                task.set_parent(self)
            self.tasks = new_tasks

            super().update_data(taskCat)

        def check(self, **kwargs) -> bool:
            if all(task.complete or task.check(**kwargs) for task in self.tasks.values()):
                self.set_complete()
                return True
            return super().check(**kwargs)

    class TaskOptionalGroup(Task):
        """
        Subclass of Task.

        A TaskOptionalGroup is a collection of tasks that are optional and do not need to be completed.
        It can be used to group tasks that are optional and do not need to be completed along with a description.
        
        Parameters:
            key: str
                - The key of the task optional group.
            name: str
                - The name of the task optional group.
            description: Union[str, List[str]]
                - The description of the task optional group.
            effects: Dict[str, List[Effect]]
                - The effects of the task optional group.
            *tasks: Task
                - The tasks of the task optional group.

        Attributes:
            tasks: Dict[str, Task]
                - The tasks of the task optional group.
        """

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, *tasks: Task):
            if key is None:
                return

            super().__init__(key, name, "None", description, effects)

            self.tasks = {task.key: task for task in tasks}
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.tasks, dict):
                log_error(802, f"Attribute invalid: TaskOptionalGroup({self.key}) 'tasks' invalid type! (should be `Dict(str, Task)`)")
            else:
                return True

            return False

        def update_data(self, taskCat: Task):
            self.description = taskCat.description

            new_tasks = {}

            for task in taskCat.tasks.values():
                if task.key not in self.tasks.keys():
                    new_tasks[task.key] = task
                    
                    global quest_manager
                    quest_manager.register_task(task)
                else:
                    new_tasks[task.key] = self.tasks[task.key]
                    new_tasks[task.key].update_data(task)
                task.set_parent(self)
            self.tasks = new_tasks

            super().update_data(taskCat)

        def check(self, **kwargs) -> bool:
            for task in self.tasks:
                task.check(**kwargs)
            return True

        def display(self) -> List[str]:
            output = self.description
            output.append("The tasks in this group are optional and do not need to be completed.")
            return output

    @deprecated(version='0.2.2', reason="Use class TaskOptionalGroup instead")
    class OptionalTask(Task):
        # DO NOT USE THIS CLASS, USE TaskOptionalGroup INSTEAD
        # THIS CLASS IS DEPRECATED AND WILL BE REMOVED IN THE FUTURE

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, task: Task = None):
            super().__init__(key, name, "optional", description, effects) 

    @deprecated(version='0.2.2', reason="Use description fields of Tasks and TaskGroups instead")
    class LabelTask(Task):
        # DO NOT USE THIS CLASS, USE description fields of Tasks and TaskGroups instead
        # THIS CLASS IS DEPRECATED AND WILL BE REMOVED IN THE FUTURE

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, task: Task = None):
            super().__init__(key, name, "label", description, effects) 


    class EventTask(Task):
        """
        Subclass of Task.

        A Task that tracks the number of times an event has occurred.
        
        Parameters:
            key: str
                - The key of the event task.
            name: str
                - The name of the event task.
            description: Union[str, List[str]]
                - The description of the event task.
            effects: Dict[str, List[Effect]]
                - The effects of the event task.
            event: str
                - The name of the event to track.
            min_seen: int
                - The minimum number of times the event must occur for the task to be complete.

        Attributes:
            event: str
                - The name of the event to track.
            min_seen: int
                - The minimum number of times the event must occur for the task to be complete.

        Methods:
            __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, event: str = None, min_seen = 1):
                - Initializes the event task.
            update_data(self, task: Task):
                - Updates the data of the event task.
            check(self, **kwargs) -> bool:
                - Checks if the event task is complete.
            display(self) -> List[str]:
                - Returns the description of the event task in text format.
        """

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, event: str = None, min_seen = 1):
            if key is None:
                return

            super().__init__(key, name, "event", description, effects)
            self.event = event
            self.min_seen = min_seen
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.event, str):
                log_error(802, f"Attribute invalid: EventTask({self.key}) 'event' invalid type! (should be `str`)")
            elif not isinstance(self.min_seen, int):
                log_error(802, f"Attribute invalid: EventTask({self.key}) 'min_seen' invalid type! (should be `int`)")
            else:
                return True

            return False

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
        """
        Subclass of Task.
        
        A Task that tracks the number of times an event has occurred with specific values.
        
        Parameters:
            key: str
                - The key of the event value task.
            name: str
                - The name of the event value task.
            description: Union[str, List[str]]
                - The description of the event value task.
            effects: Dict[str, List[Effect]]
                - The effects of the event value task.
            event: str
                - The name of the event to track.
            min_seen: int
                - The minimum number of times the event must occur for the task to be complete.
            values: Dict[str, Any]
                - The values that the event must have to count towards the task.

        Attributes:
            event: str
                - The name of the event to track.
            min_seen: int
                - The minimum number of times the event must occur for the task to be complete.
            seen: int
                - The number of times the event has occurred.
            values: Dict[str, Union[str, int, bool]]
                - The values that the event must have to count towards the task.

        Methods:
            __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, event: str = None, min_seen = 1, values = {}):
                - Initializes the event value task.
            update_data(self, task: Task):
                - Updates the data of the event value task.
            check(self, **kwargs) -> bool:
                - Checks if the event value task is complete.
            display(self) -> List[str]:
                - Returns the description of the event value task in text format.
        """
        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, event: str = None, min_seen = 1, values: Dict[str, Union[str, int, bool]] = {}):
            if key is None:
                return

            super().__init__(key, name, "event", description, effects)
            self.event = event
            self.min_seen = min_seen
            self.seen = 0
            self.values = values
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.event, str):
                log_error(802, f"Attribute invalid: EventValueTask({self.key}) 'event' invalid type! (should be `str`)")
            elif not isinstance(self.min_seen, int):
                log_error(802, f"Attribute invalid: EventValueTask({self.key}) 'min_seen' invalid type! (should be `int`)")
            elif not isinstance(self.values, dict):
                log_error(802, f"Attribute invalid: EventValueTask({self.key}) 'values' invalid type! (should be `Dict(str, Any)`)")
            elif any(not isinstance(val, str) and not isinstance(val, int) and not isinstance(val, bool) for val in self.values.values()):
                log_error(802, f"Attribute invalid: An element in EventValueTask({self.key}) 'values' is invalid type! (should be `str, int or bool`)")
            else:
                return True

            return False

        def update_data(self, task: Task):
            self.event = task.event
            self.min_seen = task.min_seen

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
        """
        Subclass of Task.

        A Task that tracks whether a condition is fulfilled.
        
        Parameters:
            key: str
                - The key of the condition task.
            name: str
                - The name of the condition task.
            task_type: str
                - The type of the condition task.
            description: Union[str, List[str]]
                - The description of the condition task.
            effects: Dict[str, List[Effect]]
                - The effects of the condition task.
            condition: Condition
                - The condition to track.

        Attributes:
            condition: Condition
                - The condition to track.

        Methods:
            __init__(self, key: str = None, name: str = None, task_type: str = None, description = None, effects: Dict[str, List[Effect]] = None, condition: Condition = None):
                - Initializes the condition task.
            update_data(self, task: Task):
                - Updates the data of the condition task.
            check(self, **kwargs) -> bool:
                - Checks if the condition task is complete.
            display(self) -> List[str]:
                - Returns the description of the condition task in text format.
        """

        def __init__(self, key: str = None, name: str = None, task_type: str = None, description = None, effects: Dict[str, List[Effect]] = None, condition: Condition = None):
            if key is None:
                return

            super().__init__(key, name, task_type, description, effects)
            self.condition = condition
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not issubclass(type(self.condition), Condition):
                log_error(802, f"Attribute invalid: ConditionTask({self.key}) 'condition' invalid type! (should be a subclass of `Condition`)")
            else:
                return True

            return False

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
        """
        Subclass of Task.

        A Task that has to be triggered manually.

        Parameters:
            key: str
                - The key of the trigger task.
            description: Union[str, List[str]]
                - The description of the trigger task.
            effects: Dict[str, List[Effect]]
                - The effects of the trigger task.

        Methods:
            __init__(self, key: str = None, description = None, effects: Dict[str, List[Effect]] = None):
                - Initializes the trigger task.
            check(self, **kwargs) -> bool:
                - Checks if the trigger task is complete.
        """

        def __init__(self, key: str = None, description = None, effects: Dict[str, Effect] = None):
            if key is None:
                return

            super().__init__(key, key, "trigger", description, effects)

        def check(self, **kwargs):
            if get_kwargs('name', **kwargs) == self.key:
                self.set_complete()
                return True

            return super().check(**kwargs)

    class JournalUnlockTask(Task):
        """
        Subclass of Task.

        A Task that tracks whether a journal object is unlocked.
        
        Parameters:
            key: str
                - The key of the journal unlock task.
            name: str
                - The name of the journal unlock task.
            description: Union[str, List[str]]
                - The description of the journal unlock task.
            effects: Dict[str, List[Effect]]
                - The effects of the journal unlock task.
            journal_obj: str
                - The name of the journal object to unlock.

        Attributes:
            journal_obj: str
                - The name of the journal object to unlock.

        Methods:
            __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None):
                - Initializes the journal unlock task.
            update_data(self, task: Task):
                - Updates the data of the journal unlock task.
            check(self, **kwargs) -> bool:
                - Checks if the journal unlock task is complete.
            display(self) -> List[str]:
                - Returns the description of the journal unlock task in text format.
        """

        def __init__(self, key: str = None, name: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None):
            if key is None:
                return

            super().__init__(key, name, "journal_unlock", description, effects)
            self.journal_obj = journal_obj
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.journal_obj, str):
                log_error(802, f"Attribute invalid: JournalUnlockTask({self.key}) 'journal_obj' invalid type! (should be `str`)")
            else:
                return True

            return False

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
            if self.complete:
                output.append("- Unlock {color=#00a000}" + self.name + "{/color} ")
            else:
                output.append("- Unlock {color=#a00000}" + self.name + "{/color} ")
            return output

    class JournalUpgradeTask(Task):
        """
        Subclass of Task.

        A Task that tracks whether a journal object is upgraded to a specific level.
        
        Parameters:
            key: str
                - The key of the journal upgrade task.
            name: str
                - The name of the journal upgrade task.
            description: Union[str, List[str]]
                - The description of the journal upgrade task.
            effects: Dict[str, List[Effect]]
                - The effects of the journal upgrade task.
            journal_obj: str
                - The name of the journal object to upgrade.
            min_level: int
                - The minimum level the journal object must be upgraded to.

        Attributes:
            journal_obj: str
                - The name of the journal object to upgrade.
            min_level: int
                - The minimum level the journal object must be upgraded to.

        Methods:
            __init__(self, key: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None, min_level = 1):
                - Initializes the journal upgrade task.
            update_data(self, task: Task):
                - Updates the data of the journal upgrade task.
            check(self, **kwargs) -> bool:
                - Checks if the journal upgrade task is complete.
            display(self) -> List[str]:
                - Returns the description of the journal upgrade task in text format.
        """

        def __init__(self, key: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None, min_level = 1):
            if key is None:
                return

            super().__init__(key, get_translation(self.journal_obj), "journal_upgrade", description, effects)
            self.journal_obj = journal_obj
            self.min_level = min_level
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.journal_obj, str):
                log_error(802, f"Attribute invalid: JournalUpgradeTask({self.key}) 'journal_obj' invalid type! (should be `str`)")
            elif not isinstance(self.min_level, int):
                log_error(802, f"Attribute invalid: JournalUpgradeTask({self.key}) 'min_level' invalid type! (should be `int`)")
            else:
                return True

            return False

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
            if self.complete:
                output.append("- Upgrade " + self.name + " to Level {color=#00a000}" + self._target_level + "{/color} ")
            else:
                output.append("- Upgrade " + self.name + " to Level {color=#a00000}" + self._target_level + "{/color} ")
            return output

    class ScheduleVotingTask(Task):
        """
        Subclass of Task.

        A Task that tracks whether a proposal is scheduled for voting.
        
        Parameters:
            key: str
                - The key of the schedule voting task.
            description: Union[str, List[str]]
                - The description of the schedule voting task.
            effects: Dict[str, List[Effect]]
                - The effects of the schedule voting task.
            journal_obj: str
                - The name of the journal object to schedule for voting.
            vote_type: str
                - The type of vote to schedule.
                - One of the following values are valid: "unlock, upgrade"

        Attributes:
            journal_obj: str
                - The name of the journal object to schedule for voting.
            vote_type: str
                - The type of vote to schedule.

        Methods:
            __init__(self, key: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None, vote_type: str = None):
                - Initializes the schedule voting task.
            update_data(self, task: Task):
                - Updates the data of the schedule voting task.
            check(self, **kwargs) -> bool:
                - Checks if the schedule voting task is complete.
            display(self) -> List[str]:
                - Returns the description of the schedule voting task in text format.
        """

        def __init__(self, key: str = None, description = None, effects: Dict[str, List[Effect]] = None, journal_obj: str = None, vote_type: str = None):
            if key is None:
                return

            super().__init__(key, get_translation(self._journal_obj), "schedule_voting", description, effects)
            self.journal_obj = journal_obj
            self.vote_type = vote_type
            
            if not self.validate():
                self.valid = False

        def validate(self) -> bool:
            if not super().validate():
                return False

            if not isinstance(self.journal_obj, str):
                log_error(802, f"Attribute invalid: ScheduleVotingTask({self.key}) 'journal_obj' invalid type! (should be `str`)")
            elif not isinstance(self.vote_type, str):
                log_error(802, f"Attribute invalid: ScheduleVotingTask({self.key}) 'vote_type' invalid type! (should be `str`)")
            elif self.vote_type not in ["unlock", "upgrade"]:
                log_error(803, f"Attribute invalid: ScheduleVotingTask({self.key}) 'vote_type' invalid value! (possible values: 'unlock', 'upgrade')")
            else:
                return True

            return False

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
            if self.complete:
                output.append("- Schedule " + self.name + " for {color=#00a000}" + self.vote_type + "{/color}")
            else:
                output.append("- Schedule " + self.name + " for {color=#a00000}" + self.vote_type + "{/color}")
            return output

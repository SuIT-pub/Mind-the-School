init -1 python:
    from abc import ABC,abstractmethod
    from deprecated import deprecated

    def call_effects(*effects: Effect, **kwargs):
        """
        Applies all effects passed as arguments.

        ### Parameters:
        1. *effects: Effect
            - Effects to be applied.
        """

        for effect in effects:
            kwargs = effect.apply(**kwargs)

        return kwargs

    class EffectStorage:
        def __init__(self, *effects: Effect):
            self.effects = list(effects)

        def __len__(self):
            return len(self.effects)

        def apply(self, **kwargs):
            for effect in self.effects:
                effect.apply(**kwargs)

        def revert(self, **kwargs):
            for effect in self.effects:
                effect.revert(**kwargs)

        def find_by_type(self, type: str):
            output = []
            for effect in self.effects:
                output.extend(effect.find_by_type(type))
            return output

    class Effect(ABC):
        """
        Abstract class for all effects.

        ### Attributes:
        1. name: str
            - Name of the effect.

        ### Methods:
        1. apply(**kwargs)
            - Applies the effect.
        """

        def __init__(self, name: str, *options: Option):
            self.name = name
            self.options = OptionSet(*options)

        @abstractmethod
        def __str__(self):
            pass

        @property
        def _type(self) -> str:
            return "effect"
        
        def find_by_type(self, type: str):
            if self._type == type:
                return [self]
            return []

        @abstractmethod
        def apply(self, **kwargs):
            pass

        def revert(self, **kwargs):
            pass

    @deprecated(version='0.2.3', reason="Replaced by Unlockable effects; kept for save compatibility.")
    class RuleEffect(Effect):
        """Legacy rule unlock effect. No-op; kept so old saves can unpickle."""

        def __init__(self, name: str, rule=None, *options: Option):
            super().__init__(name, *options)
            self.rule = rule

        @property
        def _type(self) -> str:
            return "rule"

        def __str__(self):
            return f"{self.rule}"

        def apply(self, **kwargs):
            return kwargs

    @deprecated(version='0.2.3', reason="Replaced by Unlockable effects; kept for save compatibility.")
    class ClubEffect(Effect):
        """Legacy club unlock effect. No-op; kept so old saves can unpickle."""

        def __init__(self, name: str, club=None, *options: Option):
            super().__init__(name, *options)
            self.club = club

        @property
        def _type(self) -> str:
            return "club"

        def __str__(self):
            return f"{self.club}"

        def apply(self, **kwargs):
            return kwargs

    @deprecated(version='0.2.3', reason="Replaced by Unlockable effects; kept for save compatibility.")
    class BuildingEffect(Effect):
        """Legacy building unlock effect. No-op; kept so old saves can unpickle."""

        def __init__(self, name: str, building=None, *options: Option):
            super().__init__(name, *options)
            self.building = building

        @property
        def _type(self) -> str:
            return "building"

        def __str__(self):
            return f"{self.building}"

        def apply(self, **kwargs):
            return kwargs

    class LevelEffect(Effect):
        """
        Changes the level of a character.

        ### Attributes:
        1. value: int
            - Value to be added to the level.
        2. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current level.
            - SET sets the level to the value.
        """

        def __init__(self, name: str, value: int, mode: str = "ADD", char_obj: Char = None, *options: Option):
            super().__init__(name, *options)
            self.mode = mode
            self.value = value

            if isinstance(char_obj, str):
                char_obj = get_character_by_key(char_obj)

            self.char_obj = char_obj

        @property
        def _type(self) -> str:
            return "level"

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            char_obj = self.char_obj
            if char_obj == None:
                char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            if self.mode == "SET":
                char_obj.set_level(self.value)
            if self.mode == "ADD":
                char_obj.set_level(char_obj.get_level() + self.value)
            return kwargs

    class StatEffect(Effect):
        """
        Changes the value of a stat.

        ### Attributes:
        1. stat: str
            - Name of the stat.
        2. value: num
            - Value to be added to the stat.
        3. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current stat.
            - SET sets the stat to the value.
        """

        def __init__(self, name: str, stat: str, value: num, mode: str = "ADD", *options: Option):
            super().__init__(name, *options)
            self.stat = stat
            self.mode = mode
            self.value = value

        @property
        def _type(self) -> str:
            return "stat"

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            stat_obj = char_obj.get_stat(self.stat)
            if stat_obj == None:
                return

            if self.mode == "SET":
                stat_obj.change_value_to(self.value, char_obj.get_level())
            if self.mode == "ADD":
                stat_obj.change_value(self.value, char_obj.get_level())
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs

            char_obj = get_kwargs("char_obj", **kwargs)
            if char_obj == None:
                return

            stat_obj = char_obj.get_stat(self.stat)
            if stat_obj == None:
                return

            if self.mode == "SET":
                stat_obj.change_value_to(-self.value, char_obj.get_level())
            if self.mode == "ADD":
                stat_obj.change_value(-self.value, char_obj.get_level())
            return kwargs

    class MoneyEffect(Effect):
        """
        Changes the value of money.

        ### Attributes:
        1. value: num
            - Value to be added to the money.
        2. mode: str (Default "ADD")
            - Mode of the effect. Can be "ADD" or "SET".
            - ADD adds the value to the current money.
            - SET sets the money to the value.
        """

        def __init__(self, name: str, value: num, mode: str = "ADD", *options: Option):
            super().__init__(name, *options)
            self.mode = mode
            self.value = value

        @property
        def _type(self) -> str:
            return "money"

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            if self.mode == "SET":
                money.change_value_to(self.value)
                return kwargs

            if self.mode == "ADD":
                if self.options.has_option("MoneyEscrow"):
                    escrow = self.options.get_option("MoneyEscrow")
                    stash_key = getattr(escrow, "stash_key", None)
                    if stash_key and stash_key in reserved_money:
                        # Wallet already reduced at Schedule Vote; finalize the stash.
                        spend_reserved_money(stash_key)
                        return kwargs
                money.change_value(self.value)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs

            if self.mode == "SET":
                money.change_value_to(-self.value)
            if self.mode == "ADD":
                money.change_value(-self.value)
            return kwargs

    @deprecated(version='0.2.2', reason="Highly unstable — do not use.")
    class AddTempTimeEventEffect(Effect):
        """
        Adds a temporary time event.

        ### Attributes:
        1. event: Event
            - Event to be added.
        """

        def __init__(self, event: Event, *options: Option):
            super().__init__(event.get_name(), *options)
            self.event = event

        @property
        def _type(self) -> str:
            return "event"

        def __str__(self):
            return f"{self.event.get_name()}"

        def apply(self, **kwargs):
            
            return kwargs

    @deprecated(version='0.2.2', reason="Highly unstable — do not use.")
    class RemoveTempTimeEventEffect(Effect):
        """
        Removes a temporary time event.

        ### Attributes:
        1. id: str
            - ID of the event to be removed.
        """

        def __init__(self, id: str, *options: Option):
            super().__init__(id, *options)

        @property
        def _type(self) -> str:
            return "event"

        def __str__(self):
            return f"{self.id}"

        def apply(self, **kwargs):
            
            return kwargs

    class BlockBuildingEffect(Effect):
        """
        Blocks a building.

        ### Attributes:
        1. building_name: str
            - Name of the building to be blocked.
        2. is_blocking: bool (Default True)
            - If True, the building will be blocked.
            - If False, the building will be unblocked.
        """

        def __init__(self, name: str, building_name: str, is_blocking: bool = True, *options: Option):
            super().__init__(name, *options)
            self.building_name = building_name
            self.is_blocking = is_blocking

        @property
        def _type(self) -> str:
            return "block_building"

        def __str__(self):
            return f"{self.building_name}"

        def apply(self, **kwargs):
            if self.is_blocking:
                add_building_collection_key(self.building_name, "closed", self.name)
            else:
                remove_building_collection_key(self.building_name, "closed", self.name)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs

            if self.is_blocking:
                remove_building_collection_key(self.building_name, "closed", self.name)
            else:
                add_building_collection_key(self.building_name, "closed", self.name)
            return kwargs

    class EventEffect(Effect):
        """
        Calls an event.

        ### Attributes:
        1. event: Event | EventStorage | str
            - Event to be called.
            - Event calls just the event.
            - EventStorage calls all available events.
            - str calls the label.
        """

        def __init__(self, event: Event | EventStorage | str, *options: Option):
            name = event
            if not isinstance(event, str):
                name = event.get_name()
            super().__init__(name, *options)
            self.event = event

        @property
        def _type(self) -> str:
            return "event"

        def __str__(self):
            if isinstance(self.event, Event):
                return f"{self.event.get_name()}"
            if isinstance(self.event, EventStorage):
                return f"{self.event.get_name()}"
            return self.event

        def apply(self, **kwargs):
            if isinstance(self.event, EventStorage):
                renpy.call('call_available_event', self.event, **kwargs)

            if isinstance(self.event, Event):
                self.event.call(**kwargs)
                # event_obj = self.event.get_event()
                # for event in event_obj:
                #     renpy.call(event, **kwargs)

            if isinstance(self.event, str):
                renpy.call(self.event, **kwargs)

    class EventSelectEffect(Effect):
        """
        Calls an event from a list of events.

        ### Attributes:
        1. event_list: list[Event]
            - List of events to be called.
        """

        def __init__(self, event: str | Event | EventStorage | List[Event | str], *options: Option):
            events = []
            if isinstance(event, str):
                events = [get_event_from_register(event)]
                super().__init__(event, *options)
            elif isinstance(event, Event):
                events = [event]
                super().__init__(event.get_name(), *options)
            elif isinstance(event, EventStorage):
                events = event.get_events()
                super().__init__(event.get_name(), *options)
            elif isinstance(event, list):
                for e in event:
                    if isinstance(e, str):
                        events.append(get_event_from_register(e))
                    else:
                        events.append(e)
                super().__init__(events[0].get_name(), *options)

            self.event = events

        @property
        def _type(self) -> str:
            return "event_select"

        def __str__(self):
            return f"{self.name}"

        def apply(self, **kwargs):
            if len(self.event) == 1:
                self.event[0].call(**kwargs)
            else:
                renpy.call('open_bg_image_menu', self.event, from_current=False, **kwargs)

    class ValueEffect(Effect):
        """
        Changes a value in the gameData.

        ### Attributes:
        1. key: str
            - Key of the value.
        2. value: val | bool
            - Value to be added to the key in gameData.
        """

        def __init__(self, key: str, value: val | bool, *options: Option):
            super().__init__(key, *options)
            self.key = key
            self.value = value
            self.prev_value = None

        @property
        def _type(self) -> str:
            return "value"

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            if self.key in gameData.keys():
                self.prev_value = gameData[self.key]
            gameData[self.key] = self.value
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            if self.prev_value != None:
                gameData[self.key] = self.prev_value
            return kwargs

    class ProgressEffect(Effect):
        """
        Changes a progress in the Event Series.

        ### Attributes:
        1. key: str
            - Key of the progress.
        2. value: int
            - The progress of the Event Series with the key
        """

        def __init__(self, key: str, value: int = 1, *options: Option):
            super().__init__(key, *options)
            self.key = key
            self.value = value
            self.prev_value = None

        @property
        def _type(self) -> str:
            return "progress"

        def __str__(self):
            return f"{self.value}"

        def apply(self, **kwargs):
            if self.key in gameData.keys():
                self.prev_value = gameData[self.key]
            if self.key not in gameData.keys():
                gameData[self.key] = 0
            gameData[self.key] += self.value
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            if self.prev_value != None:
                gameData[self.key] = self.prev_value
            return kwargs

    class ModifierEffect(Effect):
        """
        Adds a modifier to a stat.

        ### Attributes:
        1. key: str
            - Key of the modifier.
        2. stat: str
            - Name of the stat.
        3. mod_obj: Modifier_Obj
            - Modifier to be added.
        4. collection: str (Default "default")
            - Collection of the modifier.
        """

        def __init__(self, key: str, stat: str, mod_obj: Modifier_Obj, collection: str = 'default', *options: Option):
            super().__init__(key, *options)
            self.key = key
            self.stat = stat
            self.modifier = mod_obj
            self.collection = collection

        @property
        def _type(self) -> str:
            return "modifier"

        def __str__(self):
            return f"{self.key}"

        def apply(self, **kwargs):
            set_modifier(self.key, self.modifier, stat = self.stat, collection = self.collection)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            remove_modifier(self.key, stat = self.stat, collection = self.collection)
            return kwargs


    class RemoveModifierEffect(Effect):
        """
        Removes a modifier such as Monthly Income/Costs or Stats.
        Essentially a Wrapper class for remove_modifier()

        ### Attributes:
        1. key: str
            - Key of the modifier.
        2. stat: str
            - Name of the stat.
        3. mod_obj: Modifier_Obj
            - Modifier to be added.
        4. char_obj: Char (Default None)
            - Character from which the modifier will be removed.
        5. collection: str (Default "default")
            - Collection of the modifier.
        """

        def __init__(self, key: str, stat: str, collection: str = 'default'):
            super().__init__(key)
            self.key = key
            self.stat = stat
            self.collection = collection

        @property
        def _type(self) -> str:
            return "remove_modifier"

        def __str__(self):
            return f"{self.key}"

        def apply(self, **kwargs):
            remove_modifier(self.key, stat = self.stat, collection = self.collection)
            return kwargs

    class ChangeKwargsEffect(Effect):
        def __init__(self, key: str, value: Any):
            super().__init__(key)
            self.key = key
            self.value = value

        @property
        def _type(self) -> str:
            return "change_kwargs"

        def __str__(self):
            return f"{self.key}"

        def apply(self, **kwargs):
            kwargs[self.key] = self.value
            return kwargs

    class SetProficiencyEffect(Effect):
        def __init__(self, subject: str, *, level = 0, xp = 0):
            super().__init__(subject)
            self.level = level
            self.xp = xp

        @property
        def _type(self) -> str:
            return "set_proficiency"

        def __str__(self):
            return f"set_proficiency_{self.level}_{self.xp}"

        def apply(self, **kwargs):
            if self.level > 0:
                set_headmaster_proficiency_level(self.name, self.level * 100)
            if self.xp > 0:
                set_headmaster_proficiency_xp(self.name, self.xp)
            return kwargs

    class QuestCompleteEffect(Effect):
        def __init__(self, quest_type: str, key: str):
            super().__init__(f"complete_quest_{quest_type}_{key}")
            self.quest_type = quest_type
            self.key = key

        @property
        def _type(self) -> str:
            return "complete_quest"

        def __str__(self):
            return f"complete_quest_{self.quest_type}_{self.key}"

        def apply(self, **kwargs):
            global quest_manager

            if self.quest_type == "quest":
                quest = quest_manager.get_quest(self.key)
                if quest != None:
                    quest.set_complete()
            if self.quest_type == "goal":
                goal = quest_manager.get_goal(self.key)
                if goal != None:
                    goal.set_complete()
            if self.quest_type == "task":
                task = quest_manager.get_task(self.key)
                if task != None:
                    task.set_complete()

            return kwargs

    class QuestVisibleEffect(Effect):
        def __init__(self, quest_type: str, key: str):
            super().__init__(f"visible_quest_{quest_type}_{key}")
            self.quest_type = quest_type
            self.key = key

        @property
        def _type(self) -> str:
            return "visible_quest"

        def __str__(self):
            return f"visible_quest_{self.quest_type}_{self.key}"

        def apply(self, **kwargs):
            global quest_manager

            if self.quest_type == "quest":
                quest = quest_manager.get_quest(self.key)
                if quest != None:
                    quest.set_visible(True)
            if self.quest_type == "goal":
                goal = quest_manager.get_goal(self.key)
                if goal != None:
                    goal.set_visible(True)
            if self.quest_type == "task":
                task = quest_manager.get_task(self.key)
                if task != None:
                    task.set_visible(True)
            return kwargs

    class QuestInvisibleEffect(Effect):
        def __init__(self, quest_type: str, key: str):
            super().__init__(f"invisible_quest_{quest_type}_{key}")
            self.quest_type = quest_type
            self.key = key

        @property
        def _type(self) -> str:
            return "invisible_quest"

        def __str__(self):
            return f"invisible_quest_{self.quest_type}_{self.key}"

        def apply(self, **kwargs):
            global quest_manager

            if self.quest_type == "quest":
                quest = quest_manager.get_quest(self.key)
                if quest != None:
                    quest.set_visible(False)
            if self.quest_type == "goal":
                goal = quest_manager.get_goal(self.key)
                if goal != None:
                    goal.set_visible(False)
            if self.quest_type == "task":
                task = quest_manager.get_task(self.key)
                if task != None:
                    task.set_visible(False)
            return kwargs

    class QuestActivateEffect(Effect):
        def __init__(self, key: str):
            super().__init__(f"activate_quest_task_{key}")
            self.key = key

        @property
        def _type(self) -> str:
            return "activate_quest_task"

        def __str__(self):
            return f"activate_quest_task_{self.key}"

        def apply(self, **kwargs):
            global quest_manager
            task = quest_manager.get_task(self.key)
            if task != None:
                task.activate()
            return kwargs

    class NotificationEffect(Effect):
        def __init__(self, message: str):
            super().__init__(f"notification_{message}")
            self.message = message

        @property
        def _type(self) -> str:
            return "notification"

        def __str__(self):
            return f"notification_{self.message}"

        def apply(self, **kwargs):
            add_notify_message(self.message)
            return kwargs

    class DummyEffect(Effect):
        def __init__(self, *options: Option):
            super().__init__("dummy", *options)

        @property
        def _type(self) -> str:
            return "dummy"

        def __str__(self):
            return "dummy"

        def apply(self, **kwargs):
            return kwargs

    class ScheduleVoteEffect(Effect):
        """
        Queues an Unlockable for the next Friday PTA meeting.

        Stores the live Unlockable instance in ``voteProposal``.
        """

        def __init__(self, situation_key: str, *options: Option):
            super().__init__("ScheduleVoteEffect", *options)
            self.situation_key = situation_key

        @property
        def _type(self) -> str:
            return "schedule_vote"

        def __str__(self):
            return f"Schedule vote for {self.situation_key}"

        def apply(self, **kwargs):
            if get_game_data("voteProposal") is not None:
                return kwargs
            unlockable = None
            if situation_manager is not None:
                unlockable = situation_manager.get_situation(self.situation_key)
            if not isinstance(unlockable, Unlockable):
                return kwargs
            set_game_data("voteProposal", unlockable)
            return kwargs

        def revert(self, **kwargs):
            proposal = get_game_data("voteProposal")
            if isinstance(proposal, Unlockable) and proposal.key == self.situation_key:
                proposal.release_vote_money()
                set_game_data("voteProposal", None)
            return kwargs

    
    class UnlockableUnlockEffect(Effect):
        """
        Marks an unlockable as unlocked in game data when its situation resolves positively.
        For grouped unlockables also writes the group level.
        """

        def __init__(self, unlockable_situation_key: str, group_key: str = None, group_index: int = -1, *options: Option):
            super().__init__("unlockable_unlock", *options)
            self.unlockable_situation_key = unlockable_situation_key
            self.group_key = group_key
            self.group_index = group_index

        @property
        def _type(self) -> str:
            return "unlockable_unlock"

        def __str__(self):
            return f"Unlock {self.unlockable_situation_key}"

        def apply(self, **kwargs):
            unlockable = None
            if situation_manager is not None:
                unlockable = situation_manager.get_situation(self.unlockable_situation_key)
            if (
                isinstance(unlockable, Unlockable)
                and self.group_key is not None
                and self.group_index != -1
            ):
                unlockable.apply_group_upgrade_transition(**kwargs)

            set_game_data(self.unlockable_situation_key + "_unlocked", True)
            if self.group_key is not None and self.group_index != -1:
                set_game_data(self.group_key + "_level", self.group_index)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            remove_game_data(self.unlockable_situation_key + "_unlocked")
            if self.group_key is not None and self.group_index != -1:
                prev_level = self.group_index - 1
                if prev_level >= 1:
                    set_game_data(self.group_key + "_level", prev_level)
                else:
                    remove_game_data(self.group_key + "_level")
            return kwargs

    class BuildingOpenEffect(Effect):
        def __init__(self, building_key: str, is_open: bool = True, *options: Option):
            super().__init__(f"building_open_{building_key}")
            self.building_key = building_key
            self.is_open = is_open

        @property
        def _type(self) -> str:
            return "building_open"

        def __str__(self):
            return f"BuildingOpenEffect({self.building_key})"

        def apply(self, **kwargs):
            if self.is_open:
                add_building_collection_key(self.building_key, "open", self.name)
            else:
                remove_building_collection_key(self.building_key, "open", self.name)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            if self.is_open:
                remove_building_collection_key(self.building_key, "open", self.name)
            else:
                add_building_collection_key(self.building_key, "open", self.name)
            return kwargs

    class BuildingCloseEffect(Effect):
        def __init__(self, building_key: str, is_close: bool = True, *options: Option):
            super().__init__(f"building_close_{building_key}")
            self.building_key = building_key
            self.is_close = is_close
            
        @property
        def _type(self) -> str:
            return "building_close"

        def __str__(self):
            return f"BuildingCloseEffect({self.building_key})"

        def apply(self, **kwargs):
            if self.is_close:
                remove_building_collection_key(self.building_key, "open", self.name)
            else:
                add_building_collection_key(self.building_key, "open", self.name)
            return kwargs

        def revert(self, **kwargs):
            if self.options.has_option("EffectNoRevert"):
                return kwargs
            if self.is_close:
                add_building_collection_key(self.building_key, "open", self.name)
            else:
                remove_building_collection_key(self.building_key, "open", self.name)
            return kwargs

label open_bg_image_menu(event, **kwargs):
    $ bg_image = get_kwargs("bg_image", None, **kwargs)
    if bg_image != None:
        call show_idle_image(bg_image, **kwargs) from open_bg_image_menu_1

    
    $ event_list = [MenuElement(e.get_event(), get_translation(e.get_event()), EventEffect(e)) for e in event]
    call call_menu ('Select the Event.', character.subtitles, True, *event_list, **kwargs) from _call_call_menu
init -7 python:
    import re
    from abc import ABC, abstractmethod

    class Journal_Obj(ABC):
        """
        Abstract class for all journal objects.
        
        ### Attributes:
        1. _name: str
            - Name of the object.
        2. _title: str
            - Title of the object.
        3. _description: List[str]
            - Description of the object.
        4. _image_path_alt: str
            - Path to the image of the object.
        5. _image_path: str
            - Path to the image of the object.
        6. _unlock_conditions: ConditionStorage
            - Conditions for unlocking the object.
        7. _vote_comments: Dict[str, Dict[str, str]]
            - Comments for voting on the object.
        8. _default_comments: Dict[str, str]
            - Default comments for voting on the object.
        9. _unlock_effects: List[Effect]
            - Effects of unlocking the object.

        ### Methods:
        1. get_name(self) -> str
            - Returns the name of the object.
        2. get_title(self) -> str
            - Returns the title of the object.
        3. get_type(self) -> str
            - Returns the type of the object.
        4. get_description(self, level: int = -1) -> List[str]
            - Returns the description of the object.
        5. get_description_str(self, level: int = -1) -> str
            - Returns the description of the object as a string.
        6. get_image(self, school: str = "x", level: int = 0) -> str
            - Returns the path to the image of the object.
        7. get_full_image(self, school: str = "x", level: int = 0) -> str   
            - Returns the path to the full image of the object.
        8. unlock(self, school: str, unlock: bool = True, apply_effects: bool = False)
            - Unlocks the object.
        9. is_unlocked(self, school: str) -> bool
            - Returns whether the object is unlocked.
        10. is_visible(self, **kwargs) -> bool
            - Returns whether the object is visible.
        11. can_be_unlocked(self, **kwargs) -> bool
            - Returns whether the object can be unlocked.
        12. get_condition_storage(self) -> ConditionStorage
            - Returns the condition storage of the object.
        13. get_conditions(self) -> List[Condition]
            - Returns the conditions of the object.
        14. get_list_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]
            - Returns the list conditions of the object.
        15. get_list_conditions_list(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]
            - Returns the list conditions of the object as a list of tuples.
        16. get_desc_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]
            - Returns the description conditions of the object.
        17. get_desc_conditions_desc(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]
            - Returns the description conditions of the object as a list of strings.
        18. get_vote_comments(self, char: str, result: str) -> str
            - Returns the vote comments of the object.
        19. apply_effects(self)
            - Applies the effects of the object.
        """

        def __init__(self, name, title):
            self._name = name
            self._title = title
            self._description = [""]
            self._image_path_alt = "images/journal/empty_image.webp"
            self._image_path = "images/journal/empty_image.webp"
            self._unlock_conditions = ConditionStorage()
            self._vote_comments = {}
            self._default_comments = {
                "yes": "I vote yes.",
                "no": "I vote no.",
                "veto": "I veto this decision.",
            }
            self._unlock_effects = []

        def _update(self, title: str, data: Dict[str, Any] = None):
            self._title = title

            if hasattr(self, '_description'):
                self._description = [""]
            if hasattr(self, '_image_path_alt'):
                self._image_path_alt = "images/journal/empty_image.webp"
            if hasattr(self, '_image_path'):
                self._image_path = "images/journal/empty_image.webp"
            if hasattr(self, '_unlock_conditions'):
                self._unlock_conditions = ConditionStorage()
            if hasattr(self, '_vote_comments'):
                self._vote_comments = {}
            if hasattr(self, '_default_comments'):
                self._default_comments = {
                    "yes": "I vote yes.",
                    "no": "I vote no.",
                    "veto": "I veto this decision.",
                }
            if hasattr(self, '_unlock_effects'):
                self._unlock_effects = []

        def is_valid(self) -> bool:
            if self._name == "":
                log_error(401, f"|Journal_Obj:{self._name}| Name is missing!")
            if self._title == "":
                log_error(402, f"|Journal_Obj:{self._name}| Title is missing!")
            if not isinstance(self._description, list):
                log_error(403, f"|Journal_Obj:{self._name}| Description is not a list!")
            if self._unlock_conditions is None or not isinstance(self._unlock_conditions, ConditionStorage):
                log_error(404, f"|Journal_Obj:{self._name}| Unlock conditions are missing!")
            
            

        def get_name(self) -> str:
            """
            Returns the name of the object.
            The name is used to identify the object in the code.

            ### Returns:
            1. str
                - Name of the object.
            """

            return self._name

        def get_title(self) -> str:
            """
            Returns the title of the object.
            The title represents the visual name of the object for use in the UI.

            ### Returns:
            1. str
                - Title of the object.
            """

            return self._title

        @abstractmethod
        def get_type(self) -> str:
            pass

        def get_description(self, level: int = -1) -> List[str]:
            """
            Returns the descriptions of the object.

            ### Parameters:
            1. level: int (Default -1)
                - Level of the building.

            ### Returns:
            1. List[str]
                - Descriptions of the object.
            """

            return self._description

        def get_description_str(self, level: int = -1) -> str:
            """
            Returns the descriptions of the object as a string.

            ### Parameters:
            1. level: int (Default -1)
                - Level of the building.

            ### Returns:
            1. str
                - Descriptions of the object joined as a string separated with commas.
            """

            return "\n\n".join(self._description)

        def get_image(self, *, level: int = -1, variant = -1) -> str:
            """
            Returns the path to the image of the object.
            The image represents the visual representation of the object for use in the UI.
            The image path is interpolated with the school and level of the object it represents.

            ### Parameters:
            1. level: int (Default -1)
                - Level of the object.
                - If -1 the level will be determined by the school of the object.

            ### Returns:
            1. str
                - Path to the image of the object.
            """

            if level == -1:
                level = get_level_for_char(get_school())

            kwargs = {}

            if variant != -1:
                kwargs["variant"] = variant

            image_path = get_available_level(self._image_path, level)
            image_path, variant = refine_image_with_variant(image_path, **kwargs)
            
            if renpy.loadable(image_path):
                return image_path, variant
            return self._image_path_alt, -1
        
        def get_full_image(self, *, level: int = -1, variant = -1) -> str:
            """
            It gets the full size version of the image from get_image

            ### Parameters:
            2. level: int (Default -1)
                - Level of the object
                - If -1 the level will be determined by the school of the object

            ### Returns:
            1. str
                - Path to the full image of the object
            """

            if level == -1:
                level = get_level_for_char(get_school())

            kwargs = {}

            if variant != -1:
                kwargs["variant"] = variant

            image, variant = self.get_image(level = level, **kwargs)
            
            full_image = image.replace(".", "_full.")

            if renpy.loadable(full_image):
                return full_image, variant
            return None, 0
        
        def unlock(self, unlock: bool = True, apply_effects: bool = False):
            """
            Unlocks the object.

            ### Parameters:
            1. school: str
                - School of the object.
            2. unlock: bool (Default True)
                - Whether to unlock or lock the object.
            3. apply_effects: bool (Default False)
                - Whether to apply the effects of unlocking the object.
            """

            self._unlocked = unlock

            if self._unlocked and apply_effects:
                self.apply_effects()
        
        def is_unlocked(self) -> bool:
            """
            Returns whether the object is unlocked.

            ### Parameters:
            1. school: str
                - School of the object.

            ### Returns:
            1. bool
                - Whether the object is unlocked.
            """

            return self._unlocked

        def is_visible(self, **kwargs) -> bool:
            """
            Returns whether the object is visible.
            The object is visible if it is not blocked or if it is blocked but all conditions are fulfilled.

            ### Returns:
            1. bool
                - Whether the object is visible.
            """

            is_blocking = self._unlock_conditions.is_blocking(**kwargs)
            return is_blocking

        def can_be_unlocked(self, **kwargs) -> bool:
            """
            Returns whether the object can be unlocked.

            ### Returns:
            1. bool
                - Whether the object can be unlocked.
            """

            return self._unlock_conditions.is_fulfilled(**kwargs)

        def get_condition_storage(self) -> ConditionStorage:
            """
            Returns the condition storage of the object.

            ### Returns:
            1. ConditionStorage
                - Condition storage of the object.
            """

            return self._unlock_conditions

        def get_conditions(self) -> List[Condition]:
            """
            Returns the conditions of the object.

            ### Returns:
            1. List[Condition]
                - Conditions of the object.
            """

            return self._unlock_conditions.get_conditions()

        def get_list_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            """
            Returns the list conditions of the object.

            ### Parameters:
            1. cond_type: str (Default UNLOCK)
                - Type of the conditions.
                - not used here
            2. level: int (Default -1)
                - Level of the object.
                - not used here

            ### Returns:
            1. List[Condition]
                - List conditions of the object.
            """

            return self._unlock_conditions.get_list_conditions()

        def get_list_conditions_list(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]:
            """
            Returns the list conditions of the object as a list of tuples.

            ### Parameters:
            1. cond_type: str (Default UNLOCK)
                - Type of the conditions.
                - not used here
            2. level: int (Default -1)
                - Level of the object.
                - not used here

            ### Returns:
            1. List[Tuple[str, str]]
                - List conditions of the object as a list of tuples.
                - The tuples are in the format (condition icon, condition value).
            """

            return self._unlock_conditions.get_list_conditions_list(**kwargs)

        def get_desc_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            """
            Returns the description conditions of the object.

            ### Parameters:
            1. cond_type: str (Default UNLOCK)
                - Type of the conditions.
                - not used here
            2. level: int (Default -1)
                - Level of the object.
                - not used here

            ### Returns:
            1. List[Condition]
                - Description conditions of the object.
            """

            return self._unlock_conditions.get_desc_conditions()
        
        def get_desc_conditions_desc(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]:
            """
            Returns the description conditions of the object as a list of strings.

            ### Parameters:
            1. cond_type: str (Default UNLOCK)
                - Type of the conditions.
                - not used here
            2. level: int (Default -1)
                - Level of the object.
                - not used here

            ### Returns:
            1. List[str]
                - Description conditions of the object as a list of strings.
            """

            return self._unlock_conditions.get_desc_conditions_desc(**kwargs)
        
        def get_vote_comments(self, char: str, result: str) -> str:
            """
            Returns the vote comments of the object.
            Vote comments are comments the characters use when talking about the object depending on their stance towards it.

            ### Parameters:
            1. char: str
                - Name of the character.
            2. result: str
                - Result of the vote.
                - Can be "yes", "no" or "veto".

            ### Returns:
            1. str
                - Vote comments of the object.
            """
            
            vote = "{color=#00a000}Votes For{/color}"
            if result == NO:
                vote = "{color=#a00000}Votes Against{/color}"
            elif result == VETO:
                vote = "Vetoes"

            if char not in self._vote_comments.keys():
                return f"{vote}\n{self._default_comments[result]}"
            else:
                return f"{vote}\n{self._vote_comments[char][result]}"

        def apply_effects(self):
            """
            Applies the effects of the object.
            """

            for effect in self._unlock_effects:
                effect.apply()

    # def get_visible_unlocked_objs_by_school(map: Dict[str, Journal_Obj], school: str | Char) -> List[str]:
    #     """
    #     Returns the names of the visible unlocked objects of the map by school.

    #     ### Parameters:
    #     1. map: Dict[str, Journal_Obj]
    #         - Map of the objects.
    #     2. school: str | Char
    #         - School of the objects.

    #     ### Returns:
    #     1. List[str]
    #         - Names of the visible unlocked objects of the map by school.
    #     """

    #     output = []

    #     school_obj = school
    #     if isinstance(school, str):
    #         school_obj = get_character(school, charList['schools'])

    #     for obj in map.values():
    #         if (obj.is_visible(char_obj = school_obj) and
    #             obj.is_unlocked(school) and
    #             obj.get_name() not in output):
    #                 output.append(obj.get_name())

    #     return output

    # def get_visible_locked_objs_by_school(map: Dict[str, Journal_Obj], school: str | Char) -> List[str]:
    #     """
    #     Returns the names of the visible locked objects of the map by school.

    #     ### Parameters:
    #     1. map: Dict[str, Journal_Obj]
    #         - Map of the objects.
    #     2. school: str | Char
    #         - School of the objects.

    #     ### Returns:
    #     1. List[str]
    #         - Names of the visible locked objects of the map by school.
    #     """

    #     output = []

    #     school_obj = school
    #     if isinstance(school, str):
    #         school_obj = get_character(school, charList['schools'])

    #     for obj in map.values():
    #         if (obj.is_visible(char_obj = school_obj) and 
    #         not obj.is_unlocked(school) and
    #         obj.get_name() not in output):
    #             output.append(obj.get_name())

    #     return output

    
    def get_visible_unlocked_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        """
        Returns the names of the visible unlocked objects of all characters in map.

        ### Parameters:
        1. map: Dict[str, Journal_Obj]
            - Map of the objects.

        ### Returns:
        1. List[str]
            - Names of the visible unlocked objects of the map.
        """

        output = []

        school_obj = get_school()

        for obj in map.values():
            if (obj.is_visible(char_obj = school_obj) and 
            obj.is_unlocked() and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue

        return output

    def get_visible_locked_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        """
        Returns the names of the visible locked objects of all characters in map.

        ### Parameters:
        1. map: Dict[str, Journal_Obj]
            - Map of the objects.

        ### Returns:
        1. List[str]
            - Names of the visible locked objects of the map.
        """

        output = []

        school_obj = get_school()

        for obj in map.values():
            if (obj.is_visible(char_obj = school_obj) and 
            not obj.is_unlocked() and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue

        return output

    def get_visible_objs(map: Dict[str, Journal_Obj], include_unlocked: bool = False) -> List[str]:
        """
        Returns the names of the visible objects of all characters in map.

        ### Parameters:
        1. map: Dict[str, Journal_Obj]
            - Map of the objects.
        2. include_unlocked: bool (default False)
            - if False only not unlocked objects will be returned
            - if True all visible objects will be returned

        ### Returns:
        1. List[str]
            - Names of the visible objects of the map.
        """

        output = []

        school_obj = get_school()

        for obj in map.values():
            if (obj.is_visible(char_obj = school_obj) and 
            (not obj.is_unlocked() or include_unlocked) and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue
            
        return output

    def get_unlockable_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        """
        Returns the names of all the objects that can be unlocked.

        ### Parameters:
        1. map: Dict[str, Journal_Obj]
            - Map of the objects.

        ### Returns:
        1. List[str]
            - Names of the unlockable objects of the map.
        """

        output = []

        school_obj = get_school()

        for obj in map.values():
            if (obj.can_be_unlocked(char_obj = school_obj) and 
                not obj.is_unlocked() and 
                obj.get_name() not in output
            ):
                output.append(obj.get_name())
                continue

        return output

    # def get_unlockable_objs_by_school(school: str | Char) -> List[str]:
    #     """
    #     Returns the names of all the objects that can be unlocked for a specific school.

    #     ### Parameters:
    #     1. school: str | Char
    #         - The school for which the objects should be unlockable

    #     ### Returns:
    #     1. List[str]
    #         - Names of the unlockable objects for the school.
    #     """

    #     output = []

    #     school_obj = school
    #     if isinstance(school, str):
    #         school_obj = get_character(school, charList['schools'])

    #     for obj in map.values():
    #         unlock = obj.can_be_unlocked(char_obj = school_obj)
    #         unlocked = obj.is_unlocked(school)

    #         if (unlock and not unlocked and obj.get_name() not in output):
    #             output.append(obj.get_name())
    #             continue

    #     return output

    def get_journal_obj(map: Dict[str, Journal_Obj], name: str) -> Journal_Obj:
        """
        Returns the object with the given name from the map.

        ### Parameters:
        1. map: Dict[str, Journal_Obj]
            - Map of the objects.
        2. name: str
            - Name of the object.

        ### Returns:
        1. Journal_Obj
            - Object with the given name from the map.
            - if the object is not in the map it returns None
        """
        
        if name in map.keys():
            return map[name]
        return None


init -7 python:
    import re
    from abc import ABC, abstractmethod

    class Journal_Obj(ABC):
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

        def _update(self, title: str, data: Dict[str, Any] = None) -> None:
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

        def get_name(self) -> str:
            return self._name

        def get_title(self) -> str:
            return self._title

        @abstractmethod
        def get_type(self) -> str:
            pass

        def get_description(self, level: int = -1) -> List[str]:
            return self._description

        def get_description_str(self, level: int = -1) -> str:
            return "\n\n".join(self._description)

        def get_image(self, school: str = "x", level: int = 0) -> str:
            schools = [school]
            if school == "x":
                schools = ["high_school"]
                if loli_content >= 1:
                    schools.append("middle_school")
                if loli_content == 2:
                    schools.append("elementary_school")
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("<level>", str(i))
                for s in schools:
                    image = image.replace("<school>", s)
                    if renpy.loadable(image):
                        return image
            for i in range(0, 10):
                image = self._image_path.replace("<level>", str(i))
                for s in schools:
                    image = image.replace("<school>", s)
                    if renpy.loadable(image):
                        return image
            return self._image_path_alt
        
        def get_full_image(self, school: str = "x", level: int = 0) -> str:
            image = self.get_image(school, level)
            full_image = image.replace(".", "_full.")

            if renpy.loadable(full_image):
                return full_image
            return None
        
        def unlock(self, school: str, unlock: bool = True, apply_effects: bool = False) -> None:
            if school in self._unlocked:
                self._unlocked[school] = unlock

            if self._unlocked[school] and apply_effects:
                self.apply_effects()
        
        def is_unlocked(self, school: str) -> bool:
            return school in self._unlocked and self._unlocked[school]

        def is_visible(self, **kwargs) -> bool:
            return self._unlock_conditions.is_blocking(**kwargs)

        def can_be_unlocked(self, **kwargs) -> bool:
            return self._unlock_conditions.is_fulfilled(**kwargs)

        def get_condition_storage(self) -> ConditionStorage:
            return self._unlock_conditions

        def get_conditions(self) -> List[Condition]:
            return self._unlock_conditions.get_conditions()

        def get_list_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            return self._unlock_conditions.get_list_conditions()

        def get_list_conditions_list(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[Tuple[str, str]]:
            return self._unlock_conditions.get_list_conditions_list(**kwargs)

        def get_desc_conditions(self, cond_type: str = UNLOCK, level: int = -1) -> List[Condition]:
            return self._unlock_conditions.get_desc_conditions()
        
        def get_desc_conditions_desc(self, cond_type: str = UNLOCK, level: int = -1, **kwargs) -> List[str]:
            return self._unlock_conditions.get_desc_conditions_desc(**kwargs)
        
        def get_vote_comments(self, char: str, result: str) -> str:
            if char not in self._vote_comments.keys():
                return self._default_comments[result]

            vote = "{color=#00ff00}Votes For{/color}"
            if result == NO:
                vote = "{color=#ff0000}Votes Against{/color}"
            elif result == VETO:
                vote = "Vetoes"

            return f"{vote}\n{self._vote_comments[char][result]}"

        def apply_effects(self) -> None:
            for effect in self._unlock_effects:
                effect.apply()

    def get_visible_unlocked_objs_by_school(map: Dict[str, Journal_Obj], school: str | Char) -> List[str]:
        output = []

        school_obj = school
        if isinstance(school, str):
            school_obj = get_character(school, charList['schools'])

        for obj in map.values():
            if (obj.is_visible(char_obj = school_obj) and
                obj.is_unlocked(school) and
                obj.get_name() not in output):
                    output.append(obj.get_name())

        return output

    def get_visible_locked_objs_by_school(map: Dict[str, Journal_Obj], school: str | Char) -> List[str]:
        output = []

        school_obj = school
        if isinstance(school, str):
            school_obj = get_character(school, charList['schools'])

        for obj in map.values():
            if (obj.is_visible(char_obj = school_obj) and 
            not obj.is_unlocked(school) and
            obj.get_name() not in output):
                output.append(obj.get_name())

        return output

    
    def get_visible_unlocked_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        output = []

        high_school_obj = get_character('high_school', charList['schools'])
        middle_school_obj = get_character('middle_school', charList['schools'])
        elementary_school_obj = get_character('elementary_school', charList['schools'])

        for obj in map.values():
            if (obj.is_visible(char_obj = high_school_obj) and 
            obj.is_unlocked("high_school") and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue
            
            if loli_content >= 1:
                if (obj.is_visible(char_obj = middle_school_obj) and 
                obj.is_unlocked("middle_school") and
                obj.get_name() not in output):
                    output.append(obj.get_name())
                    continue

            if loli_content == 2:
                if (obj.is_visible(char_obj = elementary_school_obj) and 
                obj.is_unlocked("elementary_school") and
                obj.get_name() not in output):   
                    output.append(obj.get_name())
                    continue

        return output

    def get_visible_locked_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        output = []

        high_school_obj = get_character('high_school', charList['schools'])
        middle_school_obj = get_character('middle_school', charList['schools'])
        elementary_school_obj = get_character('elementary_school', charList['schools'])

        for obj in map.values():
            if (obj.is_visible(char_obj = high_school_obj) and 
            not obj.is_unlocked("high_school") and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue
            
            if loli_content >= 1:
                if (obj.is_visible(char_obj = middle_school_obj) and 
                not obj.is_unlocked("middle_school") and
                obj.get_name() not in output):
                    output.append(obj.get_name())
                    continue

            if loli_content == 2:
                if (obj.is_visible(char_obj = elementary_school_obj) and 
                not obj.is_unlocked("elementary_school") and
                obj.get_name() not in output):   
                    output.append(obj.get_name())
                    continue

        return output

    def get_visible_objs(map: Dict[str, Journal_Obj], include_unlocked: bool = False) -> List[str]:
        output = []

        high_school_obj = get_character('high_school', charList['schools'])
        middle_school_obj = get_character('middle_school', charList['schools'])
        elementary_school_obj = get_character('elementary_school', charList['schools'])

        for obj in map.values():
            if (obj.is_visible(char_obj = high_school_obj) and 
            (not obj.is_unlocked("high_school") or include_unlocked) and
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue
            
            if loli_content >= 1:
                if (obj.is_visible(char_obj = middle_school_obj) and 
                (not obj.is_unlocked("middle_school") or include_unlocked) and
                obj.get_name() not in output):
                    output.append(obj.get_name())
                    continue

            if loli_content == 2:
                if (obj.is_visible(char_obj = elementary_school_obj) and 
                (not obj.is_unlocked("elementary_school") or include_unlocked) and
                obj.get_name() not in output):   
                    output.append(obj.get_name())
                    continue

        return output

    def get_unlockable_objs(map: Dict[str, Journal_Obj]) -> List[str]:
        output = []

        high_school_obj = get_character('high_school', charList['schools'])
        middle_school_obj = get_character('middle_school', charList['schools'])
        elementary_school_obj = get_character('elementary_school', charList['schools'])

        for obj in map.values():
            high_unlock = obj.can_be_unlocked(char_obj = high_school_obj)
            high_unlocked = obj.is_unlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            obj.get_name() not in output):
                output.append(obj.get_name())
                continue

            if loli_content >= 1:
                middle_unlock = obj.can_be_unlocked(char_obj = middle_school_obj)
                middle_unlocked = obj.is_unlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                obj.get_name() not in output):
                    output.append(obj.gwt_name())
                    continue

            if loli_content == 2:
                elementary_unlock = obj.can_be_unlocked(char_obj = elementary_school_obj)
                elementary_unlocked = obj.is_unlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                obj.get_name() not in output):
                    output.append(obj.get_name())
                    continue

        return output

    def get_unlockable_objs_by_school(school: str | Char) -> List[str]:
        output = []

        school_obj = school
        if isinstance(school, str):
            school_obj = get_character(school, charList['schools'])

        for obj in map.values():
            unlock = obj.can_be_unlocked(char_obj = school_obj)
            unlocked = obj.is_unlocked(school)

            if (unlock and not unlocked and obj.get_name() not in output):
                output.append(obj.get_name())
                continue

        return output

    def get_journal_obj(map: Dict[str, Journal_Obj], name: str) -> Journal_Obj:
        if name in map.keys():
            return map[name]
        return None


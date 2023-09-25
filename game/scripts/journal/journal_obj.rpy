init -6 python:
    import re
    from abc import ABC, abstractmethod

    class Journal_Obj(ABC):
        def __init__(self, name, title):
            self._name = name
            self._title = title
            self._description = ""
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

        def _update(self, title, data = None):
            self._title = title

            if hasattr(self, '_description'):
                self._description = ""
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

        def get_name(self):
            return self._name

        def get_title(self):
            return self._title

        @abstractmethod
        def get_type(self):
            pass

        def get_description(self):
            return self._description

        def get_description_str(self):
            return "\n\n".join(self._description)

        def get_image(self, school = "x", level = 0):
            for i in reversed(range(0, level + 1)):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.loadable(image):
                    return image
            for i in range(0, 10):
                image = self._image_path.replace("<school>", school).replace("<level>", str(i))
                if renpy.loadable(image):
                    return image
            return self._image_path_alt
        
        def get_full_image(self, school = "x", level = 0):
            image = self.get_image(school, level)
            full_image = image.replace(".", "_full.")

            if renpy.loadable(full_image):
                return full_image
            return None
        
        def unlock(self, school, unlock = True, apply_effects = False):
            if school in self._unlocked:
                self._unlocked[school] = unlock

            if self._unlocked[school] and apply_effects:
                self.apply_effects()
        
        def is_unlocked(self, school):
            return school in self._unlocked and self._unlocked[school]

        def is_visible(self, school):
            return self._unlock_conditions.is_blocking(char_obj = get_character(school, charList["schools"]))

        def can_be_unlocked(self, school):
            return self._unlock_conditions.is_fullfilled(char_obj = get_character(school, charList["schools"]))

        def get_condition_storage(self):
            return self._unlock_conditions

        def get_conditions(self):
            return self._unlock_conditions.get_conditions()

        def get_list_conditions(self):
            return self._unlock_conditions.get_list_conditions()

        def get_desc_conditions(self):
            return self._unlock_conditions.get_desc_conditions()
        
        def get_desc_conditions_desc(self, **kwargs):
            return self._unlock_conditions.get_desc_conditions_desc(**kwargs)
        
        def get_vote_comments(self, char, result):
            if char not in self._vote_comments.keys():
                return self._default_comments[result]

            vote = "{color=#00ff00}Votes For{/color}"
            if result == "no":
                vote = "{color=#ff0000}Votes Against{/color}"
            elif result == "veto":
                vote = "Vetoes"

            return f"{vote}\n{self._vote_comments[char][result]}"

        def apply_effects(self):
            for effect in self._unlock_effects:
                effect.apply()

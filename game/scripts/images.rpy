init -4 python:
    from typing import List, Dict, Any, Tuple

    ########################
    # region Image Pattern #
    ########################

    def overwrite_event_image(event_key: str, pattern_key: str, pattern: Pattern):
        """
        Overwrites the image pattern of an event.

        ### Parameters:
        1. event_key: str
            - The key of the event to overwrite.
        2. pattern_key: str
            - The key of the pattern to overwrite.
        3. pattern: Pattern
            - The new pattern to use for the event.
        """

        if not is_mod_active(active_mod_key):
            return

        pattern._key = active_mod_key

        event = get_event_from_register(event_key)
        if event == None:
            log_error(501, f"Event '{event_key}' could not be found!")
            return
        event.set_pattern(pattern_key, pattern)

    def get_pattern_from_kwargs(pattern_key: str, **kwargs) -> Pattern:
        patterns = get_kwargs('frag_image_patterns', {}, **kwargs)
        if pattern_key in patterns.keys():
            return patterns[pattern_key]

        patterns = get_kwargs('image_patterns', {}, **kwargs)
        if pattern_key not in patterns.keys():
            log_error(502, f"Pattern '{pattern_key}' could not be found!")
            return None

        return patterns[pattern_key]

    def convert_pattern(pattern_key: str, **kwargs) -> Image_Series:
        """
        Converts a pattern to an image series.

        ### Parameters:
        1. pattern_key: str
            - The key of the pattern to convert.
        2. **kwargs
            - The keyword arguments to replace in the image path.
            - the patterns are also stored in the kwargs under the key 'image_patterns'
        """

        return Image_Series_Pattern(get_pattern_from_kwargs(pattern_key, **kwargs), **kwargs)

    def show_pattern(pattern_key: str, **kwargs):
        """
        Shows an image from a pattern.

        ### Parameters:
        1. pattern_key: str
            - The key of the pattern to show.
        2. **kwargs
            - The keyword arguments to replace in the image path.
            - the patterns are also stored in the kwargs under the key 'image_patterns'
        """

        pattern = get_pattern_from_kwargs(pattern_key, **kwargs)
        if pattern == None:
            return
        renpy.call('show_image', pattern.get_path(), **kwargs)

    class Pattern:
        """
        A class to represent an image pattern.
        This class can be used to store multiple image paths in an event object to enable them to be overwritten by mods.

        ### Attributes:
        1. _name: str
            - The key of the pattern.
        2. _pattern: str
            - The pattern of the image.
        3. _alternative_keys: List[str]
            - A list of all the alternative keys to replace in the image path.

        ### Methods:
        1. get_name() -> str
            - Returns the key of the pattern.
        2. get_pattern() -> str
            - Returns the pattern of the image.
        3. get_path() -> str
            - Returns the path of the pattern.
        4. get_alternative_keys() -> List[str]
            - Returns a list of all the alternative keys to replace in the image path.

        ### Parameters:
        1. name: str
            - The name of the pattern.
        2. pattern: str
            - The pattern of the image.
        3. alternative_keys: List[str] (default [])
            - A list of all the alternative keys to replace in the image path.
        """

        def __init__(self, name: str, pattern: str, *alternative_keys: str):
            self._name = name
            self._pattern = pattern
            self._alternative_keys = list(alternative_keys)

        def get_name(self) -> str:
            """
            Returns the name of the pattern.

            ### Returns:
            1. str
                - The name of the pattern.
            """

            return self._name

        def get_pattern(self) -> str:
            """
            Returns the pattern of the image.

            ### Returns:
            1. str
                - The pattern of the image.
            """

            return self._pattern

        def get_path(self) -> str:
            """
            Returns the path of the pattern.
            The path is the path based on the key combined with the pattern.

            ### Returns:
            1. str
                - The path of the pattern.
            """

            return get_mod_path(active_mod_key) + self._pattern

        def get_alternative_keys(self) -> List[str]:
            """
            Returns a list of all the alternative keys to replace in the image path.

            ### Returns:
            1. List[str]
                - A list of all the alternative keys to replace in the image path.
            """

            return self._alternative_keys

    # endregion
    ########################

init -2 python:
    from abc import ABC, abstractmethod
    from typing import List, Tuple
    import re
    import itertools

    image_code = -1
    last_image_code = -1
    last_image = ""
    last_image_nude = 0
    last_current_nude = 0

    ########################
    # region CLASSES ----- #
    ########################

    #######################
    # region Image Series #
    #######################

    class Image_Step:
        """
        A class to represent an image step.

        ### Attributes:
        1. image_path: str
            - The image path of the image.
        2. variant: int
            - The variant of the image.
        
        ### Methods:
        1. get_image(image_path: str, variant = -1) -> str
            - Returns the image path with the step and variant replaced.

        ### Parameters:
        1. image_path: str
            - The image path of the image.
        2. variant: int (default 1)
            - The variant of the image.
        """

        def __init__(self, image_path: str, variant: int = 1):
            """
            Constructs all the necessary attributes for the Image_Step object.

            ### Parameters:
            1. image_path: str
                - The image path of the image.
            2. variant: int (default 1)
                - The variant of the image.
            """

            self.image_path = image_path
            self.variant = variant

        def get_image(self, variant = -1) -> str:
            """
            Returns the image path with the step and variant replaced.

            ### Parameters:
            1. variant: int (default -1)
                - The variant to replace the variant in the image path with.
                - If the variant is -1, a random variant will be chosen.

            ### Returns:
            1. image_path: str
                - The image path with the step and variant replaced.
            """

            if variant < 1 or variant > self.variant:
                variant = renpy.random.randint(1, self.variant)
            image_path = self.image_path.replace("<variant>", str(variant))

            return image_path, variant

    class Image_Series():
        """
        A class to represent an image series.
        An image series is a series of images that are similar, but have different steps and variants.

        ### Attributes:
        1. steps: List[Image_Step]
            - A list of all the steps in the image series.
        
        ### Methods:
        1. create_steps(image_path: str)
            - Creates all the steps in the image series.
        2. show(step: int, display_type = SCENE, variant = -1) -> int
            - Shows the image with the given step and variant.
            - Returns the variant of the image.
        
        ### Parameters:
        1. image_path: str
            - The image path of the image series.
        2. **kwargs
            - The keyword arguments to replace in the image path.
            - alternative_keys: List[str]
                - A list of all the alternative keys to replace in the image path.
        """

        def __init__(self, image_path: str, alternative_keys: List[str] = [], **kwargs):
            """
            Constructs all the necessary attributes for the Image_Series object.

            ### Parameters:
            1. image_path: str
                - The image path of the image series.
            2. **kwargs
                - The keyword arguments to replace in the image path.
            """

            self._step_start = get_kwargs('step_start', 0, **kwargs)

            self._video_prefix = get_kwargs('video_prefix', 'anim_', **kwargs)

            self._image_paths = refine_image_with_alternatives(
                image_path, 
                alternative_keys,
                is_image_series = True,
                **kwargs
            )
            self.steps = []
            self.create_steps(self._image_paths)

        def update(self):
            if not hasattr(self, '_step_start'):
                self._step_start = 0

        def create_steps(self, image_paths: List[str]):
            """
            Creates all the steps in the image series.

            ### Parameters:
            1. image_paths: List[str]
                - A list of all the possible image paths.
            """

            if '<step>' in image_paths[0]:
                max_steps = get_image_max_value_with_alternatives('<step>', image_paths, self._step_start, 1000)

                for i in range(self._step_start, max_steps + 1):
                    for image_path in image_paths:
                        image_step = image_path.replace('<step>', str(i))
                        variant = 1

                        if '<variant>' in image_step:
                            variant = get_image_max_value_with_alternatives("<variant>", image_step, 1)
                            if variant == 0:
                                continue
                        elif not renpy.loadable(image_step.replace('<nude>', '0')):
                            continue
                        

                        self.steps.append(Image_Step(image_step, variant))
                        break
                    else:
                        log_error(203, f"'{image_paths[0]}' has no variants!")
                        self.steps.append(None)

            return

        def show(self, step: int, display_type = SCENE, variant = -1) -> int:
            """
            Shows the image with the given step and variant.

            ### Parameters:
            1. step: int
                - The step of the image to show.
            2. display_type: int (default SCENE)
                - The display type of the image.
            3. variant: int (default -1)
                - The variant of the image to show.
                - If the variant is -1, a random variant will be chosen.
            
            ### Returns:
            1. variant: int
                - The variant of the image.
            """

            self.update()

            if step < self._step_start or step >= len(self.steps) + self._step_start:
                log_error(201, f"Step {step} for {self._image_paths[0]} is out of range! (Min: {self._step_start}, Max: {len(self.steps) - 1 + self._step_start}))")
                renpy.show("black_screen_text", [], None, f"Step {step} is out of range! (Min: {self._step_start}, Max: {len(self.steps) - 1 + self._step_start}))")
                return -1

            image_step = self.steps[step - self._step_start]
            if image_step == None:
                log_error(202, f"Step {step} is missing variants for {self._image_paths[0]}!")
                renpy.show("black_screen_text", [], None, f"Step {step} is missing variants for {self._image_paths[0]}!")
                return -1

            (image_path, variant) = image_step.get_image(variant)

            if not sfw_mode:
                renpy.call("show_ready_image", image_path, display_type)   

            return variant  
        
        def show_video(self, step: int, pause = False, variant = -1) -> str:
            self.update()

            if step < self._step_start or step >= len(self.steps) + self._step_start:
                log_error(201, f"Step {step} for {self._image_paths[0]} is out of range! (Min: {self._step_start}, Max: {len(self.steps) - 1 + self._step_start}))")
                renpy.show("black_screen_text", [], None, f"Step {step} is out of range! (Min: {self._step_start}, Max: {len(self.steps) - 1 + self._step_start}))")
                return -1

            image_step = self.steps[step - self._step_start]
            if image_step == None:
                log_error(202, f"Step {step} is missing variants for {self._image_paths[0]}!")
                renpy.show("black_screen_text", [], None, f"Step {step} is missing variants for {self._image_paths[0]}!")
                return -1

            (image_path, variant) = image_step.get_image(variant)

            name = self._video_prefix + image_path.split('/')[-1].split('.')[0].replace(' ', '_')

            renpy.call("show_video_label", name, pause)

            return
    
    class Image_Series_Pattern(Image_Series):
        def __init__(self, pattern: Pattern, **kwargs):
            super().__init__(pattern.get_path(), pattern.get_alternative_keys(), **kwargs)

    # endregion
    #######################

    ############################
    # region Background Images #
    ############################

    class BGImage():
        """
        A class to represent a background image.

        ### Attributes:
        1. _conditions: List[Condition]
            - A list of all the conditions for the background image.
        2. _priority: int
            - The priority of the background image.
            - The higher Priority will be used over the lower Priority.
        3. _image_path: str
            - The image path of the background image.

        ### Methods:
        1. can_be_used(**kwargs) -> bool
            - Returns whether the background image can be used.
        2. get_priority() -> int
            - Returns the priority of the background image.
        3. get_image(**kwargs) -> str
            - Returns the image path of the background image.
        4. can_get_image(**kwargs) -> bool
            - Returns whether the image path of the background image can be found.

        ### Parameters:
        1. image_path: str
            - The image path of the background image.
        2. priority: int
            - The priority of the background image.
        3. *conditions: Condition
            - The conditions for the background image.
        """

        def __init__(self, image_path: str, priority: int, *conditions: Condition | Selector, alternative_keys: List[string] = []):
            """
            Constructs all the necessary attributes for the BGImage object.

            ### Parameters:
            1. image_path: str
                - The image path of the background image.
            2. priority: int
                - The priority of the background image.
            3. *conditions: Condition
                - The conditions for the background image.
            """

            self._conditions = [condition for condition in conditions if isinstance(condition, Condition)]
            self._selectors = SelectorSet(*[selector for selector in conditions if isinstance(selector, Selector)])
            self._priority = priority
            self._image_path = image_path
            self._path_prefix = ""
            
            self._combinations = [()]
            for i in range(1, len(alternative_keys) + 1):
                combinations.extend(itertools.combinations(alternative_keys, i))

        def can_be_used(self, **kwargs) -> bool:
            """
            Returns whether the background image can be used.

            ### Parameters:
            1. **kwargs
                - The keyword arguments to check the conditions with.

            ### Returns:
            1. bool
                - Whether the background image can be used.
            """

            if self._selectors != None:
                kwargs.update(self._selectors.get_values())
                self._selectors.roll_values()

            for condition in self._conditions:
                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def get_priority(self) -> int:
            """
            Returns the priority of the background image.

            ### Returns:
            1. int
                - The priority of the background image.
            """

            return self._priority

        def set_path_prefix(self, path_prefix: str):
            """
            Sets the path prefix of the background image.

            ### Parameters:
            1. path_prefix: str
                - The path prefix of the background image.
            """

            self._path_prefix = path_prefix

        def get_image(self, **kwargs) -> Tuple[int, str]:
            """
            Returns the image path of the background image.

            ### Parameters:
            1. **kwargs
                - The keyword arguments to replace in the image path.

            ### Returns:
            1. nude: int
                - The highest available nude-level.
            2. image_path: str
                - The image path of the background image.
            """
            
            if self._selectors != None:
                kwargs.update(self._selectors.get_values())
                self._selectors.roll_values()

            for combination in self._combinations:
                new_image_path = self._image_path

                for key in combination:
                    new_image_path = new_image_path.replace(f"<{key}>", "#")

                (nude, image_path) = get_image(self._path_prefix + new_image_path, **kwargs)

                if nude != -1:
                    return nude, image_path

            return -1, self._path_prefix + self._image_path

        def can_get_image(self, **kwargs) -> bool:
            """
            Returns whether the image path of the background image can be found in the game files.

            ### Parameters:
            1. **kwargs
                - The keyword arguments to replace in the image path.

            ### Returns:
            1. bool
                - Whether the image path of the background image can be found in the game files.
            """

            return self.get_image(self._path_prefix + self._image_path, **kwargs)[0] != -1
        
    class BGStorage:
        """
        A class to represent a background storage.
        A background storage is a storage for background images.

        ### Attributes:
        1. fallback_image: str
            - The fallback image path.
        2. images: List[BGImage]
            - A list of all the background images.
        3. _kwargs: dict
            - The keyword arguments to replace in the image path.

        ### Methods:
        1. get_images() -> List[BGImage]
            - Returns a list of all the background images.
        2. get_fallback() -> str
            - Returns the fallback image path.
        3. add_image(*image: BGImage)
            - Adds a background image to the background storage.
        4. add_kwargs(**kwargs)
            - Adds keyword arguments to the background storage.
        5. get_kwargs() -> dict
            - Returns the keyword arguments of the background storage.

        ### Parameters:
        1. fallback_image: str
            - The fallback image path.
        2. *images: BGImage
            - A list of all the background images.
        3. **kwargs
            - The keyword arguments to replace in the image path.
        """

        def __init__(self, fallback_image: str, *images: BGImage | Selector, **kwargs):
            self.fallback_image = fallback_image
            
            for i in images:
                if isinstance(i, BGImage):
                    i.set_path_prefix(get_mod_path(active_mod_key))

            self._selectors = SelectorSet(*[image for image in images if isinstance(image, Selector)])
            self.images = [image for image in images if isinstance(image, BGImage)]
            self._kwargs = kwargs

        def get_images(self) -> List[BGImage]:
            """
            Returns a list of all the background images.

            ### Returns:
            1. List[BGImage]
                - A list of all the background images.
            """

            return self.images

        def get_selector_values(self, **kwargs) -> Dict[str, Any]:
            """
            Returns the values of the selectors in the background storage.

            ### Returns:
            1. dict
                - The values of the selectors in the background storage.
            """

            if self._selectors == None:
                return {}

            values = self._selectors.get_values(**kwargs)
            self._selectors.roll_values(**kwargs)

            return values

        def get_fallback(self) -> str:
            """
            Returns the fallback image path.

            ### Returns:
            1. str
                - The fallback image path.
            """

            return self.fallback_image

        def set_fallback(self, fallback_image: str):
            """
            Sets the fallback image path.

            ### Parameters:
            1. fallback_image: str
                - The fallback image path.
            """

            self.fallback_image = fallback_image

        def add_image(self, *image: BGImage):
            """
            Adds a background image to the background storage.

            ### Parameters:
            1. *image: BGImage
                - A list of all the background images to add.
            """
            
            if not is_mod_active(active_mod_key):
                return

            for i in image:
                i.set_path_prefix(get_mod_path(active_mod_key))

            self.images.extend(image)

        def add_selector(self, *selector: Selector):
            self._selectors.add_selector(*selector)

        def add_kwargs(self, **kwargs):
            """
            Adds keyword arguments to the background storage.

            ### Parameters:
            1. **kwargs
                - The keyword arguments to add.
            """

            self._kwargs.update(kwargs)

        def get_kwargs(self) -> Dict[str, Any]:
            """
            Returns the keyword arguments of the background storage.

            ### Returns:
            1. dict
                - The keyword arguments of the background storage.
            """

            return self._kwargs

    # endregion
    ############################

    # endregion
    ########################

    ########################
    # region METHODS ----- #
    ########################

    #######################
    # region Image Getter #
    #######################

    def get_image(image_path: str, **kwargs) -> Tuple[int, str]:
        """
        Returns the image path with the given keyword arguments replaced.
        The <variant>-keyword will be replaced with a random variant when it is not specified in kwargs.
        The <level>-keyword will be replaced with the best available level when it is not specified in kwargs.
        The <nude>-keyword will be checked for the highest available nude-level and returned.

        ### Parameters:
        1. image_path: str
            - The image path to replace the keyword arguments in.
        2. **kwargs
            - The keyword arguments to replace in the image path.

        ### Returns:
        1. nude: int
            - The highest available nude-level.
        2. image_path: str
            - The image path with the given keyword arguments replaced.
        """

        kwargs["loli_content"] = loli_content

        # replace in string path each key from kwargs with corresponding value
        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        if 'level>' in image_path:
            image_path = insert_level(image_path, **kwargs)

        if "<variant>" in image_path:
            max_variant = get_image_max_value("<variant>", image_path, 1)
            if max_variant >= 1:
                image_path = image_path.replace("<variant>", str(get_random_int(1, max_variant)))

        if '<level>' in image_path:
            image_path = get_available_level(image_path, get_kwargs('level', 0, **kwargs))

        if "<nude>" not in image_path:
            if renpy.loadable(image_path):
                return 0, image_path
            else:
                log_error(204, f"'{image_path}' could not be found!")
                return -1, image_path

        for i in range(0, nude_vision):
            new_image_path = image_path.replace("<nude>", str(i))
            if not renpy.loadable(new_image_path):
                if i > 0:
                    return i - 1, image_path
                elif i == 0:
                    log_error(204, f" '{new_image_path}' could not be found!")
                    return -1, image_path

        return nude_vision, image_path
            
    def get_background(fallback: str, images: List[BGImage], **kwargs) -> Tuple[int, str]:
        """
        Returns the image path of the background with the highest priority that can be used.

        ### Parameters:
        1. fallback: str
            - The fallback image path.
        2. images: List[BGImage]
            - A list of all the background images.
        3. **kwargs
            - The keyword arguments to check the conditions with.

        ### Returns:
        1. nude: int
            - The highest available nude-level.
        2. image_path: str
            - The image path of the background with the highest priority that can be used.
        """

        kwargs["loli_content"] = loli_content

        output_image = None
        output_nude = 0
        priority = -1

        for bgimage in images:
            if not bgimage.can_be_used(**kwargs):
                continue

            max_nude, output = bgimage.get_image(**kwargs)
            if max_nude == -1:
                continue

            if priority < bgimage.get_priority() and max_nude >= 0:
                output_image = output
                output_nude = max_nude
                priority = bgimage.get_priority()
        

        if output_image == None:
            return 0, fallback
        else:
            return output_nude, output_image

    # endregion
    #######################

    ################
    # region Level #
    ################

    def get_available_level(path: str, level: int, register_value: bool = False) -> str:        
        """
        Searches for the best available level for a given image path.
        It first searches for the next lower level. If there is no level below found whose image is available it starts searching for the next higher level.

        ### Parameters:
        1. path: str
            - The image path whose level is to be determined
        2. level: int
            - The level to start searching from.

        ### Returns:
        1. str
            - The image path with the best available level.
        """

        old_image = path.replace("<level>", "~#~")
        old_image = old_image.replace("<variant>", "1") 
        old_image = re.sub("<.+>", "0", old_image)
        old_image = old_image.replace("~#~", "<level>")

        final_level = level

        if '<level>' in old_image:
            for i in reversed(range(0, level + 1)):
                test_image = old_image.replace("<level>", str(i))
                if renpy.loadable(test_image):
                    path =  path.replace("<level>", str(i))
                    final_level = i
                    break
            else:
                for i in range(0, 10):
                    test_image = old_image.replace("<level>", str(i))
                    if renpy.loadable(test_image):
                        path = path.replace("<level>", str(i))
                        final_level = i

        if register_value:
            register_value('level', final_level)

        return path

    def insert_level(path: str, **kwargs) -> str:
        """
        Replaces the <level>-keyword in the given image path with the best available level.

        ### Parameters:
        1. path: str
            - The image path to replace the <level>-keyword in.
        2. **kwargs
            - The keyword arguments to replace in the image path.
            - possible keywords: level, school_obj, teacher_obj, parent_obj, secretary_obj

        ### Returns:
        1. str
            - The image path with the levels inserted
        """

        if '<school_level>' in path:
            path = path.replace("<school_level>", str(get_character_by_key('school').get_level()))
        if 'teacher_level' in path:
            path = path.replace("<teacher_level>", str(get_character_by_key('teacher').get_level()))
        if 'parent_level' in path:
            path = path.replace("<parent_level>", str(get_character_by_key('parent').get_level()))
        if 'secretary_level' in path:
            path = path.replace("<secretary_level>", str(get_character_by_key('secretary').get_level()))

        return path

    # endregion
    ################

    #######################
    # region value tester #
    #######################

    def get_image_max_value(key: str, image_path: str, start: int = 0, end: int = 10) -> int:
        """
        Searches for the highest available value for a key in the given image path.

        ### Parameters:
        1. key: str
            - The key to search for.
        2. image_path: str
            - The image path to search in.
        3. start: int (default 0)
            - The start value to search from.
        4. end: int (default 10)
            - The end value to search to.

        ### Returns:
        1. int
            - The highest available value for the key in the given image path.
        """

        old_image = image_path.replace(key, "~#~")
        old_image = re.sub("<.+>", "0", old_image)
        old_image = old_image.replace("~#~", key)

        for i in range(start, end):
            test_image = old_image.replace(key, str(i))
            if not renpy.loadable(test_image):
                return i - 1

        return end

    def get_image_max_value_with_alternatives(key: str, image_paths: List[str], start: int = 0, end: int = 10) -> int:
        """
        Searches for the highest available value for a key in the given image path.

        ### Parameters:
        1. key: str
            - The key to search for.
        2. image_paths: List[str]
            - A list of all the possible image paths.
        3. start: int (default 0)
            - The start value to search from.
        4. end: int (default 10)
            - The end value to search to.

        ### Returns:
        1. int
            - The highest available value for the key in the given image path.
        """

        for i in range(start, end):
            for image_path in image_paths:

                old_image = image_path.replace(key, "~#~")
                old_image = re.sub("<.+>", "0", old_image)
                test_image = old_image.replace("~#~", str(i))

                if renpy.loadable(test_image):
                    break
            else:
                return i - 1

        return end

    # endregion
    #######################

    #######################
    # region Refine Image #
    #######################

    def refine_image_with_alternatives(image_path: str, alternative_keys: List[str], **kwargs) -> List[str]:
        """
        Returns all possible image paths with possible alternatives in case an image is missing concrete values.
        Images can use # instead.

        ### Parameters:
        1. image_path: str
            - The image path to replace the keyword arguments in.
        2. alternative_keys: List[str]
            - A list of all the alternative keys to replace in the image path.
        3. **kwargs
            - The keyword arguments to replace in the image path.

        ### Returns:
        1. List[str]
            - A list of all possible image paths with possible alternatives in case an image is missing concrete values.
        """

        combinations = [()]
        for r in range(1, len(alternative_keys) + 1):
            combinations.extend(itertools.combinations(alternative_keys, r))

        is_image_series = get_kwargs('is_image_series', False, **kwargs)
        is_replay = get_kwargs('is_replay', False, **kwargs)

        output = []

        if 'values' in kwargs.keys():
            kwargs = kwargs['values']

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        for combination in combinations:
            new_image_path = image_path

            for key in combination:
                new_image_path = new_image_path.replace(f"<{key}>", "#")

            if '<school_level>' in new_image_path:
                if is_image_series and not is_replay:
                    register_value('school_level', get_character_by_key('school').get_level())
                new_image_path = new_image_path.replace("<school_level>", str(get_character_by_key('school').get_level()))

            if 'teacher_level' in new_image_path:
                if is_image_series and not is_replay:
                    register_value('teacher_level', get_character_by_key('teacher').get_level())
                new_image_path = new_image_path.replace("<teacher_level>", str(get_character_by_key('teacher').get_level()))
            
            if 'parent_level' in new_image_path:
                if is_image_series and not is_replay:
                    register_value('parent_level', get_character_by_key('parent').get_level())
                new_image_path = new_image_path.replace("<parent_level>", str(get_character_by_key('parent').get_level()))
            
            if 'secretary_level' in new_image_path:
                if is_image_series and not is_replay:
                    register_value('secretary_level', get_character_by_key('secretary').get_level())
                new_image_path = new_image_path.replace("<secretary_level>", str(get_character_by_key('secretary').get_level()))
            
            if '<level>' in image_path:
                new_image_path = get_available_level(new_image_path, get_kwargs('level', 0, **kwargs)) 
            
            for key, value in kwargs.items():
                new_image_path = new_image_path.replace(f"<{key}>", str(value))
                if is_image_series and not is_replay:
                    register_value(key, value)
            
            output.append(new_image_path)

        output.sort(key=lambda x: x.count("#"))

        return output

    def refine_image(image_path: str, **kwargs) -> str:
        """
        Returns the image path with the given keyword arguments replaced.

        ### Parameters:
        1. image_path: str
            - The image path to replace the keyword arguments in.
        2. **kwargs
            - The keyword arguments to replace in the image path.

        ### Returns:
        1. str
            - The image path with the given keyword arguments replaced.
        """

        is_image_series = get_kwargs('is_image_series', False, **kwargs)
        is_replay = get_kwargs('is_replay', False, **kwargs)

        if 'values' in kwargs.keys():
            kwargs = kwargs['values']

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        if '<school_level>' in image_path:
            if is_image_series and not is_replay:
                register_value('school_level', get_character_by_key('school').get_level())
            image_path = image_path.replace("<school_level>", str(get_character_by_key('school').get_level()))
        
        if 'teacher_level' in image_path:
            if is_image_series and not is_replay:
                register_value('teacher_level', get_character_by_key('teacher').get_level())
            image_path = image_path.replace("<teacher_level>", str(get_character_by_key('teacher').get_level()))
        
        if 'parent_level' in image_path:
            if is_image_series and not is_replay:
                register_value('parent_level', get_character_by_key('parent').get_level())
            image_path = image_path.replace("<parent_level>", str(get_character_by_key('parent').get_level()))
        
        if 'secretary_level' in image_path:
            if is_image_series and not is_replay:
                register_value('secretary_level', get_character_by_key('secretary').get_level())
            image_path = image_path.replace("<secretary_level>", str(get_character_by_key('secretary').get_level()))
        
        if '<level>' in image_path:
            image_path = get_available_level(image_path, get_kwargs('level', 0, **kwargs)) 

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))
            if is_image_series and not is_replay:
                register_value(key, value)

        return image_path

    def refine_image_with_variant(image_path: str, **kwargs) -> str:
        """
        Returns the image path with the given keyword arguments replaced and sets the variant-keyword if not already given in kwargs

        ### Parameters:
        1. image_path: str
            - The image path to replace the keyword arguments in.
        2. **kwargs
            - The keyword arguments to replace in the image path

        ### Returns:
        1. str
            - The image path with the given keyword arguments replaced.
        """

        is_image_series = get_kwargs('is_image_series', False, **kwargs)
        is_replay = get_kwargs('is_replay', False, **kwargs)

        if 'values' in kwargs.keys():
            kwargs = kwargs['values']

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        if '<school_level>' in image_path:
            if is_image_series and not is_replay:
                register_value('school_level', get_character_by_key('school').get_level())
            image_path = image_path.replace("<school_level>", str(get_character_by_key('school').get_level()))
        
        if 'teacher_level' in image_path:
            if is_image_series and not is_replay:
                register_value('teacher_level', get_character_by_key('teacher').get_level())
            image_path = image_path.replace("<teacher_level>", str(get_character_by_key('teacher').get_level()))
        
        if 'parent_level' in image_path:
            if is_image_series and not is_replay:
                register_value('parent_level', get_character_by_key('parent').get_level())
            image_path = image_path.replace("<parent_level>", str(get_character_by_key('parent').get_level()))
        
        if 'secretary_level' in image_path:
            if is_image_series and not is_replay:
                register_value('secretary_level', get_character_by_key('secretary').get_level())
            image_path = image_path.replace("<secretary_level>", str(get_character_by_key('secretary').get_level()))
        
        if '<level>' in image_path:
            image_path = get_available_level(image_path, get_kwargs('level', 0, **kwargs)) 

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))
            if is_image_series and not is_replay:
                register_value(key, value)

        variant = get_kwargs('variant', 0, **kwargs)

        # if 'level>' in image_path:
        #     image_path = insert_level(image_path, **kwargs)

        if "<variant>" in image_path:
            max_variant = get_image_max_value("<variant>", image_path, 1)
            if max_variant >= 1:
                image_path = image_path.replace("<variant>", str(get_random_int(1, max_variant)))

        return image_path, variant
    
    # endregion
    #######################

    ###################################
    # region Check Image availability #
    ###################################

    def check_image(image_path: str) -> bool:
        """
        Checks if the image at the image path is available and ready to load

        ### Parameters:
        1. image_path: str
            - The image path to look for

        ### Returns:
        1. bool
            - If the image is available at that path
        """
        return renpy.loadable(image_path)

    # endregion
    ###################################

    # endregion
    ########################

#####################################
# region IMAGE DISPLAY LABEL #
#####################################

label show_video_label(name, pause):
    $ hide_all()
    scene expression name with dissolveM

    if pause:
        $ renpy.pause()

    return

label Image_Series:
    $ i = 0
label .show_image(image_series, *steps, pause = False, display_type = SCENE, variant = -1):
    # """
    # Shows the images of the image series with the given steps.
    # other than the show method, this method will show the images in a sequence and will pause after the last image if pause is set to True.

    # ### Parameters:
    # 1. image_series: Image_Series
    #     - The image series to show the images of.
    # 2. *steps: int
    #     - The steps of the images to show.
    # 3. pause: bool (default False)
    #     - Whether to pause after the last image.
    # 4. display_type: int (default SCENE)
    #     - The display type of the image.
    # 5. variant: int (default -1)
    #     - The variant of the image to show.
    #     - If the variant is -1, a random variant will be chosen.

    # ### Returns:
    # 1. variant: int
    #     - The variant of the last image.
    # """
    $ i = 0
    while i < len(steps):
        $ step = steps[i]
        $ variant = image_series.show(step, display_type, variant)
        if (pause and i == len(steps) - 1) or i < len(steps) - 1:
            $ renpy.pause()
        $ i += 1
    return variant

label show_image(path, display_type = SCENE, **kwargs):
    # """
    # Shows an image with the given path and keyword arguments.

    # ### Parameters:
    # 1. path: str
    #     - The image path to show.
    # 2. display_type: int (default SCENE)
    #     - The display type of the image.
    # 3. **kwargs
    #     - The keyword arguments to replace in the image path.
    # """

    $ image_path = refine_image(path, **kwargs)

    call show_ready_image(image_path, display_type) from _call_show_ready_image
    return

screen black_error_screen_text(text_str):
    python:
        """
        Displays a black screen with red text
        Would be used for error messages

        # Parameters:
        1. text_str: str
            - the text to be displayed
        """

    add "black"
    zorder -1
    
    text text_str:
        xalign 0 yalign 0
        size 20
        color "#a00000"

screen black_screen_text(text_str):
    python:
        """
        Displays a black screen with white text

        # Parameters:
        1. text_str: str
            - the text to be displayed
        """

    add "black"
    
    key "K_SPACE" action Return()
    key "K_ESCAPE" action Return()
    key "K_KP_ENTER" action Return()
    key "K_SELECT" action Return()

    text text_str:
        xalign 0.5 yalign 0.5
        size 60

    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        action Return()

screen black_screen_text_with_subtitle(text_str, subtitle_str):
    python:
        """
        Displays a black screen with white text

        # Parameters:
        1. text_str: str
            - the text to be displayed
        """

    add "black"
    
    key "K_SPACE" action Return()
    key "K_ESCAPE" action Return()
    key "K_KP_ENTER" action Return()
    key "K_SELECT" action Return()

    vbox:
        yalign 0.5
        xsize 1920

        text text_str:
            xalign 0.5
            size 60
        null height 10
        text subtitle_str:
            xalign 0.5
            size 40
    
    button:
        xpos 0 ypos 0
        xsize 1920 ysize 1080
        action Return()

label say_with_image (image_series, step, text, person_name, person):
    # """
    # Prints a text with an image
    # Mainly used for the "random_say" method

    # ### Parameters:
    # 1. image_series: Image_Series
    #     - The image series to use
    # 2. step: int
    #     - The step of the image series to use
    # 3. text: str
    #     - The text to print
    # 4. person_name: str
    #     - The name of the person to print
    # 5. person: ADVCharacter
    #     - The character who says the text
    # """

    $ image_series.show(step)
    $ person(text, name = person_name)

    return

# endregion
#####################################

#############################
# region show image methods #
#############################

label show_sfw_text(text):
    # """
    # Shows a text on black screen in sfw_mode is active

    # ### Parameters:
    # 1. text: str
    #     - The text to show
    # """

    if sfw_mode:
        call screen black_screen_text (text) with dissolveM
    return

label show_idle_image(bg_images, **kwargs):
    # """
    # Shows an idle image with the given background images and keyword arguments.

    # ### Parameters:
    # 1. bg_images: BGStorage
    #     - The background images to show.
    # 2. **kwargs
    #     - The keyword arguments to replace in the image path.
    # """
    
    if bg_images == None:
        return
    $ fallback_image = bg_images.get_fallback()
    $ images = bg_images.get_images()
    $ kwargs.update(bg_images.get_kwargs())

    $ selector_values = bg_images.get_selector_values(**kwargs)
    $ kwargs.update(selector_values)

    if last_image_code != image_code:
        $ last_image_code = image_code

        $ max_nude, image_path = get_background(fallback_image, images, **kwargs)
        $ current_nude = DEFAULT_NUDE

        $ last_image = image_path
        $ last_image_nude = max_nude
        $ last_current_nude = current_nude
    else:
        $ max_nude = last_image_nude
        $ image_path = last_image
        $ current_nude = last_current_nude

    call show_image_with_nude_var (image_path, max_nude, current_nude) from show_idle_image_1

    return

label show_image_with_variant(path, display_type = SCENE, **kwargs):
    # """
    # Shows an image with the given path and keyword arguments where the variant keyword gets selected randomly if not already given in kwargs.

    # ### Parameters:
    # 1. path: str
    #     - The image path to show.
    # 2. display_type: int (default SCENE)
    #     - The display type of the image.
    # 3. **kwargs
    #     - The keyword arguments to replace in the image path.
    # """

    $ image_path, variant = refine_image_with_variant(path, **kwargs)

    call show_ready_image(image_path, display_type) from _call_show_ready_image_1
    return
    
label show_ready_image(path, display_type = SCENE):
    # """
    # Shows an image with the given path and display type.
    # This method automatically looks for the best way to show the image.

    # ### Parameters:
    # 1. path: str
    #     - The image path to show.
    # 2. display_type: int (default SCENE)
    #     - The display type of the image.
    # """

    if "<nude>" in path:
        call show_ext_image_with_nude_var(path) from _call_show_ext_image_with_nude_var
    else:
        if check_image(path):
            if display_type == SHOW:
                show expression path with dissolveM
            elif display_type == SCENE:
                scene expression path with dissolveM
        else:
            $ log_error(204, f"'{new_image_path}' could not be found!")
    return

label show_ext_image_with_nude_var(image_path, **kwargs):
    # """
    # Shows an image with the given path and keyword arguments.
    # This method shows the image in a special way where a button is shown to switch between the different nude versions of the image.

    # ### Parameters:
    # 1. image_path: str
    #     - The image path to show.
    # 2. **kwargs
    #     - The keyword arguments to replace in the image path.
    # """

    $ nude, ext_image = get_image(image_path, **kwargs)
    call show_image_with_nude_var(ext_image, nude) from show_ext_image_with_nude_var_1
    return

label show_image_with_nude_var(image_path, limit = 0, nude = DEFAULT_NUDE):
    # """
    # Is used to display an image with nude variants.
    # DO NOT USE THIS METHOD DIRECTLY! Use show_ext_image_with_nude_var instead!

    # ### Parameters:
    # 1. image_path: str
    #     - The image path to show.
    # 2. limit: int (default 0)
    #     - The highest nude level to show.
    # """

    if limit > nude_vision:
        $ limit = nude_vision

    $ paths = []
    $ image_not_found = False

    python:
        for i in range(0, limit + 1):
            new_image_path = image_path.replace("<nude>", str(i))
            paths.append(new_image_path)
            if len(paths) == 1 and not renpy.loadable(new_image_path):
                log_error(205, f"'{image_path}' is missing nude version images!")
                image_not_found = True
    
    if image_not_found:
        return

    call call_screen_image_with_nude_var (paths, limit, nude) from show_image_with_nude_var_1

    return

label call_screen_image_with_nude_var(paths, limit = 2, nude = DEFAULT_NUDE):
    # """
    # Calls the screen image_with_nude_var with the given paths, limit and nude level.

    # ### Parameters:
    # 1. paths: List[str]
    #     - A list of all the image paths.
    # 2. limit: int (default 2)
    #     - The highest nude level to show.
    # 3. nude: int (default 2)
    #     - The current nude level.
    # """

    $ last_current_nude = nude

    show screen image_with_nude_var(paths, limit, nude) with dissolveM
    return

screen image_with_nude_var(paths, limit = 2, nude = DEFAULT_NUDE):
    # """
    # Shows the image with a button to switch between the different nude versions.

    # ### Parameters:
    # 1. paths: List[str]
    #     - A list of all the image paths.
    # 2. limit: int (default 2)
    #     - The highest nude level to show.
    # 3. nude: int (default 0)
    #     - The current nude level.
    # """
    tag background
    
    if len(paths) <= nude:
        $ nude = len(paths) - 1

    if limit < nude:
        $ nude = limit

    $ path = paths[nude]

    if renpy.loadable(path):
        image "[path]"

    if nude_vision != 0 and nude == limit and nude != 0:
        imagebutton:
            auto "icons/sight_disabled_%s.webp"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 0)

    if nude == 0 and limit > 0:
        imagebutton:
            auto "icons/eye_target_%s.webp"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 1)

    if nude == 1 and limit > 1:
        imagebutton:
            auto "icons/fire_iris_%s.webp"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 2)

# endregion
#############################

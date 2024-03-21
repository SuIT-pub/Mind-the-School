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

            log_val('image_path', image_path)

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

    class Image_Obj(ABC):
        """
        A class to represent an image object.
        """

        def __init__(self, image_path: str):
            """
            Constructs all the necessary attributes for the Image_Obj object.

            ### Parameters:
            1. image_paths: List[str]
                - A list of all the image paths.
            """
            self._image_path = image_path

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

            self._image_paths = refine_image_with_alternatives(
                image_path, 
                alternative_keys,
                **kwargs
            )
            self.steps = []
            log_val('series: image_paths', self._image_paths)
            self.create_steps(self._image_paths)

        def create_steps(self, image_paths: List[str]):
            """
            Creates all the steps in the image series.

            ### Parameters:
            1. image_paths: List[str]
                - A list of all the possible image paths.
            """

            if '<step>' in image_paths[0]:
                max_steps = get_image_max_value_with_alternatives('<step>', image_paths, 0, 100)

                log_val('max_steps', max_steps)

                for i in range(0, max_steps + 1):
                    log_val('step', i)
                    for image_path in image_paths:
                        image_step = image_path.replace('<step>', str(i))
                        log_val('image_step', image_step)
                        variant = 1

                        if '<variant>' in image_step:
                            variant = get_image_max_value_with_alternatives("<variant>", image_step, 1)
                            log_val('variant', variant)
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

            if step < 0 or step >= len(self.steps):
                log_error(201, f"Step {step} for {self._image_paths[0]} is out of range! (Min: 0, Max: {len(self.steps) - 1}))")
                renpy.show("black_screen_text", [], None, f"Step {step} is out of range! (Min: 0, Max: {len(self.steps) - 1}))")
                return

            image_step = self.steps[step]
            if image_step == None:
                log_error(202, f"Step {step} is missing variants for {self._image_paths[0]}!")
                renpy.show("black_screen_text", [], None, f"Step {step} is missing variants for {self._image_paths[0]}!")
                return

            (image_path, variant) = image_step.get_image(variant)

            if not sfw_mode:
                renpy.call("show_ready_image", image_path, display_type)   
            return variant  
                
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

        def __init__(self, fallback_image: str, *images: BGImage, **kwargs):
            self.fallback_image = fallback_image
            self.images = list(images)
            self._kwargs = kwargs

        def get_images(self) -> List[BGImage]:
            """
            Returns a list of all the background images.

            ### Returns:
            1. List[BGImage]
                - A list of all the background images.
            """

            return self.images

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

            self.images.extend(image)

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

    class BGImage(Image_Obj):
        """
        A class to represent a background image.

        ### Attributes:
        1. _conditions: List[Condition]
            - A list of all the conditions for the background image.
        2. _priority: int
            - The priority of the background image.
            - The higher Priority will be used over the lower Priority.

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

        def __init__(self, image_path: str, priority: int, *conditions: Condition):
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

            super().__init__(image_path)
            self._conditions = list(conditions)
            self._priority = priority

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

        def get_image(self, **kwargs) -> str:
            """
            Returns the image path of the background image.

            ### Parameters:
            1. **kwargs
                - The keyword arguments to replace in the image path.

            ### Returns:
            1. str
                - The image path of the background image.
            """

            return get_image(self._image_path, **kwargs)

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

            return get_image(self._image_path, **kwargs)[0] != -1

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

            if priority < bgimage.get_priority() and max_nude >= 0:
                output_image = output
                output_nude = max_nude
                priority = bgimage.get_priority()
        

        if output_image == None:
            return 0, fallback
        else:
            return output_nude, output_image

    def get_available_level(path: str, level: int) -> str:        
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

        if '<level>' in old_image:
            for i in reversed(range(0, level + 1)):
                test_image = old_image.replace("<level>", str(i))
                if renpy.loadable(test_image):
                    path =  path.replace("<level>", str(i))
                    break
            else:
                for i in range(0, 10):
                    test_image = old_image.replace("<level>", str(i))
                    if renpy.loadable(test_image):
                        path = path.replace("<level>", str(i))

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

        output = []

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        for combination in combinations:
            new_image_path = image_path
            for key in combination:
                new_image_path = new_image_path.replace(f"<{key}>", "#")
            for key, value in kwargs.items():
                new_image_path = new_image_path.replace(f"<{key}>", str(value))
                if 'level>' in image_path:
                    new_image_path = insert_level(new_image_path, **kwargs)
                if '<level>' in image_path:
                    new_image_path = get_available_level(new_image_path, get_kwargs('level', 0, **kwargs))
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

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        if 'level>' in image_path:
            image_path = insert_level(image_path, **kwargs)
        if '<level>' in image_path:
            image_path = get_available_level(image_path, get_kwargs('level', 0, **kwargs))

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

        if 'loli_content' not in kwargs.keys():
            kwargs['loli_content'] = loli_content
        if 'loli' not in kwargs.keys():
            kwargs['loli'] = get_random_loli()

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        variant = get_kwargs('variant', 0, **kwargs)

        if 'level>' in image_path:
            image_path = insert_level(image_path, **kwargs)

        if "<variant>" in image_path:
            max_variant = get_image_max_value("<variant>", image_path, 1)
            if max_variant >= 1:
                image_path = image_path.replace("<variant>", str(get_random_int(1, max_variant)))

        if '<level>' in image_path:
            image_path = get_available_level(image_path, get_kwargs('level', 0, **kwargs))

        return image_path, variant
    
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

    $ fallback_image = bg_images.get_fallback()
    $ images = bg_images.get_images()

    $ kwargs.update(bg_images.get_kwargs())

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

label call_screen_image_with_nude_var (paths, limit = 2, nude = DEFAULT_NUDE):
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
            action Call("call_screen_image_with_nude_var", paths, limit, 0)

    if nude == 0 and limit > 0:
        imagebutton:
            auto "icons/eye_target_%s.webp"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Call("call_screen_image_with_nude_var", paths, limit, 1)

    if nude == 1 and limit > 1:
        imagebutton:
            auto "icons/fire_iris_%s.webp"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Call("call_screen_image_with_nude_var", paths, limit, 2)



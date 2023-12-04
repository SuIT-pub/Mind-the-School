init -2 python:
    from abc import ABC, abstractmethod
    from typing import List, Tuple
    import re

    class Image_Step:
        """
        A class to represent an image step.

        ### Attributes:
        1. step: int
            - The step of the image.
        2. variant: int
            - The variant of the image.
        
        ### Methods:
        1. get_image(image_path: str, variant = -1) -> str
            - Returns the image path with the step and variant replaced.

        ### Parameters:
        1. step: int
            - The step of the image.
        2. variant: int (default 1)
            - The variant of the image.
        """

        def __init__(self, step: int, variant = 1):
            """
            Constructs all the necessary attributes for the Image_Step object.

            ### Parameters:
            1. step: int
                - The step of the image.
            2. variant: int (default 1)
                - The variant of the image.
            """

            self.step = step
            self.variant = variant

        def get_image(self, image_path: str, variant = -1) -> str:
            """
            Returns the image path with the step and variant replaced.

            ### Parameters:
            1. image_path: str 
                - The image path to replace the step and variant in.
            2. variant: int (default -1)
                - The variant to replace the variant in the image path with.
                - If the variant is -1, a random variant will be chosen.

            ### Returns:
            1. image_path: str
                - The image path with the step and variant replaced.
            """

            image_path = image_path.replace("<step>", str(self.step))

            if variant < 1 or variant > self.variant:
                variant = renpy.random.randint(1, self.variant)
            image_path = image_path.replace("<variant>", str(variant))

            return image_path, variant

    class Image_Obj(ABC):
        """
        A class to represent an image object.
        """

        def __init__(self, image_path: str):
            """
            Constructs all the necessary attributes for the Image_Obj object.

            ### Parameters:
            1. image_path: str
                - The image path of the image object.
            """
            self._image_path = image_path

    class Image_Series(Image_Obj):
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
        """

        def __init__(self, image_path: str, **kwargs):
            """
            Constructs all the necessary attributes for the Image_Series object.

            ### Parameters:
            1. image_path: str
                - The image path of the image series.
            2. **kwargs
                - The keyword arguments to replace in the image path.
            """

            image_path = refine_image(image_path, **kwargs)
            super().__init__(image_path)
            self.steps = []
            self.create_steps(image_path)

        def create_steps(self, image_path: str):
            """
            Creates all the steps in the image series.

            ### Parameters:
            1. image_path: str
                - The image path of the image series.
            """

            if '<step>' in image_path:
                max_steps = get_image_max_value('<step>', image_path, 0, 100)

                for i in range(0, max_steps + 1):
                    image = image_path.replace('<step>', str(i))

                    variant = 1

                    if '<variant>' in image_path:
                        variant = get_image_max_value("<variant>", image_path, 1)
                        if variant == 0:
                            log_error(f"'{image_path}' has no variants!")
                            self.steps.append(None)
                            continue

                    self.steps.append(Image_Step(i, variant))
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
                log_val("image", self._image_path)
                log_error(f"Step {step} is out of range! (Min: 0, Max: {len(self.steps) - 1}))")
                renpy.show("black_screen_text", f"Step {step} is out of range! (Min: 0, Max: {len(self.steps) - 1}))")
                return

            image_step = self.steps[step]
            if image_step == None:
                log_error(f"Step {step} is missing variants for {self._image_path}!")
                renpy.show("black_screen_text", f"Step {step} is missing variants for {self._image_path}!")
                return

            (image_path, variant) = image_step.get_image(self._image_path, variant)

            renpy.call("show_ready_image", image_path, display_type)   
            return variant  
                
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

        char_obj = get_kwargs("char_obj", **kwargs)

        kwargs["loli_content"] = loli_content
        if char_obj != None:
            if not in_kwargs("name", **kwargs):
                kwargs["name"] = char_obj.get_name()
            if not in_kwargs("level", **kwargs):
                kwargs["level"] = char_obj.get_level()

        # replace in string path each key from kwargs with corresponding value
        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        if "<variant>" in image_path:
            max_variant = get_image_max_value("<variant>", image_path, 1)
            if max_variant >= 1:
                image_path = image_path.replace("<variant>", str(get_random_int(1, max_variant)))

        if in_kwargs("level", **kwargs):
            image_path = get_available_level(image_path, get_kwargs("level", **kwargs))

        if "<nude>" not in image_path:
            if renpy.loadable(image_path):
                return 0, image_path
            else:
                log_error(f"'{image_path}' could not be found!")
                return -1, image_path

        for i in range(0, nude_vision):
            new_image_path = image_path.replace("<nude>", str(i))
            if not renpy.loadable(new_image_path):
                if i > 0:
                    return i - 1, image_path
                elif i == 0:
                    log(f"|ERROR| '{new_image_path}' is missing!")
                    return -1, image_path

        return nude_vision, image_path
            
    def get_background(fallback: str, images: List[BGImage], char_obj: Char, **kwargs) -> Tuple[int, str]:
        """
        Returns the image path of the background with the highest priority that can be used.

        ### Parameters:
        1. fallback: str
            - The fallback image path.
        2. images: List[BGImage]
            - A list of all the background images.
        3. char_obj: Char
            - The character object to check the conditions with.
        4. **kwargs
            - The keyword arguments to check the conditions with.

        ### Returns:
        1. nude: int
            - The highest available nude-level.
        2. image_path: str
            - The image path of the background with the highest priority that can be used.
        """

        level = char_obj.get_level()
        if "name" not in kwargs.keys():
            kwargs["name"] = char_obj.get_name()
        if "loli_content" not in kwargs.keys():
            kwargs["loli"] = loli_content

        output_image = None
        output_nude = 0
        priority = -1

        for image in images:
            if not image.can_be_used(**kwargs):
                continue

            max_nude, output = image.get_image(level = level, **kwargs)

            if priority < image.get_priority() and max_nude >= 0:
                output_image = output
                output_nude = max_nude
                priority = image.get_priority()
        

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
        old_image = re.sub("<.+>", "0", old_image)
        old_image = old_image.replace("~#~", "<level>")

        for i in reversed(range(0, level + 1)):
            image = old_image.replace("<level>", str(i))
            if renpy.loadable(image):
                return path.replace("<level>", str(i))
        for i in range(0, 10):
            image = old_image.replace("<level>", str(i))
            if renpy.loadable(image):
                return path.replace("<level>", str(i))

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
            image = old_image.replace(key, str(i))
            if not renpy.loadable(image):
                return i - 1
        return end

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

        char_obj = get_kwargs('char_obj', None, **kwargs)
        if char_obj != None and 'name' not in kwargs.keys():
            kwargs['name'] = char_obj.get_name()

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        if char_obj != None:
            image_path = get_available_level(image_path, char_obj.get_level())

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

        char_obj = get_kwargs('char_obj', None, **kwargs)
        if char_obj != None and 'name' not in kwargs.keys():
            kwargs['name'] = char_obj.get_name()

        for key, value in kwargs.items():
            image_path = image_path.replace(f"<{key}>", str(value))

        if "<variant>" in image_path:
            variant = get_image_max_value("<variant>", image_path, 0, 100)
            image_path = image_path.replace(f"<variant>", str(variant))

        if char_obj != None:
            image_path = get_available_level(image_path, char_obj.get_level())

        return image_path
    
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


label show_idle_image(char_obj, fallback, bg_images):

    $ max_nude, image_path = get_background(fallback, bg_images, char_obj)

    call show_image_with_nude_var (image_path, max_nude) from show_idle_image_1

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

    call show_ready_image(image_path, display_type)
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

    $ image_path = refine_image_with_variant(path, **kwargs)

    call show_ready_image(image_path, display_type)
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
        call show_ext_image_with_nude_var(path)
    else:
        if check_image(path):
            if display_type == SHOW:
                show expression path with dissolveM
            elif display_type == SCENE:
                scene expression path with dissolveM
        else:
            $ log_error("Image not found: " + path)
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

    $ nude, image = get_image(image_path, **kwargs)
    call show_image_with_nude_var(image, nude) from show_ext_image_with_nude_var_1
    return

label show_image_with_nude_var(image_path, limit = 0):
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
            if len(paths) == 0 and not renpy.loadable(new_image_path):
                log_error(f"'{image_path}' is missing nude versions!")
                image_not_found = True
    
    if image_not_found:
        return

    show screen image_with_nude_var(paths, limit) with dissolveM

    return

screen image_with_nude_var(paths, limit = 2, nude = 0):
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
    
    $ path = paths[nude]

    image "[path]"

    if nude_vision != 0 and nude == limit and nude != 0:
        imagebutton:
            auto "icons/sight_disabled_%s.png"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 0)

    if nude == 0 and limit > 0:
        imagebutton:
            auto "icons/eye_target_%s.png"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 1)

    if nude == 1 and limit > 1:
        imagebutton:
            auto "icons/fire_iris_%s.png"
            focus_mask None
            xalign 0.0 yalign 0.0
            action Show("image_with_nude_var", dissolveM, paths, limit, 2)



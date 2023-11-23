init -2 python:
    from abc import ABC, abstractmethod
    from typing import List, Tuple
    import re

    class Image_Step:
        def __init__(self, step: int, variant = 1):
            self.step = step
            self.variant = variant

        def get_image(self, image_path: str, variant = -1) -> str:
            image_path = image_path.replace("<step>", str(self.step))

            if variant < 1 or variant > self.variant:
                variant = renpy.random.randint(1, self.variant)
            image_path = image_path.replace("<variant>", str(variant))

            return image_path, variant

    class Image_Obj(ABC):
        def __init__(self, image_path: str):
            self._image_path = image_path

    class Image_Series(Image_Obj):
        def __init__(self, image_path: str, **kwargs):
            image_path = refine_image(image_path, **kwargs)
            super().__init__(image_path)
            self.steps = []
            self.create_steps(image_path)

        def create_steps(self, image_path: str):
            if '<step>' in image_path:
                max_steps = get_image_max_value('<step>', image_path, 0, 100)

                for i in range(0, max_steps + 1):
                    image = image_path.replace('<step>', str(i))

                    variant = 1

                    if '<variant>' in image_path:
                        variant = get_image_max_value("<variant>", image_path, 1)
                        if variant == 0:
                            log(f"'{image_path}' has no variants!")
                            self.steps.append(None)
                            continue

                    self.steps.append(Image_Step(i, variant))
            return

        def show(self, step: int, display_type = SCENE, variant = -1) -> int:
            if step < 0 or step >= len(self.steps):
                log_val("image", self._image_path)
                log(f"Step {step} is out of range! (Min: 0, Max: {len(self.steps) - 1}))")
                return

            image_step = self.steps[step]
            if image_step == None:
                log(f"Step {step} is missing variants for {self._image_path}!")
                return

            (image_path, variant) = image_step.get_image(self._image_path, variant)

            renpy.call("show_ready_image", image_path, display_type)   
            return variant  
                
    class BGImage(Image_Obj):
        def __init__(self, image_path: str, priority: int, *conditions: Condition):
            super().__init__(image_path)
            self._conditions = list(conditions)
            self._priority = priority

        def can_be_used(self, **kwargs) -> bool:
            for condition in self._conditions:

                if condition.is_fulfilled(**kwargs):
                    continue
                return False

            return True

        def get_priority(self) -> int:
            return self._priority

        def get_image(self, **kwargs) -> str:
            return get_image(self._image_path, **kwargs)

        def can_get_image(self, **kwargs) -> bool:
            return get_image(self._image_path, **kwargs)[0] != -1

        def get_image_old(self, level: int, **kwargs) -> Tuple[int, str]:
            output = self._image_path

            max_nude = 0

            for key, value in kwargs.items():
                output = output.replace(f"<{key}>", str(value))

            path = output.replace("<nude>", "0")

            check_output = ""

            for i in reversed(range(0, level + 1)):
                image = path.replace("<level>", str(i))
                if renpy.loadable(image):
                    check_output = output.replace("<level>", str(i))
            if check_output == "":
                for i in range(0, 10):
                    image = path.replace("<level>", str(i))
                    if renpy.loadable(image):
                        check_output = output.replace("<level>", str(i))

            if check_output == "":
                log(f"'{self._image_path}' interpolated to '{output}' couldn't be found!")
                return -1, self._image_path

            if "<nude>" not in check_output:
                return 0, check_output

            i = 0
            while True:
                i += 1
                image = check_output.replace("<nude>", str(i))
                if renpy.loadable(image):
                    max_nude = i
                else:
                    break

            return max_nude, check_output

        def can_get_image_old(self, level: int, **kwargs) -> bool:
            output = self._image_path

            for key, value in kwargs.items():
                output = output.replace(f"<{key}>", str(value))
            
            path = output.replace("<nude>", "0")

            check_output = ""

            for i in reversed(range(0, level + 1)):
                image = path.replace("<level>", str(i))
                if renpy.loadable(image):
                    check_output = output.replace("<level>", str(i))
            if check_output == "":
                for i in range(0, 10):
                    image = path.replace("<level>", str(i))
                    if renpy.loadable(image):
                        check_output = output.replace("<level>", str(i))

            if check_output == "":
                log(f"'{self._image_path}' interpolated to '{output}' couldn't be found!")
                return False

            return True
    
    def get_image(image_path: str, **kwargs) -> Tuple[int, str]:
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
                log(f"'{image_path}' could not be found!")
                return -1, image_path

        for i in range(0, nude_vision):
            new_image_path = image_path.replace("<nude>", str(i))
            if not renpy.loadable(new_image_path):
                if i > 0:
                    return i - 1, image_path
                elif i == 0:
                    log(f"'{new_image_path}' is missing!")
                    return -1, image_path

        return nude_vision, image_path
            
    def get_background(fallback: str, images: List[BGImage], char_obj: Char, **kwargs) -> Tuple[int, str]:

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

    def get_image_max_value(key: str, image_path: str, start: int = 0, end: int = 10):
        old_image = image_path.replace(key, "~#~")
        old_image = re.sub("<.+>", "0", old_image)
        old_image = old_image.replace("~#~", key)

        for i in range(start, end):
            image = old_image.replace(key, str(i))
            if not renpy.loadable(image):
                return i - 1
        return end

    def refine_image(image_path: str, **kwargs) -> str:

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
    
    def check_image(image_path: str) -> bool:
            return renpy.loadable(image_path)


label show_image(path, display_type = SCENE, **kwargs):
    $ image_path = refine_image(path, **kwargs)

    call show_ready_image(image_path, display_type)
    return
    
label show_ready_image(path, display_type = SCENE):
    if "<nude>" in path:
        call show_image_with_nude_var(path)
    else:
        if check_image(path):
            if display_type == SHOW:
                show expression path with dissolveM
            elif display_type == SCENE:
                scene expression path with dissolveM
        else:
            $ log("Image not found: " + path)
    return

label show_ext_image_with_nude_var(image_path, **kwargs):
    $ nude, image = get_image(image_path, **kwargs)
    call show_image_with_nude_var(image, nude) from show_ext_image_with_nude_var_1
    return

label show_image_with_nude_var(image_path, limit = 0, nude = 0):
    if limit > nude_vision:
        $ limit = nude_vision

    $ paths = []
    $ image_not_found = False

    python:
        for i in range(0, limit + 1):
            new_image_path = image_path.replace("<nude>", str(i))
            paths.append(new_image_path)
            if len(paths) == 0 and not renpy.loadable(new_image_path):
                log(f"'{image_path}' is missing nude versions!")
                image_not_found = True
    
    if image_not_found:
        return

    show screen image_with_nude_var(paths, limit, nude) with dissolveM

    return

screen image_with_nude_var(paths, limit = 2, nude = 0):
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



init -2 python:
    class BGImage:
        def __init__(self, image_path, priority, *conditions):
            self._image_path = image_path
            self._conditions = list(conditions)
            self._priority = priority

        def can_be_used(self):
            for condition in self._conditions:

                if condition.is_fullfilled(None):
                    continue
                return False

            return True

        def get_priority(self):
            return self._priority

        def get_image(self, level, **kwargs):
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
                print(f"'{self._image_path}' interpolated to '{output}' couldn't be found!")
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


        def can_get_image(self, level, **kwargs):
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
                print(f"'{self._image_path}' interpolated to '{output}' couldn't be found!")
                return False

            return True
    
    def get_background(fallback, images, level, **kwargs):
        output_image = None
        output_nude = 0
        priority = -1

        for image in images:
            if not image.can_be_used():
                continue

            max_nude, output = image.get_image(level, **kwargs)

            if priority < image.get_priority() and max_nude >= 0:
                output_image = output
                output_nude = max_nude
                priority = image.get_priority()
        

        if output_image == None:
            return 0, fallback
        else:
            return output_nude, output_image


init python:
    import random
    import math

    class Shaker(object):

        anchors = {
            'top' : 0.0,
            'center' : 0.5,
            'bottom' : 1.0,
            'left' : 0.0,
            'right' : 1.0,
        }

        def __init__(self, start, child, dist, seed=None, samples=120):
            if start is None:
                start = child.get_placement()

            self.start   = [ self.anchors.get(i, i) for i in start ]
            self.dist    = dist
            self.child   = child
            # If no seed is set, we behave as before (true coincidence).
            self.seed    = None if seed is None else hash(seed) & 0xffffffff
            # How finely we divide t into discrete steps (≈ frames over the animation duration).
            self.samples = max(1, int(samples))

        def _rand_pair_at(self, idx):
            """
            Returns two deterministic random values in [0,1),
            derived from (seed, idx). For the same seed and idx
            produce identical values - perfect for synchronisation.
            """
            if self.seed is None:
                # Fallback: real random behaviour as before
                return renpy.random.random(), renpy.random.random()

            # Own local PRNG instance, initialised from (seed, idx).
            r = random.Random(self.seed + 9973 * idx)
            return r.random(), r.random()

        def __call__(self, t, sizes):
            # Float -> int helper
            def fti(x, r):
                if x is None:
                    x = 0
                if isinstance(x, float):
                    return int(x * r)
                else:
                    return x

            xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

            xpos = xpos - xanchor
            ypos = ypos - yanchor

            # Discretise the progress t into a stable index.
            # Same t + same seed => same idx => same "random" values.
            # (t runs [0..1], choice of floor/round does not matter, the main thing is consistency).
            idx = int(t * self.samples)

            rx, ry = self._rand_pair_at(idx)   # each in [0,1)
            jx = (rx * 2.0 - 1.0)              # -> [-1, 1]
            jy = (ry * 2.0 - 1.0)

            nx = xpos + (1.0 - t) * self.dist * jx
            ny = ypos + (1.0 - t) * self.dist * jy

            return (int(nx), int(ny), 0, 0)

    def _Shake(start, time, child=None, dist=100.0, seed=None, samples=120, **properties):
        move = Shaker(start, child, dist=dist, seed=seed, samples=samples)
        return renpy.display.layout.Motion(
            move,
            time,
            child,
            add_sizes=True,
            **properties
        )

    Shake = renpy.curry(_Shake)

init -99 python:
    from abc import ABC, abstractmethod

    def init_dialogue():
        global dialogue_manager
        dialogue_manager = DialogueManager()

    def clear_dialogue():
        global dialogue_manager
        if dialogue_manager != None:
            dialogue_manager.clear()
        dialogue_manager = None

    class Dialogue_Obj:
        def __init__(self, key: str, *pattern: str, **kwargs):
            self.key = key
            self.pattern = list(pattern)
            self.image = [""] * len(self.pattern)
            self.values = {}

            self.overrides = {}

            override_list = get_kwargs("overrides", [], **kwargs)
            if "overrides" in kwargs.keys():
                del kwargs["overrides"]

            for override in override_list:
                if override.index not in self.overrides.keys():
                    self.overrides[override.index] = []
                self.overrides[override.index].append(override)

            self.set_values(update_dict(kwargs, get_kwargs_values(**kwargs)))
            
            self.alt_keys = get_kwargs("alt_keys", [], **kwargs)

            self.config = update_dict({
                "alignX": -0.5,
                "alignY": 0.0,
                "rotation": 0.0,
            },
            get_kwargs("config", {}, **kwargs))

            self.config_init = update_dict({
                "alignX": -0.5,
                "alignY": 0.0,
                "rotation": 0.0,
            },
            get_kwargs("config", {}, **kwargs))

            self.config_override = [{
                "alignX": 0.0,
                "alignY": 0.0,
                "rotation": 0.0,
            }] * len(self.pattern)

        def get_x(self, index: int):
            return self.config["alignX"] + self.config_override[index]["alignX"]
        def get_y(self, index: int):
            return self.config["alignY"] + self.config_override[index]["alignY"]
        def get_rot(self, index: int):
            return self.config["rotation"] + self.config_override[index]["rotation"]
        def get_x_override(self, index: int):
            return self.config_override[index]["alignX"]
        def get_y_override(self, index: int):
            return self.config_override[index]["alignY"]
        def get_rot_override(self, index: int):
            return self.config_override[index]["rotation"]

        def set_values(self, data):
            self.values = data
            if "values" in self.values.keys():
                del self.values["values"]

        def hide_image_at(self, index: int):
            renpy.hide(self.key + str(index))

        def hide_all_images(self):
            for i in range(len(self.pattern)):
                self.hide_image_at(i)

        def update_overrides(self, index: int):
            x, y, rot = 0.0, 0.0, 0.0
            if index not in self.overrides.keys():
                self.config_override[index] = {
                    "alignX": 0.0,
                    "alignY": 0,
                    "rotation": 0.0,
                }
                return

            for override in self.overrides[index]:
                x_override, y_override, rot_override = override.get_override(**self.values)
                log_val("override value", self.values)
                log_val("x, y, rot", x_override, y_override, rot_override)
                x += x_override
                y += y_override
                rot += rot_override

            self.config_override[index] = {
                "alignX": x,
                "alignY": y,
                "rotation": rot,
            }

    class DialogueManager:
        def __init__(self):
            self.dialogue_objs = {}

        def register_obj(self, key: str, *pattern: str, **kwargs):
            self.dialogue_objs[key] = (Dialogue_Obj(key, *pattern, **kwargs))

        def display(self, key: str, *actions: Action):
            if key not in self.dialogue_objs.keys():
                return

            renpy.call("display_dialogue_image", self.dialogue_objs[key], list(actions))

        def set_background(self, image: str):
            pass

        def clear(self):
            for dialogue_obj in self.dialogue_objs.values():
                dialogue_obj.hide_all_images()

    class Action:
        def __init__(self, key: str, **kwargs):
            self.key = key
            self.values = kwargs

    class DialogueOverride:
        def __init__(self, index: int, conditions: Dict[str, Any], x_override = 0.0, y_override = 0.0, rot_override = 0.0):
            self.conditions = conditions
            self.index = index
            self.x_override = x_override
            self.y_override = y_override
            self.rot_override = rot_override

        def get_override(self, **kwargs) -> List[float]:
            for key, value in self.conditions.items():
                log_val("key, value", key, value)
                cond_value = get_kwargs(key, None, **kwargs)
                log_val("cond_value", cond_value)
                if value != cond_value and not check_in_value(value, cond_value):
                    log("no_override")
                    return 0.0, 0.0, 0.0        
            log("override")
            return self.x_override, self.y_override, self.rot_override


transform t_dialogue_position(xAlign, yAlign):
    xalign xAlign
    ypos yAlign
transform t_dialogue_rotation(rotation):
    rotate rotation
transform t_dialogue_move(duration, xAlign, yAlign):
    ease duration xalign xAlign ypos yAlign
transform t_dialogue_rotate(duration, rotation):
    ease duration rotate rotation
transform t_dialogue_move_rotate(duration, rotation, xAlign, yAlign):
    ease duration xalign xAlign ypos yAlign rotate rotation


label display_dialogue_image(dialogue_obj, actions):

    $ index = 0
    while (index < len(dialogue_obj.pattern)):
        $ pattern = dialogue_obj.pattern[index]

        if dialogue_obj.image[index] == "":
            $ dialogue_obj.update_overrides(index)

            $ dialogue_obj.image[index] = find_available_images(refine_image_with_alternatives(pattern, dialogue_obj.alt_keys, **dialogue_obj.values))
            $ renpy.show(
                dialogue_obj.key + str(index), 
                at_list = [t_dialogue_position(
                    dialogue_obj.get_x(index), 
                    dialogue_obj.get_y(index)
                )],
                what = Image(dialogue_obj.image[index]),
                tag = dialogue_obj.key + str(index)
            )

        $ index += 1

    while (len(actions) > 0):
        $ action = actions.pop(0)

        $ action_label = "dialogue_action_" + action.key

        if renpy.has_label(action_label):
            $ renpy.call(action_label, dialogue_obj, action.values)

    return

###########################
# region Dialogue Actions #
###########################

label dialogue_action_image(dialogue_obj, action):
    $ dialogue_obj.set_values(update_dict(dialogue_obj.values, action))
    
    $ index = 0
    while (index < len(dialogue_obj.pattern)):
        $ pattern = dialogue_obj.pattern[index]
        $ dialogue_obj.update_overrides(index)

        $ log_val("pattern", pattern)

        $ dialogue_obj.image[index] = find_available_images(refine_image_with_alternatives(pattern, dialogue_obj.alt_keys, **dialogue_obj.values))

        $ log_val("dialogue image", dialogue_obj.image[index])
        

        $ renpy.show(
            dialogue_obj.key + str(index), 
            at_list = [t_dialogue_position(
                dialogue_obj.get_x(index), 
                dialogue_obj.get_y(index)
            )],
            what = Image(dialogue_obj.image[index]),
            tag = dialogue_obj.key + str(index)
        )

        $ index += 1

    return

label dialogue_action_pos(dialogue_obj, action):
    $ alignX = get_kwargs("alignX", dialogue_obj.config["alignX"], **action)
    $ alignY = get_kwargs("alignY", dialogue_obj.config["alignY"], **action)
    $ duration = get_kwargs("duration", 0.3, **action)

    if preferences.transitions != 0 and persistent.transition_speed > 0:
        $ duration = duration / persistent.transition_speed

    $ index = 0
    while (index < len(dialogue_obj.pattern)):
        $ log_val("y override", dialogue_obj.get_y(index), alignY, dialogue_obj.get_y_override(index))
        $ log_val("pos", dialogue_obj.get_x(index), dialogue_obj.get_y(index))
        $ renpy.show(
            dialogue_obj.key + str(index), 
            at_list = [
                t_dialogue_position(
                    dialogue_obj.get_x(index), 
                    dialogue_obj.get_y(index)
                ), 
                t_dialogue_move(
                    duration, 
                    alignX + dialogue_obj.get_x_override(index), 
                    alignY + dialogue_obj.get_y_override(index)
                )
            ],
            what = Image(dialogue_obj.image[index]),
            tag = dialogue_obj.key + str(index)
        )

        $ index += 1

    $ dialogue_obj.config["alignX"] = alignX
    $ dialogue_obj.config["alignY"] = alignY

    return

label dialogue_action_rotate(dialogue_obj, action):
    $ rotation = get_kwargs("degree", dialogue_obj.config["rotation"], **action)
    $ duration = get_kwargs("duration", 0.3, **action)

    if preferences.transitions != 0 and persistent.transition_speed > 0:
        $ duration = duration / persistent.transition_speed

    $ index = 0
    while (index < len(dialogue_obj.pattern)):
        $ renpy.show(
            dialogue_obj.key + str(index), 
            at_list = [
                t_dialogue_position(
                    dialogue_obj.get_x(index), 
                    dialogue_obj.get_y(index)
                ),
                t_dialogue_rotation(dialogue_obj.get_rot(index)),
                t_dialogue_rotate(duration, rotation + dialogue_obj.get_rot_override(index))
            ],
            what = Image(dialogue_obj.image[index]),
            tag = dialogue_obj.key + str(index)
        )

        $ index += 1

    $ dialogue_obj.config["rotation"] = rotation

    return

label dialogue_action_pos_rotate(dialogue_obj, action):
    $ alignX = get_kwargs("alignX", dialogue_obj.config["alignX"], **action)
    $ alignY = get_kwargs("alignY", dialogue_obj.config["alignY"], **action)
    $ rotation = get_kwargs("degree", dialogue_obj.config["rotation"], **action)
    $ duration = get_kwargs("duration", 0.3, **action)

    if preferences.transitions != 0 and persistent.transition_speed > 0:
        $ duration = duration / persistent.transition_speed

    $ index = 0
    while (index < len(dialogue_obj.pattern)):
        $ renpy.show(
            dialogue_obj.key + str(index), 
            at_list = [
                t_dialogue_position(
                    dialogue_obj.get_x(index), 
                    dialogue_obj.get_y(index)
                ),
                t_dialogue_rotation(dialogue_obj.get_rot(index)),
                t_dialogue_move_rotate(
                    duration, 
                    rotation + dialogue_obj.get_rot_override(index), 
                    alignX + dialogue_obj.get_x_override(index), 
                    alignY + dialogue_obj.get_y_override(index)
                )
            ],
            what = Image(dialogue_obj.image[index]),
            tag = dialogue_obj.key + str(index)
        )

        $ index += 1

    $ dialogue_obj.config["alignX"] = alignX
    $ dialogue_obj.config["alignY"] = alignY
    $ dialogue_obj.config["rotation"] = rotation

    return

label dialogue_action_pause(dialogue_obj, action):
    $ duration = get_kwargs("duration", 0.0, **action)
    $ transition = get_kwargs("transition", True, **action)

    if preferences.transitions != 0 and persistent.transition_speed > 0 and transition:
        $ duration = duration / persistent.transition_speed

    $ log_val("pause duration", duration)

    $ renpy.pause(duration)

    return

label dialogue_action_shake(dialogue_obj, action):
    $ duration = get_kwargs("duration", 1.0, **action)
    $ max_distance = get_kwargs("max_distance", 15, **action)

    $ index = 0

    while (index < len(dialogue_obj.pattern)):
        # Use dedicated seed here, to give all images in the dialogue_obj the same shake.
        $ renpy.show(
            dialogue_obj.key + str(index), 
            at_list = [Shake(
                (dialogue_obj.get_x(index), dialogue_obj.get_y(index), dialogue_obj.get_x(index), dialogue_obj.get_y(index)), 
                duration, 
                dist = max_distance, 
                seed = dialogue_obj.key
            )],
            what = Image(dialogue_obj.image[index]),
            tag = dialogue_obj.key + str(index)
        )

        $ index += 1
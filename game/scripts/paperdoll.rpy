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

init -98 python:
    import copy

    ##################
    # region Presets #

    paperdoll_presets = {}
    paperdoll_temp_presets = set()

    def register_preset(key: str, *actions: PDAction):
        global paperdoll_presets
        paperdoll_presets[key] = list(actions)

    def register_temp_preset(key: str, *actions: PDAction):
        """
        Registers a preset that is available until the paperdoll manager is unloaded.

        Temporary presets use the same lookup path as permanent ones
        (`PDAPreset("key")`), but are discarded by `clear_temp_presets()`.
        Permanent presets registered via `register_preset` cannot be overwritten.
        Object presets are stored as `"object_key:preset_key"` temp entries.

        ### Parameters:
        1. key: str
            - The preset name used with `PDAPreset(key)`.
        2. *actions: PDAction
            - The actions that make up the preset.
        """
        global paperdoll_presets, paperdoll_temp_presets
        if key in paperdoll_presets and key not in paperdoll_temp_presets:
            log(
                "register_temp_preset: cannot override permanent preset '" + str(key) + "'",
                log_type="error",
                category="paperdoll",
            )
            return
        paperdoll_presets[key] = list(actions)
        paperdoll_temp_presets.add(key)

    def resolve_preset_key(key: str, paperdoll_obj=None) -> str:
        """
        Resolves a preset name for the displaying object.

        Looks up `"{obj.key}:{key}"` first, then `key` as-is. That lets
        `PDAPreset("intro")` on aona hit `aona:intro`, and
        `PDAPreset("aona:intro")` on emiko fall through to `aona:intro`.

        ### Parameters:
        1. key: str
            - The preset argument from `PDAPreset`.
        2. paperdoll_obj: Optional[Paperdoll_Obj]
            - The object currently running `.display()`.

        ### Returns:
        1. str
            - The resolved registry key, or `""` when neither exists.
        """
        global paperdoll_presets
        if paperdoll_obj is not None:
            scoped = str(paperdoll_obj.key) + ":" + str(key)
            if scoped in paperdoll_presets:
                return scoped
        if key in paperdoll_presets:
            return key
        return ""

    def get_preset(key: str, paperdoll_obj=None) -> List[PDAction]:
        global paperdoll_presets
        resolved = resolve_preset_key(key, paperdoll_obj)
        if resolved == "":
            log(
                "get_preset: preset '" + str(key) + "' not found",
                log_type="error",
                category="paperdoll",
            )
            return []
        return paperdoll_presets[resolved]

    def get_preset_with_overrides(key: str, paperdoll_obj=None, **kwargs) -> List[PDAction]:
        """
        Returns a deep copy of the preset actions with overrides applied.

        Copy-on-expand so `PDAPreset("x", duration=0.4)` does not mutate the
        stored preset for later callers.

        ### Parameters:
        1. key: str
            - The preset name (bare or `"object:name"`).
        2. paperdoll_obj: Optional[Paperdoll_Obj]
            - Display target used for scoped lookup.
        3. **kwargs
            - Overrides applied via each action's `overwrite_values`.

        ### Returns:
        1. List[PDAction]
            - A fresh action list, or empty when the preset is missing.
        """
        global paperdoll_presets
        resolved = resolve_preset_key(key, paperdoll_obj)
        if resolved == "":
            log(
                "get_preset_with_overrides: preset '" + str(key) + "' not found",
                log_type="error",
                category="paperdoll",
            )
            return []
        paperdoll_preset = copy.deepcopy(paperdoll_presets[resolved])
        for action in paperdoll_preset:
            if action.key != "preset":
                action.overwrite_values(**kwargs)
        return paperdoll_preset

    def clear_temp_presets():
        """
        Removes all presets registered via `register_temp_preset`.
        Permanent presets are left untouched.
        """
        global paperdoll_presets, paperdoll_temp_presets
        for key in list(paperdoll_temp_presets):
            if key in paperdoll_presets:
                del paperdoll_presets[key]
        paperdoll_temp_presets = set()

    def clear_presets():
        global paperdoll_presets, paperdoll_temp_presets
        paperdoll_presets = {}
        paperdoll_temp_presets = set()

    register_preset("outside", PDAMove(alignX = -1.5))
    register_preset("close_body", PDAMove(alignY = -0.1, zoom = 2.0))
    register_preset("close_body_center", PDAPreset("close_body"), PDAMove(alignX = 0.5))
    register_preset("close_body_right", PDAPreset("close_body"), PDAMove(alignX = 1.0))
    register_preset("close_body_left", PDAPreset("close_body"), PDAMove(alignX = 0.0))
    register_preset("upper_body", PDAMove(alignY = -0.1, zoom = 3.0))
    register_preset("upper_body_center", PDAPreset("upper_body"), PDAMove(alignX = 0.5))
    register_preset("upper_body_right", PDAPreset("upper_body"), PDAMove(alignX = 1.0))
    register_preset("upper_body_left", PDAPreset("upper_body"), PDAMove(alignX = 0.0))

    # endregion
    ##################


init -99 python:
    from abc import ABC, abstractmethod
    from typing import Any, Dict, List, Optional, Tuple, Union

    paperdoll_display_scale_cache = {}

    def paperdoll_get_display_size(pd_obj: "Paperdoll_Obj", index: int):
        """
        Returns the logical display size for a paperdoll layer, if configured.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object to query.
        2. index: int
            - The layer index to query.

        ### Returns:
        1. Optional[Tuple[int, int]]
            - The logical (width, height) in screen pixels, or None for native sizing.
        """
        if pd_obj.display_sizes is not None and index < len(pd_obj.display_sizes):
            layer_size = pd_obj.display_sizes[index]
            if layer_size is not None:
                return layer_size
        return pd_obj.display_size

    def paperdoll_compute_base_scale(pd_obj: "Paperdoll_Obj", index: int, image_path: str) -> float:
        """
        Computes the base scale factor that maps a native image to its logical display size.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object the image belongs to.
        2. index: int
            - The layer index the image belongs to.
        3. image_path: str
            - The resolved image path.

        ### Returns:
        1. float
            - 1.0 when no display size is configured, otherwise logical_height / native_height.
        """
        display_size = paperdoll_get_display_size(pd_obj, index)
        if display_size is None or image_path == "":
            return 1.0

        cache_key = (image_path, display_size[0], display_size[1])
        if cache_key in paperdoll_display_scale_cache:
            return paperdoll_display_scale_cache[cache_key]

        _, native_height = renpy.image_size(Image(image_path))
        logical_height = display_size[1]
        base_scale = logical_height / float(native_height)
        paperdoll_display_scale_cache[cache_key] = base_scale
        return base_scale

    def paperdoll_saturation(bw: bool) -> float:
        """
        Returns the SaturationMatrix factor for color or black-and-white display.

        ### Parameters:
        1. bw: bool
            - True for grayscale, False for full color.

        ### Returns:
        1. float
            - 0.0 for black-and-white, 1.0 for full color.
        """
        return 0.0 if bw else 1.0

    def apply_paperdoll_bw(displayable, bw: bool = False):
        """
        Optionally wraps a displayable with a grayscale color matrix.

        ### Parameters:
        1. displayable
            - The source displayable.
        2. bw: bool
            - True to force black-and-white display.

        ### Returns:
        1. Displayable
            - The original displayable, or a grayscale Transform.
        """
        if not bw:
            return displayable
        return Transform(displayable, matrixcolor=SaturationMatrix(0.0))

    def build_split_background(path_left: str, path_right: str, separator_width: int = 8, bw_left: bool = False, bw_right: bool = False):
        """
        Builds a Composite displayable from the left half of one image and the
        right half of another, with a white separator strip in the middle.

        ### Parameters:
        1. path_left: str
            - Image path used for the left half of the screen.
        2. path_right: str
            - Image path used for the right half of the screen.
        3. separator_width: int
            - Width of the white center strip in pixels.
        4. bw_left: bool
            - True to render the left half in black-and-white.
        5. bw_right: bool
            - True to render the right half in black-and-white.

        ### Returns:
        1. Displayable
            - A Composite covering the full screen size.
        """
        screen_w = config.screen_width
        screen_h = config.screen_height
        sep = max(0, int(separator_width))
        left_w = (screen_w - sep) // 2
        right_w = screen_w - left_w - sep

        left_native_w, left_native_h = renpy.image_size(Image(path_left))
        right_native_w, right_native_h = renpy.image_size(Image(path_right))

        left_half = apply_paperdoll_bw(
            Transform(
                Image(path_left),
                crop=(0, 0, left_native_w // 2, left_native_h),
                size=(left_w, screen_h),
            ),
            bw_left,
        )
        right_half = apply_paperdoll_bw(
            Transform(
                Image(path_right),
                crop=(right_native_w // 2, 0, right_native_w - right_native_w // 2, right_native_h),
                size=(right_w, screen_h),
            ),
            bw_right,
        )

        parts = [
            (0, 0), left_half,
        ]
        if sep > 0:
            parts.extend([
                (left_w, 0), Solid("#ffffff", xsize=sep, ysize=screen_h),
            ])
        parts.extend([
            (left_w + sep, 0), right_half,
        ])

        return Composite((screen_w, screen_h), *parts)

    paperdoll_manager = None

    def init_paperdoll_manager():
        """
        Initializes the paperdoll manager
        """
        global paperdoll_manager
        clear_temp_presets()
        paperdoll_manager = PaperdollManager()

    def unload_paperdoll_manager():
        """
        Unloads the paperdoll manager
        """
        global paperdoll_manager
        if paperdoll_manager != None:
            paperdoll_manager.clear()
        clear_temp_presets()
        paperdoll_manager = None

    def paperdoll_layer_displayable(path):
        """
        Builds the displayable for a paperdoll layer.

        Returns an Image for a resolved path, or a transparent Null when the path is
        empty (e.g. a missing / WIP asset), so a missing layer degrades to nothing
        instead of crashing the render with Image("").

        ### Parameters:
        1. path: str
            - The resolved image path (may be empty).

        ### Returns:
        1. Displayable
            - Image(path), or Null() when the path is empty.
        """
        if not path:
            return Null()
        return Image(path)

    paperdoll_native_size_cache = {}

    def paperdoll_native_size(path):
        """
        Returns the cached native pixel size of a paperdoll layer image.

        ### Parameters:
        1. path: str
            - The resolved image path.

        ### Returns:
        1. Tuple[int, int]
            - (width, height) in native pixels, or (0, 0) when path is empty.
        """
        if not path:
            return (0, 0)
        if path not in paperdoll_native_size_cache:
            paperdoll_native_size_cache[path] = renpy.image_size(Image(path))
        return paperdoll_native_size_cache[path]

    def paperdoll_flipped_layer(path, duration=0.0, start_xzoom=1.0, end_xzoom=1.0):
        """
        Wraps a layer image so `xzoom` eases around the sprite's horizontal center.

        The image sits in a Fixed of native size; the flip ATL uses `xalign 0.5` inside
        that box. Outer `xalign` / zoom then position the box, so the flip pivot is not
        the screen-align point (which would swing a right-aligned figure off-frame).

        ### Parameters:
        1. path: str
            - The resolved image path (may be empty).
        2. duration: float
            - Ease duration for the flip. `0.0` snaps.
        3. start_xzoom: float
            - `xzoom` at the start of the ease (`1.0` or `-1.0`).
        4. end_xzoom: float
            - `xzoom` at the end of the ease.

        ### Returns:
        1. Displayable
            - The boxed, flippable layer, or Null() when path is empty.
        """
        if not path:
            return Null()
        width, height = paperdoll_native_size(path)
        return Fixed(
            At(paperdoll_layer_displayable(path), t_paperdoll_flip(duration, start_xzoom, end_xzoom)),
            xysize = (int(width), int(height)),
        )

    def paperdoll_layer_for_show(pd_obj, index, duration=0.0, start_xzoom=None, end_xzoom=None):
        """
        Builds the showable layer for a paperdoll object, holding or easing its flip.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.
        2. index: int
            - The layer index.
        3. duration: float
            - Flip ease duration. `0.0` holds the current (or given) facing.
        4. start_xzoom: float
            - Optional start `xzoom`; defaults to the stored flip.
        5. end_xzoom: float
            - Optional end `xzoom`; defaults to the stored flip.

        ### Returns:
        1. Displayable
            - The boxed layer to pass as `what` in `renpy.show`.
        """
        flip = pd_obj.get_flip()
        if start_xzoom is None:
            start_xzoom = flip
        if end_xzoom is None:
            end_xzoom = flip
        layer = paperdoll_flipped_layer(pd_obj.image[index], duration, start_xzoom, end_xzoom)
        return layer

    PAPERDOLL_BG_ZORDER = -100
    PAPERDOLL_LAYER_ZORDER = 0
    PAPERDOLL_BEHIND_ZORDER = -1

    def paperdoll_layer_zorder(pd_obj) -> int:
        """
        Returns the renpy.show zorder for a paperdoll object's layers.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.

        ### Returns:
        1. int
            - `-1` when `behind` is set (still above the background), else `0`.
        """
        if getattr(pd_obj, "behind", False):
            return PAPERDOLL_BEHIND_ZORDER
        return PAPERDOLL_LAYER_ZORDER

    def paperdoll_is_visible(pd_obj) -> bool:
        """
        Returns True when at least one layer has a resolved image path.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.

        ### Returns:
        1. bool
            - Whether the object has been shown at least once.
        """
        return any(img != "" for img in pd_obj.image)

    def paperdoll_capture_world(pd_obj) -> Dict[str, Any]:
        """
        Snapshots the object's current world transform from `config`.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.

        ### Returns:
        1. Dict[str, Any]
            - alignX, alignY, zoom, rotation, flip.
        """
        return {
            "alignX": pd_obj.config["alignX"],
            "alignY": pd_obj.config["alignY"],
            "zoom": pd_obj.config["zoom"],
            "rotation": pd_obj.config.get("rotation", 0.0),
            "flip": pd_obj.get_flip(),
        }

    def paperdoll_write_world_to_config(pd_obj, world: Dict[str, Any]):
        """
        Writes a world transform dict into the object's shared `config`.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.
        2. world: Dict[str, Any]
            - World-space transform keys.
        """
        pd_obj.config["alignX"] = world["alignX"]
        pd_obj.config["alignY"] = world["alignY"]
        pd_obj.config["zoom"] = world["zoom"]
        pd_obj.config["rotation"] = world.get("rotation", 0.0)
        pd_obj.config["flip"] = world["flip"]

    def paperdoll_parent_box_screen_frac(parent, parent_world: Dict[str, Any]) -> Tuple[float, float]:
        """
        Returns the parent's on-screen box size as fractions of the screen.

        Uses `display_size * zoom` when set; otherwise native layer-0 size times
        effective zoom. Falls back to `(0, 0)` when neither is available.

        ### Parameters:
        1. parent: Paperdoll_Obj
            - The parent object.
        2. parent_world: Dict[str, Any]
            - Parent world transform (uses `zoom`).

        ### Returns:
        1. Tuple[float, float]
            - `(width_frac, height_frac)` of the screen.
        """
        zoom = float(parent_world.get("zoom", 1.0))
        size = paperdoll_get_display_size(parent, 0)
        if size is not None:
            dw = float(size[0]) * zoom
            dh = float(size[1]) * zoom
        else:
            path = parent.image[0] if parent.image else ""
            nw, nh = paperdoll_native_size(path) if path else (0, 0)
            if nh <= 0 or nw <= 0:
                return 0.0, 0.0
            scale = parent.scale_factors[0] if parent.scale_factors else 1.0
            dw = float(nw) * zoom * scale
            dh = float(nh) * zoom * scale
        screen_w = float(config.screen_width)
        screen_h = float(config.screen_height)
        if screen_w <= 0 or screen_h <= 0:
            return 0.0, 0.0
        return dw / screen_w, dh / screen_h

    def paperdoll_world_config(obj, parent_world: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Composes world-space transform by folding the full parent chain.

        Unparented objects use `config` as world. Parented objects apply `local`
        against the parent's world.

        With `space="screen"` (default), `local.alignX/Y` are screen-unit offsets
        (`alignX` flipped with parent facing). With `space="parent"`, `local.alignX/Y`
        are 0–1 points on the parent's `display_size` box (`0` left/top, `0.5`
        centre, `1` right/bottom); X mirrors with parent flip around the box centre.

        ### Parameters:
        1. obj: Paperdoll_Obj
            - The object to compose.
        2. parent_world: Optional[Dict[str, Any]]
            - Optional already-computed parent world (for end-state fan-out).

        ### Returns:
        1. Dict[str, Any]
            - World-space alignX, alignY, zoom, rotation, flip.
        """
        if obj.parent is None:
            return paperdoll_capture_world(obj)

        if parent_world is None:
            parent = paperdoll_manager.get_obj(obj.parent)
            parent_world = paperdoll_world_config(parent)
        else:
            parent = paperdoll_manager.get_obj(obj.parent)

        flip = parent_world["flip"] * obj.local["flip"]
        zoom = parent_world["zoom"] * obj.local["zoom"]
        rotation = parent_world["rotation"] + obj.local.get("rotation", 0.0)

        if getattr(obj, "space", "screen") == "parent":
            pw, ph = paperdoll_parent_box_screen_frac(parent, parent_world)
            ax = parent_world["alignX"]
            ay = parent_world["alignY"]
            u = float(obj.local["alignX"])
            v = float(obj.local["alignY"])
            # Mirror attach X around the parent box centre when the parent faces left
            u_eff = 0.5 + (u - 0.5) * parent_world["flip"]
            # transform_anchor + xalign: point U on the sprite maps to
            # A + (U - A) * (box_w / screen_w)
            alignX = ax + (u_eff - ax) * pw
            # ypos places the top of the box; V=0 top, V=1 bottom
            alignY = ay + v * ph
        else:
            alignX = parent_world["alignX"] + obj.local["alignX"] * parent_world["flip"]
            alignY = parent_world["alignY"] + obj.local["alignY"]

        return {
            "flip": flip,
            "zoom": zoom,
            "alignY": alignY,
            "alignX": alignX,
            "rotation": rotation,
        }

    def paperdoll_compose_subtree_worlds(obj, obj_world: Dict[str, Any]) -> List[Tuple[Any, Dict[str, Any]]]:
        """
        Builds (object, world) pairs for `obj` and all descendants, parent-first.

        ### Parameters:
        1. obj: Paperdoll_Obj
            - Subtree root.
        2. obj_world: Dict[str, Any]
            - World transform for `obj`.

        ### Returns:
        1. List[Tuple[Paperdoll_Obj, Dict[str, Any]]]
            - Depth-first list with parents before children.
        """
        result = [(obj, obj_world)]
        for child_key in obj.children:
            if paperdoll_manager is None or child_key not in paperdoll_manager.paperdoll_objs:
                continue
            child = paperdoll_manager.get_obj(child_key)
            child_world = paperdoll_world_config(child, parent_world=obj_world)
            result.extend(paperdoll_compose_subtree_worlds(child, child_world))
        return result

    def paperdoll_iter_descendants(pd_obj):
        """
        Yields all descendant paperdoll objects depth-first.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - Subtree root (not yielded).
        """
        for child_key in pd_obj.children:
            if paperdoll_manager is None or child_key not in paperdoll_manager.paperdoll_objs:
                continue
            child = paperdoll_manager.get_obj(child_key)
            yield child
            for desc in paperdoll_iter_descendants(child):
                yield desc

    def paperdoll_show_layers(pd_obj, at_list, flip_duration=0.0, start_xzoom=None, end_xzoom=None, skip_empty=True):
        """
        Shows every layer of a paperdoll with a shared zorder and at_list.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The paperdoll object.
        2. at_list: list or callable
            - Transform list, or `callable(index) -> list`.
        3. flip_duration: float
            - Passed to `paperdoll_layer_for_show`.
        4. start_xzoom: Optional[float]
            - Flip ease start.
        5. end_xzoom: Optional[float]
            - Flip ease end.
        6. skip_empty: bool
            - When True, skip layers whose image path is still empty.
        """
        z = paperdoll_layer_zorder(pd_obj)
        for index in range(len(pd_obj.pattern)):
            if skip_empty and pd_obj.image[index] == "":
                continue
            transforms = at_list(index) if callable(at_list) else at_list
            renpy.show(
                pd_obj.key + str(index),
                tag=pd_obj.key + str(index),
                what=paperdoll_layer_for_show(pd_obj, index, flip_duration, start_xzoom, end_xzoom),
                at_list=transforms,
                zorder=z,
            )

    def paperdoll_show_move(pd_obj, duration, start_world, end_world, start_flip=None, end_flip=None):
        """
        Eases a paperdoll (and writes end world into config) from start to end world.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - The object to move.
        2. duration: float
            - Ease duration.
        3. start_world: Dict[str, Any]
            - World transform at the start of the ease.
        4. end_world: Dict[str, Any]
            - World transform at the end of the ease.
        5. start_flip: Optional[float]
            - Optional flip ease start; defaults to start_world flip.
        6. end_flip: Optional[float]
            - Optional flip ease end; defaults to end_world flip.
        """
        if start_flip is None:
            start_flip = start_world["flip"]
        if end_flip is None:
            end_flip = end_world["flip"]
        flip_duration = duration if start_flip != end_flip else 0.0

        if paperdoll_is_visible(pd_obj):
            def _at_list(index):
                return [
                    t_paperdoll_move(
                        duration,
                        start_world["alignX"] + pd_obj.get_override_config("alignX", index),
                        start_world["alignY"] + pd_obj.get_override_config("alignY", index),
                        (start_world["zoom"] + pd_obj.get_override_config("zoom", index)) * pd_obj.scale_factors[index],
                        end_world["alignX"] + pd_obj.get_override_config("alignX", index),
                        end_world["alignY"] + pd_obj.get_override_config("alignY", index),
                        (end_world["zoom"] + pd_obj.get_override_config("zoom", index)) * pd_obj.scale_factors[index],
                    ),
                    t_paperdoll_bw(paperdoll_saturation(pd_obj.is_bw())),
                ]
            paperdoll_show_layers(
                pd_obj,
                _at_list,
                flip_duration=flip_duration,
                start_xzoom=start_flip,
                end_xzoom=end_flip,
            )
        paperdoll_write_world_to_config(pd_obj, end_world)

    def paperdoll_apply_subtree_transform(pd_obj, end_world, duration, start_worlds=None):
        """
        Moves `pd_obj` and all descendants from captured start worlds to composed ends.

        ### Parameters:
        1. pd_obj: Paperdoll_Obj
            - Subtree root whose end world is `end_world`.
        2. end_world: Dict[str, Any]
            - New world transform for `pd_obj`.
        3. duration: float
            - Shared ease duration for the whole subtree.
        4. start_worlds: Optional[Dict[str, Dict]]
            - Pre-captured worlds keyed by object key; captured now when omitted.
        """
        if start_worlds is None:
            start_worlds = {pd_obj.key: paperdoll_capture_world(pd_obj)}
            for desc in paperdoll_iter_descendants(pd_obj):
                start_worlds[desc.key] = paperdoll_capture_world(desc)

        for obj, world in paperdoll_compose_subtree_worlds(pd_obj, end_world):
            start = start_worlds.get(obj.key, paperdoll_capture_world(obj))
            paperdoll_show_move(obj, duration, start, world)

    def paperdoll_would_cycle(child_key: str, parent_key: str) -> bool:
        """
        Returns True if attaching `child_key` under `parent_key` would create a cycle.

        Walks ancestors of `parent_key`; a hit on `child_key` means a cycle.

        ### Parameters:
        1. child_key: str
            - Key of the object being parented.
        2. parent_key: str
            - Proposed parent key.

        ### Returns:
        1. bool
            - True when the link would cycle.
        """
        if child_key == parent_key:
            return True
        current = parent_key
        seen = set()
        while current is not None:
            if current == child_key:
                return True
            if current in seen:
                return True
            seen.add(current)
            if paperdoll_manager is None or current not in paperdoll_manager.paperdoll_objs:
                break
            current = paperdoll_manager.get_obj(current).parent
        return False

    class Paperdoll_Obj:
        """
        A class that represents a paperdoll object
        This class is used to carry the data for an individual paperdoll object

        ### Attributes:
        1. key: str
            - The key of the paperdoll object
        2. pattern: List[str]
            - The patterns of the paperdoll object
        3. image: List[str]
            - The images of the paperdoll object
        4. values: Dict[str, Any]
            - The values of the paperdoll object
        5. overrides: Dict[int, List[PaperdollOverride]]
            - The overrides of the paperdoll object
            - The key is the index of the pattern and the value is a list of overrides
            - The overrides are of type PaperdollOverride
        6. alt_keys: List[str]
            - The alternative keys of the paperdoll object
            - The alternative keys are used to use alternative images if the main image is not available
        7. config: Dict[str, Any]
            - The configuration of the paperdoll object
            - The configuration is used to configure the position and rotation of the paperdoll object
        8. config_override: List[Dict[str, Any]]
            - The override configuration of the paperdoll object
            - The override configuration is used to override the initial configuration
        9. display_size: Optional[Tuple[int, int]]
            - The logical display size (width, height) for all layers
            - Used to normalize high-resolution assets to their intended on-screen size
        10. display_sizes: Optional[List[Optional[Tuple[int, int]]]]
            - Per-layer logical display sizes; overrides display_size for specific layers
        11. scale_factors: List[float]
            - Cached base scale per layer, computed when an image is loaded

        ### Parameters:
        1. key: str
            - The key of the paperdoll object
        2. *pattern: str
            - The patterns of the paperdoll object
        3. **kwargs: Dict[str, Any]
            - Additional keyword arguments to pass to the paperdoll object
            - possible kwargs:
                - overrides: List[PaperdollOverride]
                    - overrides are used to include values changes based on specific conditions
                - alt_keys: List[str]
                    - alternative keys are used to use alternative images if the main image is not available
                - config: Dict[str, Any]
                    - used to set the initial configuration on object creation
                - display_size: Tuple[int, int]
                    - logical display size for all layers; omit to keep native pixel sizing
                - display_sizes: List[Optional[Tuple[int, int]]]
                    - per-layer logical display sizes
                - local: Dict[str, Any]
                    - relative transform when parented (alignX/alignY/zoom/rotation/flip)
                - space: str
                    - `"screen"` (default): local align is a screen-unit offset;
                        `"parent"`: local align is 0–1 on the parent's display_size box
                - behind: bool
                    - when True, layers use zorder -1 (still above the background)

        ### Methods:
        7. set_values(data: Dict[str, Any])
            - Sets the values of the paperdoll object
        8. hide_image_at(index: int)
            - Hides the image of the paperdoll object at the given index
        9. hide_all_images(recurse: bool = True)
            - Hides all the images of the paperdoll object (optionally descendants)
        10. update_overrides(index: int)
            - Updates the overrides of the paperdoll object at the given index
        11. update_scale_factor(index: int, image_path: str)
            - Recomputes and stores the base scale factor for a loaded layer image
        12. get_effective_zoom(index: int, zoom: float = None) -> float
            - Returns config zoom multiplied by the layer base scale factor
        """

        def __init__(self, key: str, *pattern: str, **kwargs):
            self.key = key
            self.pattern = list(pattern)
            self.image = [""] * len(self.pattern)
            self.values = {}

            self.overrides = {}

            self.parent = None
            self.children = []
            self.behind = bool(get_kwargs("behind", False, **kwargs))
            if "behind" in kwargs.keys():
                del kwargs["behind"]

            space = get_kwargs("space", "screen", **kwargs)
            if "space" in kwargs.keys():
                del kwargs["space"]
            if space not in ("screen", "parent"):
                log(
                    "Paperdoll_Obj: space must be 'screen' or 'parent', got '" + str(space) + "'",
                    log_type="error",
                    category="paperdoll",
                )
                space = "screen"
            self.space = space

            local_kw = get_kwargs("local", {}, **kwargs)
            if "local" in kwargs.keys():
                del kwargs["local"]
            self.local = {
                "alignX": float(local_kw.get("alignX", 0.0)),
                "alignY": float(local_kw.get("alignY", 0.0)),
                "zoom": float(local_kw.get("zoom", 1.0)),
                "rotation": float(local_kw.get("rotation", 0.0)),
                "flip": float(local_kw.get("flip", 1.0)),
            }

            self.display_size = get_kwargs("display_size", None, **kwargs)
            self.display_sizes = get_kwargs("display_sizes", None, **kwargs)
            if "display_size" in kwargs.keys():
                del kwargs["display_size"]
            if "display_sizes" in kwargs.keys():
                del kwargs["display_sizes"]

            self.scale_factors = [1.0] * len(self.pattern)

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
                "zoom": 1.0,
                "blur": 0.0,
                "bw": False,
                "flip": 1.0,
            },
            get_kwargs("config", {}, **kwargs))

            self.config_override = [{
                "alignX": 0.0,
                "alignY": 0.0,
                "rotation": 0.0,
                "zoom": 1.0,
                "blur": 0.0,
            }] * len(self.pattern)

        def get_config(self, key: str, index: int):
            return self.config[key] + self.config_override[index][key]
        def get_override_config(self, key: str, index: int):
            return self.config_override[index][key]

        def is_bw(self) -> bool:
            """
            Returns whether this paperdoll is displayed in black-and-white.

            ### Returns:
            1. bool
                - True when grayscale display is enabled.
            """
            return bool(self.config.get("bw", False))

        def set_values(self, data):
            """
            Sets the values of the paperdoll object
            The values are used to provide data to the paperdoll object

            ### Parameters:
            1. data: Dict[str, Any]
                - The data to set the values of the paperdoll object
            """

            self.values = data
            if "values" in self.values.keys():
                del self.values["values"]

        def get_value(self, key: str) -> Any:
            return self.values[key]

        def hide_image_at(self, index: int):
            """
            Hides the image of the paperdoll object at the given index
            ### Parameters:
            1. index: int
                - The index of the image to hide
            """
            renpy.hide(self.key + str(index))

        def hide_all_images(self, recurse: bool = True):
            """
            Hides all the images of the paperdoll object.

            ### Parameters:
            1. recurse: bool
                - When True, also hides all descendant children.
            """
            for i in range(len(self.pattern)):
                self.hide_image_at(i)
            if recurse:
                for child_key in list(self.children):
                    if paperdoll_manager is not None and child_key in paperdoll_manager.paperdoll_objs:
                        paperdoll_manager.get_obj(child_key).hide_all_images(recurse=True)

        def set_override_config(self, index: int, config: Dict[str, Any]):
            """
            Sets the override configuration of the paperdoll object at the given index
            ### Parameters:
            1. index: int
                - The index of the pattern to set the override configuration for
            2. config: Dict[str, Any]
                - The configuration to set the override configuration of the paperdoll object at the given index
            """
            self.config_override[index] = config

        def update_overrides(self, index: int):
            """
            Updates the overrides of the paperdoll object at the given index
            ### Parameters:
            1. index: int
                - The index of the pattern to update the overrides for
            """
            x, y, rot, blur, zoom = 0.0, 0.0, 0.0, 0.0, 0.0
            if index not in self.overrides.keys():
                self.config_override[index] = {
                    "alignX": 0.0,
                    "alignY": 0,
                    "rotation": 0.0,
                    "zoom": 0.0,
                    "blur": 0.0,
                }
                return

            for override in self.overrides[index]:
                x_override, y_override, rot_override, blur_override, zoom_override = override.get_override(**self.values)
                x += x_override
                y += y_override
                rot += rot_override
                blur += blur_override
                zoom += zoom_override

            self.config_override[index] = {
                "alignX": x,
                "alignY": y,
                "rotation": rot,
                "zoom": zoom,
                "blur": blur
            }

        def update_scale_factor(self, index: int, image_path: str):
            """
            Recomputes and stores the base scale factor for a loaded layer image.

            ### Parameters:
            1. index: int
                - The layer index to update.
            2. image_path: str
                - The resolved image path for the layer.
            """
            self.scale_factors[index] = paperdoll_compute_base_scale(self, index, image_path)

        def resolve_image(self, index: int) -> str:
            """
            Resolves and stores the layer image path, then updates its scale factor.

            ### Parameters:
            1. index: int
                - The layer index to resolve.

            ### Returns:
            1. str
                - The resolved image path (empty when no asset matches, e.g. a WIP layer).
            """
            resolved = find_available_images(refine_image_with_alternatives(self.pattern[index], self.alt_keys, **self.values))
            if resolved == "":
                # Log the pattern with concrete values filled in (unmatched placeholders
                # stay as <key>) so a specific missing image is easy to identify.
                log(f"'{refine_image(self.pattern[index], **self.values)}' could not be found!", log_type="error", category="image")
            self.image[index] = resolved
            self.update_scale_factor(index, resolved)
            return resolved

        def get_effective_zoom(self, index: int, zoom: float = None) -> float:
            """
            Returns config zoom multiplied by the layer base scale factor.
            Placement transforms use this combined value as their `zoom`.

            ### Parameters:
            1. index: int
                - The layer index to query.
            2. zoom: float
                - Optional zoom override; defaults to the layer config zoom.

            ### Returns:
            1. float
                - Combined zoom to pass to display transforms (config zoom × base scale).
            """
            if zoom is None:
                zoom = self.get_config("zoom", index)
            return zoom * self.scale_factors[index]

        def get_flip(self) -> float:
            """
            Returns the stored horizontal flip as an `xzoom` multiplier.

            ### Returns:
            1. float
                - `1.0` unflipped, `-1.0` mirrored. Defaults to `1.0`.
            """
            return self.config.get("flip", 1.0)

    class PaperdollManager:
        """
        This class is used to manage the paperdoll objects and the background image

        To use it first register the paperdoll objects you want to use with the register_obj method
        Then you can display the paperdoll objects with the display method
        You can also set the background image with the set_background method
        Or a split background with set_background_split
        And you can hide the background image with the hide_background method
        And you can clear the paperdoll objects with the clear method

        ### Attributes:
        1. paperdoll_objs: Dict[str, Paperdoll_Obj]
            - The paperdoll objects
        2. background_image: Union[str, Displayable]
            - The background image path or a Composite displayable
        3. background_blur: float
            - The background blur
        4. background_bw: bool
            - True to display a single background in black-and-white

        ### Methods:
        1. register_obj(key: str, *pattern: str, **kwargs)
            - Registers a paperdoll object with the given key and pattern
        2. get_obj(key: str) -> Paperdoll_Obj
            - Returns the paperdoll object with the given key
        3. display(key: str, *actions: Action)
            - Displays the paperdoll object with the given key and actions
        4. background(*actions: Action)
            - Displays the background image and actions
        5. set_background(pattern = None, blur: Union[bool, float] = False, blur_duration: float = 0.0, bw: bool = False, alt_keys: List[str] = [], **kwargs)
            - Sets the background from a pattern, concrete path, or Image_Series step (`image[n]`)
        6. set_background_split(pattern_left = None, pattern_right = None, blur: Union[bool, float] = False, blur_duration: float = 0.0, separator_width: int = 8, bw_left: bool = False, bw_right: bool = False, alt_keys: List[str] = [], **kwargs)
            - Sets a split background from patterns / concrete paths / Image_Series steps
        7. hide_background()
            - Hides the background image
        8. clear()
            - Clears all the paperdoll objects and the background image

        """
        def __init__(self):
            self.paperdoll_objs = {}
            self.background_image = ""
            self.background_blur = 0.0
            self.background_bw = False

            self.background_pattern = ""
            self.background_values = {}

            self.presets = {}

        def register_obj(self, key: str, *pattern: str, **kwargs):
            """
            Registers a paperdoll object and optional object presets / parent link.

            ### Parameters:
            1. key: str
                - Unique object key (also the show-tag prefix).
            2. *pattern: str
                - One pattern per layer, bottom to top.
            3. **kwargs
                - Passed to `Paperdoll_Obj`, plus:
                - presets: List[PaperdollPreset] — stored as temp `"key:preset"` entries
                - parent: str — parent object key (must already be registered)
            """
            presets = get_kwargs("presets", [], **kwargs)
            if "presets" in kwargs.keys():
                del kwargs["presets"]

            parent_key = get_kwargs("parent", None, **kwargs)
            if "parent" in kwargs.keys():
                del kwargs["parent"]

            obj = Paperdoll_Obj(key, *pattern, **kwargs)
            self.paperdoll_objs[key] = obj

            for preset in presets:
                preset_key = getattr(preset, "key", None)
                actions = getattr(preset, "actions", None)
                if preset_key is None or actions is None:
                    log(
                        "register_obj: presets entry is not a PaperdollPreset",
                        log_type="error",
                        category="paperdoll",
                    )
                    continue
                if ":" in str(preset_key):
                    log(
                        "register_obj: object preset key '" + str(preset_key) + "' must not contain ':'",
                        log_type="error",
                        category="paperdoll",
                    )
                    continue
                register_temp_preset(str(key) + ":" + str(preset_key), *actions)

            if parent_key is not None:
                self._attach_parent(obj, parent_key)

        def _attach_parent(self, obj, parent_key: str):
            """
            Links `obj` under `parent_key` after cycle and existence checks.

            ### Parameters:
            1. obj: Paperdoll_Obj
                - The child object.
            2. parent_key: str
                - Key of the parent (must already be registered).
            """
            if parent_key not in self.paperdoll_objs:
                log(
                    "register_obj: parent '" + str(parent_key) + "' not registered for '" + str(obj.key) + "'",
                    log_type="error",
                    category="paperdoll",
                )
                return
            if paperdoll_would_cycle(obj.key, parent_key):
                log(
                    "register_obj: parenting '" + str(obj.key) + "' under '" + str(parent_key) + "' would cycle",
                    log_type="error",
                    category="paperdoll",
                )
                return
            parent = self.paperdoll_objs[parent_key]
            obj.parent = parent_key
            if obj.key not in parent.children:
                parent.children.append(obj.key)
            paperdoll_write_world_to_config(obj, paperdoll_world_config(obj))

        def get_obj(self, key: str) -> Paperdoll_Obj:
            return self.paperdoll_objs[key]

        def display(self, key: str, *actions: Action):
            if key not in self.paperdoll_objs.keys():
                return

            renpy.call("display_paperdoll_image", self.paperdoll_objs[key], list(actions))

        def background(self, *actions: Action):
            pass

        def _resolve_background_path(self, pattern, alt_keys: List[str] = [], **kwargs) -> str:
            """
            Resolves a background source to an available image path.

            Accepts a paperdoll-style pattern string, or a concrete path such as
            the result of `image[step]` on an `Image_Series` (which may be None).

            If the pattern does not resolve to an image, it is retried as a pattern
            *key*: when the author passes the name of a `Pattern` registered on the
            event (available via kwargs `image_patterns` / `frag_image_patterns`),
            the underlying pattern string and its alternative keys are resolved.

            ### Parameters:
            1. pattern: Optional[str]
                - Image pattern, concrete path, or None.
            2. alt_keys: List[str]
                - Alternative keys for image refinement (pattern mode only).
            3. **kwargs
                - Values passed to image refinement (pattern mode only).

            ### Returns:
            1. str
                - Resolved image path, or empty string if none was found.
            """
            if pattern is None or pattern == "":
                return ""
            if not isinstance(pattern, str):
                log(
                    "set_background: expected str or None, got " + type(pattern).__name__,
                    log_type="error",
                    category="paperdoll",
                )
                return ""

            # Concrete path from Image_Series.__getitem__ / direct file path
            # (.png patterns also resolve a matching .webp, and vice versa)
            resolved_concrete = find_loadable_image(pattern)
            if resolved_concrete != "":
                return resolved_concrete

            # Event-style path that still contains <nude> (e.g. raw get_image result)
            if "<nude>" in pattern:
                nude, resolved = get_image(pattern, **kwargs)
                if nude < 0 or resolved == "":
                    return ""
                if "<nude>" in resolved:
                    for level in [0] + list(range(nude, 0, -1)):
                        candidate = find_loadable_image(resolved.replace("<nude>", str(level)))
                        if candidate != "":
                            return candidate
                    return ""
                resolved = find_loadable_image(resolved)
                if resolved != "":
                    return resolved
                return ""

            images = refine_image_with_alternatives(pattern, alt_keys, **kwargs)
            resolved = find_available_images(images) if len(images) > 0 else ""
            if resolved != "":
                return resolved

            # Fallback: `pattern` may be a pattern *key* the author registered on the
            # event via Pattern(...), passed through kwargs as image_patterns /
            # frag_image_patterns. If so, resolve the underlying pattern string using
            # the Pattern's own alternative keys (merged with any passed in).
            frag_patterns = get_kwargs('frag_image_patterns', {}, **kwargs)
            image_patterns = get_kwargs('image_patterns', {}, **kwargs)
            pattern_obj = frag_patterns.get(pattern)
            if pattern_obj is None:
                pattern_obj = image_patterns.get(pattern)
            if isinstance(pattern_obj, Pattern):
                combined_alt_keys = list(alt_keys)
                for key in pattern_obj.get_alternative_keys():
                    if key not in combined_alt_keys:
                        combined_alt_keys.append(key)
                images = refine_image_with_alternatives(pattern_obj.get_path(), combined_alt_keys, **kwargs)
                if len(images) > 0:
                    return find_available_images(images)

            return ""

        def _apply_background_blur(self, blur: Union[bool, float]):
            """
            Stores the background blur value.

            ### Parameters:
            1. blur: Union[bool, float]
                - True maps to 10.0, False to 0.0, floats are used as-is.
            """
            if isinstance(blur, bool):
                self.background_blur = 10.0 if blur else 0.0
            else:
                self.background_blur = blur

        def set_background(self, pattern = None, blur: Union[bool, float] = False, blur_duration: float = 0.0, bw: bool = False, alt_keys: List[str] = [], **kwargs):
            """
            Sets the background image.

            ### Parameters:
            1. pattern: Optional[str]
                - A paperdoll pattern, a concrete image path, or `image[step]`
                    from an `Image_Series` (None clears / skips).
            2. blur: Union[bool, float]
                - Background blur; True maps to 10.0, False to 0.0.
            3. blur_duration: float
                - Duration of the blur transition.
            4. bw: bool
                - True to render the background in black-and-white.
            5. alt_keys: List[str]
                - Alternative keys for pattern refinement.
            6. **kwargs
                - Values passed to pattern refinement.
            """
            self.background_image = self._resolve_background_path(pattern, alt_keys, **kwargs)
            self.background_bw = bw
            self._apply_background_blur(blur)
            renpy.call("display_background_image", blur_duration)

        def set_background_split(self, pattern_left = None, pattern_right = None, blur: Union[bool, float] = False, blur_duration: float = 0.0, separator_width: int = 8, bw_left: bool = False, bw_right: bool = False, alt_keys: List[str] = [], **kwargs):
            """
            Sets a split background: left half of the first image, right half of
            the second image, with a white separator strip in the middle.

            ### Parameters:
            1. pattern_left: Optional[str]
                - Pattern, concrete path, or `image[step]` for the left half.
            2. pattern_right: Optional[str]
                - Pattern, concrete path, or `image[step]` for the right half.
            3. blur: Union[bool, float]
                - Background blur; True maps to 10.0, False to 0.0.
            4. blur_duration: float
                - Duration of the blur transition.
            5. separator_width: int
                - Width of the white center strip in pixels.
            6. bw_left: bool
                - True to render the left half in black-and-white.
            7. bw_right: bool
                - True to render the right half in black-and-white.
            8. alt_keys: List[str]
                - Alternative keys applied to both patterns.
            9. **kwargs
                - Values passed to image refinement for both patterns.
            """
            path_left = self._resolve_background_path(pattern_left, alt_keys, **kwargs)
            path_right = self._resolve_background_path(pattern_right, alt_keys, **kwargs)

            if path_left != "" and path_right != "":
                self.background_image = build_split_background(
                    path_left,
                    path_right,
                    separator_width,
                    bw_left=bw_left,
                    bw_right=bw_right,
                )
                self.background_bw = False
            elif path_left != "":
                self.background_image = path_left
                self.background_bw = bw_left
            elif path_right != "":
                self.background_image = path_right
                self.background_bw = bw_right
            else:
                self.background_image = ""
                self.background_bw = False

            self._apply_background_blur(blur)
            renpy.call("display_background_image", blur_duration)

        def hide_background(self):
            renpy.hide("background")

        def clear(self):
            for paperdoll_obj in self.paperdoll_objs.values():
                paperdoll_obj.hide_all_images(recurse=False)
            self.hide_background()

    ##################
    # region Actions #

    def paperdoll_is_delta_string(value) -> bool:
        """
        Returns True when `value` is a string delta like `"+0.5"` or `"-0.1"`.

        The string must start with `+` or `-` and parse as a float. Plain
        `"0.5"` is not a delta (absolute).

        ### Parameters:
        1. value
            - Candidate action argument.

        ### Returns:
        1. bool
            - True when the value is a signed delta string.
        """
        if not isinstance(value, str):
            return False
        s = value.strip()
        if len(s) < 2 or s[0] not in "+-":
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    def paperdoll_resolve_number(value, current: float, keep_below: float = None) -> float:
        """
        Resolves an action number: absolute, keep-sentinel, or `"+"`/`"-"` delta.

        ### Parameters:
        1. value
            - Float/int, numeric string, delta string (`"+0.5"` / `"-0.1"`), or
                a keep-sentinel below `keep_below`.
        2. current: float
            - Existing value the delta is added to (and the keep-sentinel returns).
        3. keep_below: Optional[float]
            - When set, numeric `value < keep_below` means "keep `current`"
                (e.g. Move sentinels at `-100`).

        ### Returns:
        1. float
            - The resolved absolute number.
        """
        if isinstance(value, str):
            s = value.strip()
            if paperdoll_is_delta_string(s):
                return float(current) + float(s)
            return float(s)
        if keep_below is not None and value < keep_below:
            return float(current)
        return float(value)

    def paperdoll_apply_number_arg(incoming, existing):
        """
        Stores an override onto an action field (preset `**overrides`).

        Delta strings are applied immediately against `existing`. Absolute values
        replace it. Deferred deltas against paperdoll config stay as strings on
        construction / when not overwritten this way — callers that pass a delta
        at init leave it for `paperdoll_resolve_number` at get-time.

        ### Parameters:
        1. incoming
            - New argument from `overwrite_values`.
        2. existing
            - Current field value on the action.

        ### Returns:
        1. Any
            - Value to store on the action (usually a float).
        """
        if paperdoll_is_delta_string(incoming):
            if isinstance(existing, str):
                base = paperdoll_resolve_number(existing, 0.0)
            else:
                base = float(existing)
            return base + float(incoming.strip())
        if isinstance(incoming, str):
            return float(incoming.strip())
        return incoming

    class PDAction(ABC):
        def __init__(self, key: str):
            self.key = key

    class PDAPreset(PDAction):
        def __init__(self, preset: str, **kwargs):
            super().__init__("preset")
            self.preset = preset
            self.values = kwargs

        def get_actions(self, paperdoll_obj=None) -> List[PDAction]:
            """
            Expands this preset for the displaying object (scoped lookup + copy).

            ### Parameters:
            1. paperdoll_obj: Optional[Paperdoll_Obj]
                - Display target; used to prefer `"{key}:{preset}"` entries.

            ### Returns:
            1. List[PDAction]
                - Fresh action list with overrides applied.
            """
            return list(get_preset_with_overrides(self.preset, paperdoll_obj, **self.values))


    class PDAImage(PDAction):
        def __init__(self, **kwargs):
            super().__init__("image")
            self.values = kwargs

        def overwrite_values(self, **kwargs):
            self.values = update_dict(self.values, kwargs)

    class PDAMove(PDAction):
        def __init__(self, alignX = -100.0, alignY = -100.0, zoom = -100.0, duration = 0.0):
            """
            Repositions / scales a paperdoll.

            Numeric args may be floats, or delta strings (`alignX="+0.5"`) added to
            the current local/world value at apply time. Omitted args use a
            keep-sentinel (`< -10`).

            ### Parameters:
            1. alignX
                - Absolute xalign, delta string, or keep-sentinel.
            2. alignY
                - Absolute ypos, delta string, or keep-sentinel.
            3. zoom
                - Absolute zoom, delta string, or keep-sentinel.
            4. duration
                - Ease duration (absolute or delta string vs `0.0` / prior override).
            """
            super().__init__("move")
            self.alignX = alignX
            self.alignY = alignY
            self.zoom = zoom
            self.duration = duration

        def overwrite_values(self, **kwargs):
            if "alignX" in kwargs:
                if paperdoll_is_delta_string(kwargs["alignX"]):
                    self.alignX = kwargs["alignX"]
                else:
                    self.alignX = paperdoll_apply_number_arg(kwargs["alignX"], self.alignX)
            if "alignY" in kwargs:
                if paperdoll_is_delta_string(kwargs["alignY"]):
                    self.alignY = kwargs["alignY"]
                else:
                    self.alignY = paperdoll_apply_number_arg(kwargs["alignY"], self.alignY)
            if "zoom" in kwargs:
                if paperdoll_is_delta_string(kwargs["zoom"]):
                    self.zoom = kwargs["zoom"]
                else:
                    self.zoom = paperdoll_apply_number_arg(kwargs["zoom"], self.zoom)
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)

        def _space(self, pd_obj: Paperdoll_Obj) -> Dict[str, Any]:
            """Returns local transform when parented, else world config."""
            if pd_obj.parent is not None:
                return pd_obj.local
            return pd_obj.config

        def get_x(self, pd_obj: Paperdoll_Obj) -> float:
            return paperdoll_resolve_number(self.alignX, self._space(pd_obj)["alignX"], keep_below=-10.0)

        def get_y(self, pd_obj: Paperdoll_Obj) -> float:
            return paperdoll_resolve_number(self.alignY, self._space(pd_obj)["alignY"], keep_below=-10.0)

        def get_zoom(self, pd_obj: Paperdoll_Obj) -> float:
            return paperdoll_resolve_number(self.zoom, self._space(pd_obj)["zoom"], keep_below=-10.0)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

        def get_values(self, pd_obj: Paperdoll_Obj) -> Tuple[float, float, float, float]:
            return self.get_x(pd_obj), self.get_y(pd_obj), self.get_zoom(pd_obj), self.get_duration()

    class PDABlur(PDAction):
        def __init__(self, blur, duration = 0.0):
            super().__init__("blur")
            self.blur = blur
            self.duration = duration

        def overwrite_values(self, **kwargs):
            if "blur" in kwargs:
                if paperdoll_is_delta_string(kwargs["blur"]):
                    self.blur = kwargs["blur"]
                else:
                    self.blur = paperdoll_apply_number_arg(kwargs["blur"], self.blur)
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)

        def get_blur(self, pd_obj: Paperdoll_Obj) -> float:
            return paperdoll_resolve_number(self.blur, pd_obj.config["blur"], keep_below=-100.0)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

        def get_values(self, pd_obj: Paperdoll_Obj) -> Tuple[float, float]:
            return self.get_blur(pd_obj), self.get_duration()

    class PDAPause(PDAction):
        def __init__(self, duration = 0.0, transition: bool = True):
            super().__init__("pause")
            self.duration = duration
            self.transition = transition

        def overwrite_values(self, **kwargs):
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)
            self.transition = kwargs.get("transition", self.transition)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

    class PDAShake(PDAction):
        def __init__(self, duration = 1.0, max_distance = 15):
            super().__init__("shake")
            self.duration = duration
            self.max_distance = max_distance

        def overwrite_values(self, **kwargs):
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)
            if "max_distance" in kwargs:
                self.max_distance = paperdoll_apply_number_arg(kwargs["max_distance"], self.max_distance)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

        def get_max_distance(self) -> float:
            return paperdoll_resolve_number(self.max_distance, 15.0)

    class PDAFlip(PDAction):
        def __init__(self, flip: bool = False, duration = 0.0):
            """
            Mirrors a paperdoll horizontally (`xzoom`).

            ### Parameters:
            1. flip: bool
                - True faces the other way (`xzoom = -1`), False is unflipped (`xzoom = 1`).
            2. duration
                - Ease duration for the flip. `0.0` snaps immediately.
                    Accepts delta strings vs `0.0` / prior override.
            """
            super().__init__("flip")
            self.flip = -1.0 if flip else 1.0
            self.duration = duration

        def overwrite_values(self, **kwargs):
            if "flip" in kwargs:
                flip = kwargs["flip"]
                if isinstance(flip, bool):
                    self.flip = -1.0 if flip else 1.0
                else:
                    self.flip = float(flip)
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

    class PDABw(PDAction):
        def __init__(self, bw: bool = True, duration = 0.0):
            """
            Toggles black-and-white display for a paperdoll.

            ### Parameters:
            1. bw: bool
                - True for grayscale, False for full color.
            2. duration
                - Transition duration for the saturation change.
                    Accepts delta strings vs `0.0` / prior override.
            """
            super().__init__("bw")
            self.bw = bw
            self.duration = duration

        def overwrite_values(self, **kwargs):
            self.bw = kwargs.get("bw", self.bw)
            if "duration" in kwargs:
                self.duration = paperdoll_apply_number_arg(kwargs["duration"], self.duration)

        def get_duration(self) -> float:
            return paperdoll_resolve_number(self.duration, 0.0)

        def get_values(self) -> Tuple[bool, float]:
            return self.bw, self.get_duration()

    class PaperdollOverride:
        def __init__(self, index: int, conditions: Dict[str, Any], x_override = 0.0, y_override = 0.0, rot_override = 0.0, blur_override = 0.0, zoom_override = 0.0):
            self.conditions = conditions
            self.index = index
            self.x_override = x_override
            self.y_override = y_override
            self.rot_override = rot_override
            self.blur_override = blur_override
            self.zoom_override = zoom_override

        def get_override(self, **kwargs) -> List[float]:
            for key, value in self.conditions.items():
                cond_value = get_kwargs(key, None, **kwargs)
                if value != cond_value and not check_in_value(value, cond_value):
                    return 0.0, 0.0, 0.0, 0.0, 0.0        
            return self.x_override, self.y_override, self.rot_override, self.blur_override, self.zoom_override

    class PaperdollPreset:
        """
        A named action list stored on a Person or passed to `register_obj(presets=...)`.

        On registration it becomes a temporary preset `"object_key:key"`. Bare keys
        must not contain `:` (`:` is reserved for cross-object lookup).

        ### Parameters:
        1. key: str
            - Preset name without colons.
        2. *actions: PDAction
            - Actions expanded by `PDAPreset(key)`.
        """

        def __init__(self, key: str, *actions):
            self.key = key
            self.actions = list(actions)

    # endregion
    ##################

transform t_paperdoll_blur(blur_val, duration = 0.0):
    ease duration blur blur_val
transform t_paperdoll_position(xAlign, yAlign, zoom_val):
    transform_anchor True
    xalign xAlign
    ypos yAlign
    zoom zoom_val
transform t_paperdoll_move(duration, startX, startY, startZ, endX, endY, endZ):
    transform_anchor True
    xalign startX
    ypos startY
    zoom startZ
    ease duration xalign endX ypos endY zoom endZ
transform t_paperdoll_flip(duration, start_xzoom, end_xzoom):
    xalign 0.5
    yalign 0.0
    xzoom start_xzoom
    ease duration xzoom end_xzoom
transform t_paperdoll_bw(saturation, duration = 0.0):
    ease duration matrixcolor SaturationMatrix(saturation)

label display_background_image(duration):
    if paperdoll_manager.background_image != "":
        $ bg_displayable = paperdoll_manager.background_image
        if isinstance(bg_displayable, str):
            $ bg_displayable = Image(bg_displayable)
        $ bg_displayable = apply_paperdoll_bw(bg_displayable, paperdoll_manager.background_bw)
        $ renpy.show(
            "background",
            what = At(
                bg_displayable,
                t_paperdoll_blur(paperdoll_manager.background_blur, duration)
            ),
            tag = "background",
            zorder = PAPERDOLL_BG_ZORDER,
        )
    return

label display_paperdoll_image(paperdoll_obj, actions):
    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        if paperdoll_obj.image[index] == "":
            $ paperdoll_obj.update_overrides(index)
            $ paperdoll_obj.resolve_image(index)
            $ renpy.show(
                paperdoll_obj.key + str(index),
                tag = paperdoll_obj.key + str(index),
                what = paperdoll_layer_for_show(paperdoll_obj, index),
                at_list = [
                    t_paperdoll_position(
                        paperdoll_obj.get_config("alignX", index),
                        paperdoll_obj.get_config("alignY", index),
                        paperdoll_obj.get_effective_zoom(index)
                    ),
                    t_paperdoll_blur(paperdoll_obj.get_value("blur")),
                    t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
                ],
                zorder = paperdoll_layer_zorder(paperdoll_obj),
            )

        $ index += 1

    call run_paperdoll_actions(paperdoll_obj, actions) from _call_run_paperdoll_actions

    return

label run_paperdoll_actions(paperdoll_obj, actions):
    while (len(actions) > 0):
        $ action = actions.pop(0)

        if action.key == "preset":
            call run_paperdoll_actions(paperdoll_obj, action.get_actions(paperdoll_obj)) from _call_run_paperdoll_actions_recursive
        else:
            $ action_label = "paperdoll_action_" + action.key

            if renpy.has_label(action_label):
                $ renpy.call(action_label, paperdoll_obj, action)

    return

###########################
# region Dialogue Actions #
###########################

label paperdoll_action_blur(paperdoll_obj, pda_blur):
    $ blur, duration = pda_blur.get_values(paperdoll_obj)

    python:
        for index in range(len(paperdoll_obj.pattern)):
            paperdoll_obj.update_overrides(index)
            paperdoll_obj.resolve_image(index)

        def _blur_at_list(index):
            return [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(blur, duration),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ]
        paperdoll_show_layers(paperdoll_obj, _blur_at_list, skip_empty=False)

    $ paperdoll_obj.config["blur"] = blur

    return

label paperdoll_action_image(paperdoll_obj, pda_image):
    $ paperdoll_obj.set_values(update_dict(paperdoll_obj.values, pda_image.values))

    python:
        for index in range(len(paperdoll_obj.pattern)):
            paperdoll_obj.update_overrides(index)
            paperdoll_obj.resolve_image(index)

        def _image_at_list(index):
            return [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(paperdoll_obj.get_value("blur")),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ]
        paperdoll_show_layers(paperdoll_obj, _image_at_list, skip_empty=False)

    return

label paperdoll_action_move(paperdoll_obj, pda_move):
    $ alignX, alignY, zoom, duration = pda_move.get_values(paperdoll_obj)

    if preferences.transitions != 0 and persistent.transitionSpeed > 0:
        $ duration = duration / persistent.transitionSpeed

    python:
        start_worlds = {paperdoll_obj.key: paperdoll_capture_world(paperdoll_obj)}
        for _desc in paperdoll_iter_descendants(paperdoll_obj):
            start_worlds[_desc.key] = paperdoll_capture_world(_desc)

        if paperdoll_obj.parent is not None:
            paperdoll_obj.local["alignX"] = alignX
            paperdoll_obj.local["alignY"] = alignY
            paperdoll_obj.local["zoom"] = zoom
            end_world = paperdoll_world_config(paperdoll_obj)
        else:
            end_world = {
                "alignX": alignX,
                "alignY": alignY,
                "zoom": zoom,
                "rotation": paperdoll_obj.config.get("rotation", 0.0),
                "flip": paperdoll_obj.get_flip(),
            }

        paperdoll_apply_subtree_transform(paperdoll_obj, end_world, duration, start_worlds)

    return

label paperdoll_action_flip(paperdoll_obj, pda_flip):
    $ duration = pda_flip.get_duration()

    if preferences.transitions != 0 and persistent.transitionSpeed > 0:
        $ duration = duration / persistent.transitionSpeed

    python:
        start_worlds = {paperdoll_obj.key: paperdoll_capture_world(paperdoll_obj)}
        for _desc in paperdoll_iter_descendants(paperdoll_obj):
            start_worlds[_desc.key] = paperdoll_capture_world(_desc)

        if paperdoll_obj.parent is not None:
            paperdoll_obj.local["flip"] = pda_flip.flip
            end_world = paperdoll_world_config(paperdoll_obj)
        else:
            end_world = paperdoll_capture_world(paperdoll_obj)
            end_world["flip"] = pda_flip.flip

        paperdoll_apply_subtree_transform(paperdoll_obj, end_world, duration, start_worlds)

    return

label paperdoll_action_bw(paperdoll_obj, pda_bw):
    $ bw, duration = pda_bw.get_values()

    if preferences.transitions != 0 and persistent.transitionSpeed > 0 and duration > 0:
        $ duration = duration / persistent.transitionSpeed

    $ paperdoll_obj.config["bw"] = bw

    python:
        def _bw_at_list(index):
            return [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(paperdoll_obj.config.get("blur", 0.0)),
                t_paperdoll_bw(paperdoll_saturation(bw), duration),
            ]
        paperdoll_show_layers(paperdoll_obj, _bw_at_list)

    return

label paperdoll_action_pause(paperdoll_obj, pda_pause):
    $ duration, transition = pda_pause.get_duration(), pda_pause.transition

    if preferences.transitions != 0 and persistent.transitionSpeed > 0 and transition:
        $ duration = duration / persistent.transitionSpeed
    $ renpy.pause(duration)

    return

label paperdoll_action_shake(paperdoll_obj, pda_shake):
    $ duration, max_distance = pda_shake.get_duration(), pda_shake.get_max_distance()

    python:
        _shake_targets = [paperdoll_obj] + list(paperdoll_iter_descendants(paperdoll_obj))
        for _shake_obj in _shake_targets:
            if not paperdoll_is_visible(_shake_obj):
                continue

            def _make_shake_at_list(_obj):
                def _at_list(index):
                    return [
                        t_paperdoll_position(
                            _obj.get_config("alignX", index),
                            _obj.get_config("alignY", index),
                            _obj.get_effective_zoom(index)
                        ),
                        Shake(
                            (_obj.get_config("alignX", index), _obj.get_config("alignY", index), _obj.get_config("alignX", index), _obj.get_config("alignY", index)),
                            duration,
                            dist=max_distance,
                            seed=_obj.key,
                        ),
                        t_paperdoll_bw(paperdoll_saturation(_obj.is_bw())),
                    ]
                return _at_list

            paperdoll_show_layers(_shake_obj, _make_shake_at_list(_shake_obj))

    return

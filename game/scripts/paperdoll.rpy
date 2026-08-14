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

    def get_preset(key: str) -> List[PDAction]:
        global paperdoll_presets
        return paperdoll_presets[key]
    def get_preset_with_overrides(key: str, **kwargs) -> List[PDAction]:
        global paperdoll_presets
        paperdoll_preset = paperdoll_presets[key]
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
    register_preset("close_body_right", PDAPreset("close_body"), PDAMove(alignX = 1.5))
    register_preset("close_body_left", PDAPreset("close_body"), PDAMove(alignX = -0.1))
    register_preset("upper_body", PDAMove(alignY = -0.1, zoom = 3.0))
    register_preset("upper_body_center", PDAPreset("upper_body"), PDAMove(alignX = 0.5))
    register_preset("upper_body_right", PDAPreset("upper_body"), PDAMove(alignX = 6.0))
    register_preset("upper_body_left", PDAPreset("upper_body"), PDAMove(alignX = -1.5))

    # endregion
    ##################


init -99 python:
    from abc import ABC, abstractmethod

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

        ### Methods:
        7. set_values(data: Dict[str, Any])
            - Sets the values of the paperdoll object
        8. hide_image_at(index: int)
            - Hides the image of the paperdoll object at the given index
        9. hide_all_images()
            - Hides all the images of the paperdoll object
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

        def hide_all_images(self):
            """
            Hides all the images of the paperdoll object
            """
            for i in range(len(self.pattern)):
                self.hide_image_at(i)

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
            Returns the zoom value adjusted for the layer's base scale factor.

            ### Parameters:
            1. index: int
                - The layer index to query.
            2. zoom: float
                - Optional zoom override; defaults to the layer config zoom.

            ### Returns:
            1. float
                - The effective zoom to pass to display transforms.
            """
            if zoom is None:
                zoom = self.get_config("zoom", index)
            return zoom * self.scale_factors[index]

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
            self.paperdoll_objs[key] = (Paperdoll_Obj(key, *pattern, **kwargs))

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
                paperdoll_obj.hide_all_images()
            self.hide_background()

    ##################
    # region Actions #

    class PDAction(ABC):
        def __init__(self, key: str):
            self.key = key

    class PDAPreset(PDAction):
        def __init__(self, preset: str, **kwargs):
            super().__init__("preset")
            self.preset = preset
            self.values = kwargs

        def get_actions(self) -> List[PDAction]:
            return [action for action in get_preset_with_overrides(self.preset, **self.values)]


    class PDAImage(PDAction):
        def __init__(self, **kwargs):
            super().__init__("image")
            self.values = kwargs

        def overwrite_values(self, **kwargs):
            self.values = update_dict(self.values, kwargs)

    class PDAMove(PDAction):
        def __init__(self, alignX: float = -100.0, alignY: float = -100.0, zoom: float = -100.0, duration: float = 0.0):
            super().__init__("move")
            self.alignX = alignX
            self.alignY = alignY
            self.zoom = zoom
            self.duration = duration

        def overwrite_values(self, **kwargs):
            self.alignX = kwargs.get("alignX", self.alignX)
            self.alignY = kwargs.get("alignY", self.alignY)
            self.zoom = kwargs.get("zoom", self.zoom)
            self.duration = kwargs.get("duration", self.duration)

        def get_x(self, pd_obj: Paperdoll_Obj) -> float:
            if self.alignX < -10.0:
                return pd_obj.config["alignX"]
            return self.alignX
        def get_y(self, pd_obj: Paperdoll_Obj) -> float:
            if self.alignY < -10.0:
                return pd_obj.config["alignY"]
            return self.alignY
        def get_zoom(self, pd_obj: Paperdoll_Obj) -> float:
            if self.zoom < -10.0:
                return pd_obj.config["zoom"]
            return self.zoom
        def get_duration(self) -> float:
            return self.duration
        def get_values(self, pd_obj: Paperdoll_Obj) -> Tuple[float, float, float, float]:
            return self.get_x(pd_obj), self.get_y(pd_obj), self.get_zoom(pd_obj), self.get_duration()

    class PDABlur(PDAction):
        def __init__(self, blur: float, duration: float = 0.0):
            super().__init__("blur")
            self.blur = blur
            self.duration = duration

        def overwrite_values(self, **kwargs):
            self.blur = kwargs.get("blur", self.blur)
            self.duration = kwargs.get("duration", self.duration)

        def get_blur(self, pd_obj: Paperdoll_Obj) -> float:
            if self.blur < -100.0:
                return pd_obj.config["blur"]
            return self.blur
        def get_duration(self) -> float:
            return self.duration
        def get_values(self, pd_obj: Paperdoll_Obj) -> Tuple[float, float]:
            return self.get_blur(pd_obj), self.get_duration()

    class PDAPause(PDAction):
        def __init__(self, duration: float = 0.0, transition: bool = True):
            super().__init__("pause")
            self.duration = duration
            self.transition = transition

        def overwrite_values(self, **kwargs):
            self.duration = kwargs.get("duration", self.duration)
            self.transition = kwargs.get("transition", self.transition)

    class PDAShake(PDAction):
        def __init__(self, duration: float = 1.0, max_distance: float = 15):
            super().__init__("shake")
            self.duration = duration
            self.max_distance = max_distance

        def overwrite_values(self, **kwargs):
            self.duration = kwargs.get("duration", self.duration)
            self.max_distance = kwargs.get("max_distance", self.max_distance)

    class PDAFlip(PDAction):
        def __init__(self, flip: bool = False):
            super().__init__("flip")
            self.flip = -1.0 if flip else 1.0

        def overwrite_values(self, **kwargs):
            self.flip = kwargs.get("flip", self.flip)

    class PDABw(PDAction):
        def __init__(self, bw: bool = True, duration: float = 0.0):
            """
            Toggles black-and-white display for a paperdoll.

            ### Parameters:
            1. bw: bool
                - True for grayscale, False for full color.
            2. duration: float
                - Transition duration for the saturation change.
            """
            super().__init__("bw")
            self.bw = bw
            self.duration = duration

        def overwrite_values(self, **kwargs):
            self.bw = kwargs.get("bw", self.bw)
            self.duration = kwargs.get("duration", self.duration)

        def get_values(self) -> Tuple[bool, float]:
            return self.bw, self.duration

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

    # endregion
    ##################

transform t_paperdoll_blur(blur_val, duration = 0.0):
    ease duration blur blur_val
transform t_paperdoll_position(xAlign, yAlign, zoom):
    xalign xAlign
    ypos yAlign
    zoom zoom
transform t_paperdoll_move(duration, xAlign, yAlign):
    ease duration xalign xAlign ypos yAlign
transform t_paperdoll_flip(flip):
    xzoom flip
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
            tag = "background"
        )
    return

label display_paperdoll_image(paperdoll_obj, actions):
    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ pattern = paperdoll_obj.pattern[index]

        if paperdoll_obj.image[index] == "":
            $ paperdoll_obj.update_overrides(index)

            $ paperdoll_obj.resolve_image(index)
            $ renpy.show(
                paperdoll_obj.key + str(index), 
                tag = paperdoll_obj.key + str(index),
                what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
                at_list = [
                    t_paperdoll_position(
                        paperdoll_obj.get_config("alignX", index), 
                        paperdoll_obj.get_config("alignY", index),
                        paperdoll_obj.get_effective_zoom(index)
                    ),
                    t_paperdoll_blur(paperdoll_obj.get_value("blur")),
                    t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
                ],
            )

        $ index += 1
    
    call run_paperdoll_actions(paperdoll_obj, actions) from _call_run_paperdoll_actions

    return

label run_paperdoll_actions(paperdoll_obj, actions):
    while (len(actions) > 0):
        $ action = actions.pop(0)

        if action.key == "preset":
            call run_paperdoll_actions(paperdoll_obj, action.get_actions()) from _call_run_paperdoll_actions_recursive
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

    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ pattern = paperdoll_obj.pattern[index]
        $ paperdoll_obj.update_overrides(index)

        $ paperdoll_obj.resolve_image(index)

        $ renpy.show(
            paperdoll_obj.key + str(index), 
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index), 
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(blur, duration),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ],
        )

        $ index += 1

    $ paperdoll_obj.config["blur"] = blur

    return

label paperdoll_action_image(paperdoll_obj, pda_image):
    $ paperdoll_obj.set_values(update_dict(paperdoll_obj.values, pda_image.values))

    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ pattern = paperdoll_obj.pattern[index]
        $ paperdoll_obj.update_overrides(index)

        $ paperdoll_obj.resolve_image(index)

        $ renpy.show(
            paperdoll_obj.key + str(index), 
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index), 
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(paperdoll_obj.get_value("blur")),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ],
        )

        $ index += 1

    return

label paperdoll_action_move(paperdoll_obj, pda_move):
    $ alignX, alignY, zoom, duration = pda_move.get_values(paperdoll_obj)

    if preferences.transitions != 0 and persistent.transitionSpeed > 0:
        $ duration = duration / persistent.transitionSpeed

    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ renpy.show(
            paperdoll_obj.key + str(index), 
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index), 
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_move(
                    duration, 
                    alignX + paperdoll_obj.get_override_config("alignX", index), 
                    alignY + paperdoll_obj.get_override_config("alignY", index)
                ),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ],
        )

        $ index += 1

    $ paperdoll_obj.config["alignX"] = alignX
    $ paperdoll_obj.config["alignY"] = alignY
    $ paperdoll_obj.config["zoom"] = zoom

    return

label paperdoll_action_flip(paperdoll_obj, pda_flip):
    $ flip = pda_flip.flip
    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ renpy.show(
            paperdoll_obj.key + str(index), 
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_flip(flip),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ],
        )

        $ index += 1

    return

label paperdoll_action_bw(paperdoll_obj, pda_bw):
    $ bw, duration = pda_bw.get_values()

    if preferences.transitions != 0 and persistent.transitionSpeed > 0 and duration > 0:
        $ duration = duration / persistent.transitionSpeed

    $ paperdoll_obj.config["bw"] = bw

    $ index = 0
    while (index < len(paperdoll_obj.pattern)):
        $ renpy.show(
            paperdoll_obj.key + str(index),
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]),
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                t_paperdoll_blur(paperdoll_obj.config.get("blur", 0.0)),
                t_paperdoll_bw(paperdoll_saturation(bw), duration),
            ],
        )

        $ index += 1

    return

label paperdoll_action_pause(paperdoll_obj, pda_pause):
    $ duration, transition = pda_pause.duration, pda_pause.transition

    if preferences.transitions != 0 and persistent.transitionSpeed > 0 and transition:
        $ duration = duration / persistent.transitionSpeed
    $ renpy.pause(duration)

    return

label paperdoll_action_shake(paperdoll_obj, pda_shake):
    $ duration, max_distance = pda_shake.duration, pda_shake.max_distance

    $ index = 0

    while (index < len(paperdoll_obj.pattern)):
        # Use dedicated seed here, to give all images in the paperdoll_obj the same shake.
        $ renpy.show(
            paperdoll_obj.key + str(index), 
            tag = paperdoll_obj.key + str(index),
            what = paperdoll_layer_displayable(paperdoll_obj.image[index]), 
            at_list = [
                t_paperdoll_position(
                    paperdoll_obj.get_config("alignX", index),
                    paperdoll_obj.get_config("alignY", index),
                    paperdoll_obj.get_effective_zoom(index)
                ),
                Shake(
                    (paperdoll_obj.get_config("alignX", index), paperdoll_obj.get_config("alignY", index), paperdoll_obj.get_config("alignX", index), paperdoll_obj.get_config("alignY", index)), 
                    duration, 
                    dist = max_distance, 
                    seed = paperdoll_obj.key
                ),
                t_paperdoll_bw(paperdoll_saturation(paperdoll_obj.is_bw())),
            ],
        )

        $ index += 1

    return

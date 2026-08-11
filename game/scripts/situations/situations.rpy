init python:
    
    situation_manager = None

init -99 python:
    from abc import ABC, abstractmethod

    TEASER_NOTE_TYPES = {
        "observation": ("Observation", "#2563eb"),
        "suspicion": ("Suspicion", "#7c3aed"),
        "insight": ("Insight", "#15803d"),
        "setback": ("Setback", "#b91c1c"),
    }
    TEASER_TEXT_LAYOUTS = ("text_full", "text_aside")
    TEASER_PHOTO_LAYOUTS = ("photo_left", "photo_right", "photo_top")
    TEASER_PHOTO_W = 160
    TEASER_PHOTO_H = 120

    #########################
    # region Helper Methods #

    def parse_situation_stat_key(key: str):
        """
        Parse a situation progress key of the form ``situation:<situation_key>:<bar_key>``.

        ``situation_key`` may itself contain colons (e.g. unlockable ``rule:level:3``).
        The last ``:``-separated segment is always the bar key.

        Args:
            key (str): Full key, optionally without the ``situation:`` prefix
                (``situation_key:bar_key``).

        Returns:
            tuple | None: ``(situation_key, bar_key)``, or ``None`` if the key
            cannot be parsed.
        """
        if key is None or key == "":
            return None

        if key.startswith("situation:"):
            rest = key[len("situation:"):]
            if rest == "":
                return None
            if ":" not in rest:
                return (rest, "main")
            situation_key, bar_key = rest.rsplit(":", 1)
            if situation_key == "" or bar_key == "":
                return None
            return (situation_key, bar_key)

        parts = key.split(":")
        if len(parts) == 2:
            return (parts[0], parts[1])
        return None

    def compute_polaroid_metrics(photo_w=160, photo_h=120, rotation=0.0, xoff=0, yoff=0):
        """
        Layout metrics for a tilted polaroid cell.

        Cell size grows with |rotation| so rotated corners, shadow, and micro-offsets
        stay inside the reserved box (text column / row height can follow).

        Returns:
            dict: frame_w/h, cell_w/h, place_x/y, photo_w/h, rotation.
        """
        import math

        frame_w = photo_w + 16
        frame_h = photo_h + 36
        shadow_w = 2
        shadow_h = 3
        # Tape sits on the top edge; keep a little slack above the frame.
        tape_slack = 6

        rad = math.radians(abs(float(rotation or 0.0)))
        bb_w = frame_w * math.cos(rad) + frame_h * math.sin(rad)
        bb_h = frame_w * math.sin(rad) + frame_h * math.cos(rad)

        cell_w = int(math.ceil(bb_w + shadow_w + 2 * abs(int(xoff or 0)) + 2))
        cell_h = int(math.ceil(bb_h + shadow_h + tape_slack + 2 * abs(int(yoff or 0)) + 2))
        place_x = (cell_w - frame_w) // 2 + int(xoff or 0)
        place_y = (cell_h - frame_h) // 2 + int(yoff or 0)

        return {
            "photo_w": photo_w,
            "photo_h": photo_h,
            "frame_w": frame_w,
            "frame_h": frame_h,
            "cell_w": cell_w,
            "cell_h": cell_h,
            "place_x": place_x,
            "place_y": place_y,
            "rotation": float(rotation or 0.0),
        }
    
    def get_bar_value_mood(area: int, min: int = None, max: int = None) -> str:
        """
        Short English mood keyword for a bar area.

        On two-sided bars (``min < 0 < max``), area ``0`` is ``neutral``.
        On one-sided bars (range does not cross zero), area ``0`` is the end
        nearest zero — the floor of the available range, not a midpoint — so
        it maps to ``minimal`` instead of ``neutral``.
        """
        one_sided = min is not None and max is not None and (max < 0 or min > 0)
        moods = {
            -3: "hostile",
            -2: "tense",
            -1: "uneasy",
            0: "minimal" if one_sided else "neutral",
            1: "open",
            2: "relaxed",
            3: "enthusiastic",
        }
        return moods.get(area, "neutral")

    def get_bar_value_area(min: int, max: int, value: int) -> int:
        """
        Map a bar value to area ``-3 … 0 … 3``.

        Each side of zero is split into **7** equal parts:
        - the seventh nearest to 0 → area ``0``
        - the remaining six sevenths form three pairs → ``±1``, ``±2``, ``±3``
            (closer pair = smaller magnitude)

        Entirely positive or entirely negative bars use the same 7-way split
        over ``[min, max]``, with the end nearer to zero treated as area ``0``.
        """
        if min > max:
            return 0

        def map_seventh(index: int, negative: bool) -> int:
            # index 0 = nearest zero → 0; 1–2 → ±1; 3–4 → ±2; 5–6 → ±3
            if index <= 0:
                return 0
            level = (index + 1) // 2
            if level > 3:
                level = 3
            return -level if negative else level

        def seventh_index(lo: float, hi: float, v: float, from_near_zero: bool) -> int:
            """Return 0..6; index 0 is the end nearer to zero."""
            span = hi - lo
            if span <= 0:
                return 0
            if v < lo:
                v = lo
            elif v > hi:
                v = hi
            t = (v - lo) / float(span)
            raw = t if from_near_zero else (1.0 - t)
            idx = int(raw * 7)
            if idx >= 7:
                idx = 6
            elif idx < 0:
                idx = 0
            return idx

        # Entirely negative: near-zero end is max
        if max < 0:
            return map_seventh(
                seventh_index(min, max, value, from_near_zero=False),
                negative=True,
            )

        # Entirely positive: near-zero end is min
        if min > 0:
            return map_seventh(
                seventh_index(min, max, value, from_near_zero=True),
                negative=False,
            )

        if value == 0:
            return 0

        if value > 0:
            return map_seventh(
                seventh_index(0, max, value, from_near_zero=True),
                negative=False,
            )

        return map_seventh(
            seventh_index(min, 0, value, from_near_zero=False),
            negative=True,
        )

    #endregion
    #########################

    ##########################
    # region SituationTeaser #

    class SituationTeaser:
        """
        Chronicle note / pre-activation teaser for a situation.

        Definition fields (hot-reloadable): teaser text, conditions, optional
        interpretation, note_type, image pattern, layout. Runtime fields freeze on
        activate (timestamp, layout_id, resolved image, interpolated texts).
        """

        def __init__(
            self,
            key: str,
            teaser: str,
            *conditions: Condition,
            interpretation: str = None,
            note_type: str = None,
            image: str = None,
            layout: str = None,
        ):
            self.key = key
            self.teaser = teaser
            self.conditions = ConditionStorage(*conditions)
            self.interpretation = interpretation
            self.note_type = note_type
            # Redirect the path into the current mod's folder (base = "" prefix).
            self.image = get_mod_path(active_mod_key) + image if image else image
            # Optional forced journal layout id; None → random on activate.
            self.layout = layout

            self.active = False
            self.values = {}
            self.text = self.teaser
            self.interpretation_text = None
            self.activation_order = -1
            self.activated_time = None
            self.image_path = None
            self.layout_id = None
            self.layout_rotation = 0.0
            self.layout_offset_x = 0
            self.layout_offset_y = 0

            self.situation = None
        
        def update_data(self, teaser: SituationTeaser):
            self.key = teaser.key
            self.teaser = teaser.teaser
            self.conditions = teaser.conditions
            self.interpretation = teaser.interpretation
            self.note_type = teaser.note_type
            self.image = teaser.image
            self.layout = teaser.layout
            if not hasattr(self, 'activation_order'):
                self.activation_order = -1
            if not hasattr(self, 'interpretation'):
                self.interpretation = None
            if not hasattr(self, 'note_type'):
                self.note_type = None
            if not hasattr(self, 'image'):
                self.image = None
            if not hasattr(self, 'layout'):
                self.layout = None
            if not hasattr(self, 'activated_time'):
                self.activated_time = None
            if not hasattr(self, 'image_path'):
                self.image_path = None
            if not hasattr(self, 'layout_id'):
                self.layout_id = None
            if not hasattr(self, 'layout_rotation'):
                self.layout_rotation = 0.0
            if not hasattr(self, 'layout_offset_x'):
                self.layout_offset_x = 0
            if not hasattr(self, 'layout_offset_y'):
                self.layout_offset_y = 0
            if not hasattr(self, 'interpretation_text'):
                self.interpretation_text = None
            if self.active:
                self.text = interpolate_string(self.teaser, **self.values)
                if self.interpretation:
                    self.interpretation_text = interpolate_string(self.interpretation, **self.values)
                # Migrate older saves that lack chronicle freeze fields
                if getattr(self, "layout_id", None) is None:
                    self._resolve_image()
                    self._pick_layout()
                if getattr(self, "interpretation_text", None) is None and self.interpretation:
                    self.interpretation_text = interpolate_string(self.interpretation, **self.values)
            return self

        def __str__(self):
            return "situation_teaser:" + self.situation.key + ":" + self.key

        def run_self_test(self):
            error_messages = []
            if len(self.conditions) == 0:
                error_messages.append((700, "No conditions provided."))
            if self.note_type is not None and self.note_type not in TEASER_NOTE_TYPES:
                error_messages.append((701, f"note_type '{self.note_type}' is invalid."))
            valid_layouts = TEASER_TEXT_LAYOUTS + TEASER_PHOTO_LAYOUTS
            if self.layout is not None and self.layout not in valid_layouts:
                error_messages.append((702, f"layout '{self.layout}' is invalid."))
            if self.layout in TEASER_PHOTO_LAYOUTS and not self.image:
                error_messages.append((703, f"layout '{self.layout}' requires an image."))
            return error_messages

        def check_conditions(self, **kwargs):
            return self.conditions.is_fulfilled(**kwargs)

        def has_photo(self) -> bool:
            return self.image_path is not None and self.image_path != ""

        def get_polaroid_metrics(self, photo_w: int = None, photo_h: int = None):
            """
            Rotation-aware polaroid cell metrics for journal layout.

            Args:
                photo_w: Inner photo width. Defaults to TEASER_PHOTO_W.
                photo_h: Inner photo height. Defaults to TEASER_PHOTO_H.

            Returns:
                dict: See compute_polaroid_metrics.
            """
            if photo_w is None:
                photo_w = TEASER_PHOTO_W
            if photo_h is None:
                photo_h = TEASER_PHOTO_H
            return compute_polaroid_metrics(
                photo_w,
                photo_h,
                rotation=getattr(self, "layout_rotation", 0.0),
                xoff=getattr(self, "layout_offset_x", 0),
                yoff=getattr(self, "layout_offset_y", 0),
            )

        def get_timestamp_text(self) -> str:
            """Frozen in-game timestamp label, or empty if not activated."""
            if self.activated_time is None:
                return ""
            day = self.activated_time.get_day()
            month = self.activated_time.get_month_name()
            daytime = self.activated_time.get_daytime_name()
            return f"Day {day} {month}, {daytime}"

        def get_note_type_display(self):
            """
            Returns:
                tuple: (label, color) or (None, None) when unset.
            """
            if self.note_type is None:
                return None, None
            return TEASER_NOTE_TYPES.get(self.note_type, (self.note_type, "#444444"))

        def _collect_interpolation_values(self, template: str, **kwargs):
            if not template:
                return
            for key in get_interpolation_keys(template):
                if key in kwargs:
                    self.values[key] = kwargs[key]

        def _resolve_image(self, **kwargs):
            self.image_path = None
            if not self.image:
                return
            merge = dict(kwargs)
            merge.update(self.values)
            nude, path = get_image(self.image, **merge)
            if path and renpy.loadable(path):
                self.image_path = path

        def _pick_layout(self):
            """
            Freeze layout_id + micro tilt/offset. Uses definition `layout` when set;
            otherwise picks randomly (anti-repeat) from the matching pool.
            """
            forced = getattr(self, "layout", None)
            if forced in TEASER_PHOTO_LAYOUTS and not self.has_photo():
                forced = None
            if forced in TEASER_TEXT_LAYOUTS + TEASER_PHOTO_LAYOUTS:
                self.layout_id = forced
            else:
                pool = list(TEASER_PHOTO_LAYOUTS if self.has_photo() else TEASER_TEXT_LAYOUTS)
                prev_layout = None
                if self.situation is not None:
                    previous = [
                        teaser for teaser in self.situation.teasers.values()
                        if teaser is not self and teaser.active and teaser.layout_id
                    ]
                    if previous:
                        previous.sort(key=lambda t: t.activation_order)
                        prev_layout = previous[-1].layout_id
                if prev_layout in pool and len(pool) > 1:
                    pool.remove(prev_layout)
                self.layout_id = pool[get_random_int(0, len(pool) - 1)]

            self.layout_rotation = round((renpy.random.random() * 8.0) - 4.0, 2)
            self.layout_offset_x = get_random_int(-6, 6)
            self.layout_offset_y = get_random_int(-4, 4)

        def activate(self, **kwargs):
            """
            Unlock this note once. Freezes timestamp, layout, and interpolated texts.
            Re-entry is a no-op (ink is dry).
            """
            if self.active:
                return self

            self.active = True
            if self.situation is not None:
                order = 0
                for teaser in self.situation.teasers.values():
                    if teaser is not self and teaser.active:
                        order += 1
                self.activation_order = order

            self.activated_time = Time("now")
            self._collect_interpolation_values(self.teaser, **kwargs)
            self._collect_interpolation_values(self.interpretation, **kwargs)
            self.text = interpolate_string(self.teaser, **self.values)
            if self.interpretation:
                self.interpretation_text = interpolate_string(self.interpretation, **self.values)
            else:
                self.interpretation_text = None

            self._resolve_image(**kwargs)
            self._pick_layout()
            return self

    #endregion
    ##########################

    #############################
    # region SituationThreshold #

    class SituationThreshold:
        def __init__(self, approach_hint: str, threshold_hint: str, *elements: Condition | Effect, direction: int = 1, visible_range: int = 100, thumbnail: str = None, default_hold: int = 5):
            self.bounds = {}
            self.approach_hint = approach_hint
            self.threshold_hint = threshold_hint
            self.direction = direction
            self.blocking = ConditionStorage()
            self.effects = []
            self.reached = False
            # Redirect the path into the current mod's folder (base = "" prefix).
            self.thumbnail = get_mod_path(active_mod_key) + thumbnail if thumbnail else thumbnail
            self.visible_range = visible_range
            self.situation = None
            self.timed_release = None
            self.default_hold = default_hold
            self.hold = -1

            for element in elements:
                if isinstance(element, Condition):
                    if isinstance(element, TimerCondition):
                        self.timed_release = element
                        continue
                    self.add_blocking(element)
                elif isinstance(element, Effect):
                    self.add_effect(element)

        @property
        def key(self):
            bounds = ",".join(f"{k}:{self.bounds[k]}" for k in sorted(self.bounds.keys()))
            if self.situation is None:
                return bounds
            return "situation:" + self.situation.key + ":" + bounds

        def update_data(self, threshold: SituationThreshold):
            self.bounds = dict(threshold.bounds)
            self.approach_hint = threshold.approach_hint
            self.threshold_hint = threshold.threshold_hint
            self.direction = threshold.direction
            self.blocking = threshold.blocking
            self.effects = threshold.effects
            self.visible_range = threshold.visible_range
            self.thumbnail = threshold.thumbnail
            self.default_hold = threshold.default_hold
            if not hasattr(self, 'hold'):
                self.hold = -1

            return self

        def run_self_test(self):
            error_messages = []
            if self.timed_release is not None and len(self.blocking) == 0:
                error_messages.append((710, "Timed release condition without blocking conditions"))

            for bar_keys in self.bounds.keys():
                if bar_keys not in self.situation.bars.keys():
                    error_messages.append((711, f"Bar {bar_keys} not found."))
                else:
                    if self.situation.bars[bar_keys].min > self.bounds[bar_keys]:
                        error_messages.append((712, f"Bar {bar_keys} min is less than bound {self.bounds[bar_keys]}."))
                    if self.situation.bars[bar_keys].max < self.bounds[bar_keys]:
                        error_messages.append((713, f"Bar {bar_keys} max is greater than bound {self.bounds[bar_keys]}."))

            if self.direction not in [1, -1]:
                error_messages.append((714, "Direction is 0. Has to be 1 or -1."))

            if self.default_hold < -1:
                error_messages.append((715, "Default hold is less than -1. Has to be -1 (no hysteresis) or 0 or greater."))

            if self.visible_range < 0:
                error_messages.append((716, "Visible range is less than 0. Has to be 0 or greater."))

            if len(self.bounds) == 0:
                error_messages.append((717, "No bounds provided."))

            if self.is_blocking() != (self.threshold_hint is not None and self.threshold_hint != ""):
                error_messages.append(
                    (718, "Mismatch: Blocking threshold must have at least one blocking Condition and a threshold_hint, or neither (for Auto threshold).")
                )

            if self.approach_hint == "":
                error_messages.append((719, "Approach hint is empty. Has to be a non-empty string."))

            return error_messages

        def add_blocking(self, *blocking: Condition):
            for condition in blocking:
                if isinstance(condition, TimerCondition):
                    self.timed_release = condition
                    continue
                self.blocking.add_conditions(condition)
            return self

        def set_visible_range(self, visible_range: int):
            self.visible_range = visible_range
            return self

        def set_hold(self, hold: int = -1):
            """
            Enter hysteresis hold, or permanently clear when hold is disabled.

            ``hold == -1`` means ``use default_hold``. If the effective value is
            ``-1``, the threshold is marked ``reached`` and never re-arms
            (no hysteresis). Otherwise the bar must leave the bound by that
            many points before the threshold can trigger again.

            Args:
                hold (int): Hold distance, or ``-1`` to use ``default_hold``.

            Returns:
                SituationThreshold: self
            """
            effective = self.default_hold if hold == -1 else hold
            if effective < 0:
                self.reached = True
                self.hold = -1
                if self.situation is not None and self.key in getattr(self.situation, "threshold_holds", {}):
                    self.situation.release_threshold_hold(self.key)
                return self

            self.hold = effective
            self.situation.add_threshold_hold(self, self.hold)
            return self

        def release_hold(self):
            self.hold = -1
            self.situation.release_threshold_hold(self.key)
            return self

        def is_bar_values_reached(self):
            for key in self.bounds.keys():
                bar_value = self.situation.bars[key].value
                if (self.direction > 0 and bar_value < self.bounds[key]) or (self.direction < 0 and bar_value > self.bounds[key]):
                    return False
            return True

        def add_bounds(self, **bounds):
            for key, value in bounds.items():
                self.bounds[key] = value
            return self

        def trigger_threshold(self):
            if self.reached or self.hold != -1:
                return

            if len(self.blocking) > 0 or self.timed_release is not None:
                situation_manager.add_threshold_check(self)
                if self.timed_release is not None:
                    self.timed_release.id = self.key
                    set_timer(self.key, "now")
            else:
                self.reached = True
                self.trigger_effects()
            return

        def add_effect(self, *effects: Effect):
            self.effects.extend(effects)
            return self

        def trigger_effects(self):
            for effect in self.effects:
                effect.apply()

        def load_thumbnail(self, **kwargs):
            refined_thumbnail = refine_image(self.thumbnail, **kwargs)
            if refined_thumbnail is not None:
                return refined_thumbnail
            return None

        def is_blocking(self):
            return len(self.blocking.get_conditions()) > 0

    # endregion
    #############################

    ############################
    # region SituationPassives #

    class SituationPassive(ABC):
        def __init__(self, name: str, description: str, *effects):
            self.name = name
            self.description = description
            self.effects = {}
            self.situation = None
            self._pending_effects = list(effects)
            self.active = False

        @property
        def type(self) -> str:
            return "passive"

        def run_self_test(self):
            error_messages = []
            if len(self.effects) == 0:
                error_messages.append((720, "No effects provided."))
            for effect in self.effects.values():
                error_messages.extend(effect.run_self_test())
                if isinstance(effect, UnlockableScheduleVoteEffect):
                    error_messages.append((721, "UnlockableScheduleVoteEffect is not allowed in a passive. Use a measure instead."))
            return error_messages

        def update_data(self, passive: SituationPassive):
            """
            Sync description and effects from a template passive.

            Args:
                passive (SituationPassive): Template passive from a fresh load.

            Returns:
                SituationPassive: self
            """
            self.description = passive.description
            self._sync_effects(passive)
            return self

        def _sync_effects(self, template: SituationPassive):
            """
            Sync effect definitions by local_key. Does not apply/revert modifiers.

            Args:
                template (SituationPassive): Template passive with bound effects.
            """
            template_effects = {effect.local_key: effect for effect in template._iter_effects()}

            for local_key, template_effect in template_effects.items():
                if local_key in self.effects:
                    self.effects[local_key].update_data(template_effect)
                    self.effects[local_key].passive = self
                else:
                    clone = template_effect.clone()
                    clone.passive = self
                    self.effects[local_key] = clone

            for local_key in list(self.effects.keys()):
                if local_key not in template_effects:
                    del self.effects[local_key]

        def _iter_effects(self):
            if self.effects:
                return list(self.effects.values())
            return list(self._pending_effects)

        def bind_situation(self, situation):
            """
            Attach to a situation and index pending effects by local_key.

            Args:
                situation (Situation): Parent situation.

            Returns:
                SituationPassive: self
            """
            self.situation = situation
            for effect in self._pending_effects:
                if not isinstance(effect, SituationEffect):
                    continue
                effect.passive = self
                self.effects[effect.local_key] = effect
            self._pending_effects = []
            for effect in self.effects.values():
                effect.passive = self
            return self

        def check(self, **kwargs):
            pass

        def activate(self):
            self.active = True
            self.run_effects()

        def deactivate(self):
            self.active = False
            self.revert_effects()

        def get_effects_description(self, in_rows: bool = False):
            if in_rows:
                rows = []
                for effect in self.effects.values():
                    rows.extend(effect.descriptions)
                return rows
            return ", ".join(effect.description for effect in self.effects.values())

        def get_description(self):
            return self.description

        def get_full_description(self):
            return self.description, self.get_effects_description(True)

        def add_effect(self, *effects):
            for effect in effects:
                if not isinstance(effect, SituationEffect):
                    continue
                effect.passive = self
                if self.situation is not None:
                    self.effects[effect.local_key] = effect
                else:
                    self._pending_effects.append(effect)
            return self

        def run_effects(self):
            for effect in self.effects.values():
                effect.apply()

        def revert_effects(self):
            for effect in self.effects.values():
                effect.revert()

        def detach_effects(self):
            """Clear local ModifierEffect handles without touching the registry."""
            for effect in self.effects.values():
                effect.detach()

        def check_available(self, **kwargs):
            return True

    class SituationMeasure(SituationPassive):
        def __init__(self, name: str, description: str, duration: TimerCondition, conditions: List[Condition], instant_effects: List[SituationEffect], permanent_effects: List[SituationEffect]):
            super().__init__(name, description, *permanent_effects)
            self.conditions = ConditionStorage()
            self.cooldown = None
            self.counter = None

            for condition in conditions:
                if isinstance(condition, TimerCondition):
                    self.cooldown = condition
                elif isinstance(condition, ManualCounterCondition) or isinstance(condition, CounterCondition) or isinstance(condition, LatchCounterCondition):
                    self.counter = condition
                else:
                    self.conditions.add_conditions(condition)

            self.instant_effects = instant_effects
            self.permanent_effects = permanent_effects
            self.duration = duration

        @property
        def type(self) -> str:
            return "measure"

        def get_effects_description(self, in_rows: bool = False):
            """
            Include instant (now) and lasting (while active) effect descriptions.

            Args:
                in_rows (bool): If True, return a list; otherwise a comma-joined string.

            Returns:
                list|str: Effect descriptions for journal display.
            """
            descs = []
            for effect in self.instant_effects:
                if isinstance(effect, SituationEffect):
                    for line in effect.descriptions:
                        descs.append(f"Now: {line}")
            for effect in self.effects.values():
                for line in effect.descriptions:
                    descs.append(f"While active: {line}")
            if in_rows:
                return descs
            return ", ".join(descs)

        def check_available(self, **kwargs):
            if self.situation is not None and self.situation.active_measure is not None:
                return False
            if self.counter is not None:
                kwargs[self.counter.counter_key] = self.active
            if not super().check_available(**kwargs):
                return False
            if not self.conditions.is_fulfilled(**kwargs):
                return False
            if self.cooldown is not None and get_timer(self.cooldown.id) is not None and not self.cooldown.is_fulfilled(**kwargs):
                return False
            if self.counter is not None and not self.counter.is_fulfilled(**kwargs):
                return False
            return True

        def check(self, **kwargs):
            if self.duration is not None and self.duration.is_fulfilled(**kwargs):
                self.deactivate()

        def activate(self):
            super().activate()
            if self.duration is not None:
                set_timer(self.duration.id, "now")
            if self.cooldown is not None:
                remove_timer(self.cooldown.id)
            if self.counter is not None and isinstance(self.counter, ManualCounterCondition):
                self.counter.increase()
            for effect in self.instant_effects:
                if isinstance(effect, SituationEffect):
                    effect.passive = self
                    effect.apply(conditions = self.conditions)

        def deactivate(self):
            super().deactivate()
            if self.duration is not None:
                remove_timer(self.duration.id)
            
            if self.cooldown is not None:
                set_timer(self.cooldown.id, "now")

            if self.situation is not None and self.situation.active_measure == self.name:
                self.situation.active_measure = None

        def bind_situation(self, situation):
            super().bind_situation(situation)
            for effect in self.instant_effects:
                if isinstance(effect, SituationEffect):
                    effect.passive = self
            return self

        def run_self_test(self):
            error_messages = []
            if len(self.effects) == 0 and len(self.instant_effects) == 0:
                error_messages.append((720, "No effects provided."))
            for effect in self.effects.values():
                error_messages.extend(effect.run_self_test())
            for effect in self.instant_effects:
                if isinstance(effect, SituationEffect):
                    error_messages.extend(effect.run_self_test())
            return error_messages

        def clone(self) -> SituationMeasure:
            conditions = self.conditions.get_conditions()
            if self.cooldown is not None:
                conditions.append(self.cooldown)
            if self.counter is not None:
                conditions.append(self.counter)
            return SituationMeasure(self.name, self.description, self.duration, conditions, list(self.instant_effects), list(self.permanent_effects))

    class SituationEffect(ABC):
        def __init__(self):
            self.passive = None
            self.effect = None

        @property
        @abstractmethod
        def local_key(self) -> str:
            """Stable identity within a passive (no situation prefix)."""
            pass

        @property
        def key(self) -> str:
            return (
                self.passive.situation.key
                + ":passive:"
                + self.passive.name
                + ":effect:"
                + self.local_key
            )

        @property
        @abstractmethod
        def description(self) -> str:
            pass

        @property
        def descriptions(self) -> list:
            """
            Description lines for the row (detail) display.

            Defaults to the single ``description``. Effects that carry several lines
            (e.g. ``SituationEffectGeneral``) override this so each line renders on
            its own row while ``description`` stays the comma-joined summary.
            """
            return [self.description]

        @abstractmethod
        def run_self_test(self):
            pass

        @abstractmethod
        def clone(self) -> SituationEffect:
            """Return a new unbound instance with the same definition."""
            pass

        @abstractmethod
        def update_data(self, other: SituationEffect):
            """Copy definition fields from another effect of the same type."""
            pass

        @abstractmethod
        def apply(self, **kwargs):
            pass

        @abstractmethod
        def revert(self):
            pass

        def detach(self):
            self.effect = None

    class SituationEffectSetGameData(SituationEffect):
        def __init__(self, data_key: str, value: float, description: str):
            super().__init__()
            self.data_key = data_key
            self.value = value
            self._description = description
            self._previous_value = None
            self._applied = False

        @property
        def local_key(self) -> str:
            return self.data_key

        @property
        def description(self) -> str:
            return self._description

        def clone(self) -> SituationEffectSetGameData:
            return SituationEffectSetGameData(self.data_key, self.value, self._description)

        def update_data(self, other: SituationEffect):
            if not isinstance(other, SituationEffectSetGameData):
                return
            self.data_key = other.data_key
            self.value = other.value
            self._description = other._description

        def run_self_test(self):
            error_messages = []
            if not isinstance(self.data_key, str) or self.data_key == "":
                error_messages.append((730, f"Game data key {self.data_key} is invalid."))
            if not isinstance(self.value, (int, float)):
                error_messages.append((731, f"Value {self.value} is not a float."))
            return error_messages

        def apply(self, **kwargs):
            self._previous_value = get_game_data(self.data_key)
            set_game_data(self.data_key, self.value)
            self._applied = True
            return self

        def revert(self, **kwargs):
            if not self._applied:
                return self
            if self._previous_value is None:
                remove_game_data(self.data_key)
            else:
                set_game_data(self.data_key, self._previous_value)
            self._previous_value = None
            self._applied = False
            return self

    class SituationEffectStatChangeModifier(SituationEffect):
        def __init__(self, stat: str, value: float, operation: str):
            super().__init__()
            self.stat = stat
            self.value = value
            self.operation = operation

        @property
        def local_key(self) -> str:
            return self.stat + "_" + self.operation

        @property
        def description(self) -> str:
            stat_name = Stat_Data[self.stat].get_title()
            operation_name = self.operation
            if operation_name == "+" and self.value < 0:
                return f"{stat_name}: -{self.value}"
            elif operation_name == "+":
                return f"{stat_name}: +{self.value}"
            elif operation_name == "*":
                return f"{stat_name}: *{self.value}"
            elif operation_name == "value_percent" and self.value > 0:
                return f"{stat_name}: +{self.value}% of the value"
            elif operation_name == "value_percent" and self.value < 0:
                return f"{stat_name}: -{self.value}% of the value"
            elif operation_name == "range_percent" and self.value > 0:
                return f"{stat_name}: +{self.value}% of the range"
            elif operation_name == "range_percent" and self.value < 0:
                return f"{stat_name}: -{self.value}% of the range"
            elif operation_name == "gated_percent" and self.value > 0:
                return f"{stat_name}: +{self.value}% of the gated range"
            elif operation_name == "gated_percent" and self.value < 0:
                return f"{stat_name}: -{self.value}% of the gated range"
            return f"{stat_name}: {operation_name} {self.value}"

        def clone(self) -> SituationEffectStatChangeModifier:
            return SituationEffectStatChangeModifier(self.stat, self.value, self.operation)

        def update_data(self, other: SituationEffect):
            if not isinstance(other, SituationEffectStatChangeModifier):
                return
            self.stat = other.stat
            self.value = other.value
            self.operation = other.operation

        def run_self_test(self):
            error_messages = []
            if Stat_Data[self.stat] == None:
                error_messages.append((740, f"Stat {self.stat} not found."))
            if not isinstance(self.value, (int, float)):
                error_messages.append((741, f"Value {self.value} is not a float."))
            if self.operation not in ["+", "*", "%", "value_percent", "range_percent", "gated_percent"]:
                error_messages.append((742, f"Operation {self.operation} is invalid. Has to be +, *, value_percent, range_percent or gated_percent."))
            return error_messages

        def apply(self, **kwargs):
            situation = self.passive.situation
            mod_key = self.key
            self.effect = ModifierEffect(
                mod_key,
                self.stat,
                Modifier_Obj(mod_key, self.operation, self.value),
                "default",
            )
            self.effect.apply(**kwargs)
            situation.track_modifier(
                mod_key, self.stat, "default", self.operation, self.value
            )
            return self

        def revert(self, **kwargs):
            mod_key = self.key
            if self.effect is not None:
                self.effect.revert(**kwargs)
                self.effect = None
            # Modifier already removed by ModifierEffect.revert — drop lifecycle entry
            lifecycle_registry.ping(mod_key, REMOVE)
            return self

    class SituationEffectBarChangeModifier(SituationEffect):
        def __init__(self, bar_key: str, value: float, operation: str, interval: str):
            super().__init__()
            self.bar_key = bar_key
            self.value = value
            self.operation = operation
            self.interval = interval

        @property
        def local_key(self) -> str:
            return self.bar_key + "_" + self.operation + "_" + self.interval

        @property
        def description(self) -> str:
            operation_name = self.operation
            if operation_name == "+" and self.value < 0:
                return f"Bar: -{self.value}/{self.interval}"
            elif operation_name == "+":
                return f"Bar: +{self.value}/{self.interval}"
            elif operation_name == "*":
                return f"Bar: *{self.value}/{self.interval}"
            elif operation_name == "value_percent" and self.value > 0:
                return f"Bar: +{self.value}%/{self.interval} of the value"
            elif operation_name == "value_percent" and self.value < 0:
                return f"Bar: -{self.value}%/{self.interval} of the value"
            elif operation_name == "range_percent" and self.value > 0:
                return f"Bar: +{self.value}%/{self.interval} of the range"
            elif operation_name == "range_percent" and self.value < 0:
                return f"Bar: -{self.value}%/{self.interval} of the range"
            elif operation_name == "gated_percent" and self.value > 0:
                return f"Bar: +{self.value}%/{self.interval} of the gated range"
            elif operation_name == "gated_percent" and self.value < 0:
                return f"Bar: -{self.value}%/{self.interval} of the gated range"
            return f"Bar: {operation_name} {self.value}/{self.interval}"

        def clone(self) -> SituationEffectBarChangeModifier:
            return SituationEffectBarChangeModifier(self.bar_key, self.value, self.operation, self.interval)

        def update_data(self, other: SituationEffect):
            if not isinstance(other, SituationEffectBarChangeModifier):
                return
            self.bar_key = other.bar_key
            self.value = other.value
            self.operation = other.operation
            self.interval = other.interval

        def run_self_test(self):
            error_messages = []
            if self.bar_key is None or self.bar_key == "":
                error_messages.append((740, f"Bar key {self.bar_key} is invalid."))
            elif self.passive is not None and self.passive.situation is not None and self.bar_key not in self.passive.situation.bars.keys() and self.bar_key != "ALL":
                error_messages.append((744, f"Bar key {self.bar_key} not found on situation."))
            if not isinstance(self.value, (int, float)):
                error_messages.append((741, f"Value {self.value} is not a float."))
            if self.operation not in ["+", "*", "%", "value_percent", "range_percent", "gated_percent"]:
                error_messages.append((742, f"Operation {self.operation} is invalid. Has to be +, *, value_percent, range_percent or gated_percent."))
            if self.interval not in ["daytime_change", "daily", "weekly", "monthly", "yearly"]:
                error_messages.append((743, f"Interval {self.interval} is invalid. Has to be daytime_change, daily, weekly, monthly or yearly."))
            return error_messages

        def apply(self, **kwargs):
            situation = self.passive.situation
            mod_key = self.key
            stat = f"situation:{situation.key}:{self.bar_key}"
            self.effect = ModifierEffect(
                mod_key,
                stat,
                Modifier_Obj(mod_key, self.operation, self.value),
                self.interval,
            )
            self.effect.apply(**kwargs)
            situation.track_modifier(
                mod_key, stat, self.interval, self.operation, self.value
            )
            return self

        def revert(self, **kwargs):
            mod_key = self.key
            if self.effect is not None:
                self.effect.revert(**kwargs)
                self.effect = None
            # Modifier already removed by ModifierEffect.revert — drop lifecycle entry
            lifecycle_registry.ping(mod_key, REMOVE)
            return self

    class SituationEffectCancelSituation(SituationEffect):
        def __init__(self):
            super().__init__()

        @property
        def local_key(self) -> str:
            return "cancel_situation"

        @property
        def description(self) -> str:
            return "Cancel situation"

        def clone(self) -> SituationEffectCancelSituation:
            return SituationEffectCancelSituation()

        def update_data(self, other: SituationEffect):
            return

        def run_self_test(self):
            return []

        def apply(self, **kwargs):
            situation = self.passive.situation
            situation.cancel()
            return self

        def revert(self, **kwargs):
            return self

    class SituationEffectRegularStatChange(SituationEffect):
        def __init__(self, stat: str, value: float, rhythm: str):
            super().__init__()
            self.stat = stat
            self.value = value
            self.rhythm = rhythm  # daytime_change, daily, weekly, monthly, yearly

        @property
        def local_key(self) -> str:
            return self.stat + "_" + self.rhythm

        @property
        def description(self) -> str:
            stat_name = Stat_Data[self.stat].get_title()
            rhythm_name = self.rhythm
            if rhythm_name == "daytime_change":
                rhythm_name = "Time"
            elif rhythm_name == "daily":
                rhythm_name = "Day"
            elif rhythm_name == "weekly":
                rhythm_name = "Week"
            elif rhythm_name == "monthly":
                rhythm_name = "Month"
            elif rhythm_name == "yearly":
                rhythm_name = "Year"

            sign = "+" if self.value >= 0 else ""
            return f"{stat_name}: {sign}{self.value}/{rhythm_name}"

        def clone(self) -> SituationEffectRegularStatChange:
            return SituationEffectRegularStatChange(self.stat, self.value, self.rhythm)

        def update_data(self, other: SituationEffect):
            if not isinstance(other, SituationEffectRegularStatChange):
                return
            self.stat = other.stat
            self.value = other.value
            self.rhythm = other.rhythm

        def run_self_test(self):
            error_messages = []
            if Stat_Data[self.stat] == None:
                error_messages.append((750, f"Stat {self.stat} not found."))
            if not isinstance(self.value, (int, float)):
                error_messages.append((751, f"Value {self.value} is not a float."))
            if self.rhythm not in ["daytime_change", "daily", "weekly", "monthly", "yearly"]:
                error_messages.append((752, f"Rhythm {self.rhythm} not found."))
            return error_messages

        def apply(self, **kwargs):
            situation = self.passive.situation
            mod_key = self.key
            self.effect = ModifierEffect(
                mod_key,
                self.stat,
                Modifier_Obj(mod_key, "+", self.value),
                self.rhythm,
            )
            self.effect.apply(**kwargs)
            situation.track_modifier(mod_key, self.stat, self.rhythm, "+", self.value)
            return self

        def revert(self, **kwargs):
            mod_key = self.key
            if self.effect is not None:
                self.effect.revert(**kwargs)
                self.effect = None
            # Modifier already removed by ModifierEffect.revert — drop lifecycle entry
            lifecycle_registry.ping(mod_key, REMOVE)
            return self

    class SituationEffectGeneral(SituationEffect):
        """
        Bridge between the SituationEffect description layer and *any* regular Effect.

        The other SituationEffect types exist because a plain ``Effect`` cannot
        produce an accurate player-facing description of itself — the SituationEffect
        supplies that description. That also limits passives/measures to the handful
        of built-in SituationEffect types. ``SituationEffectGeneral`` removes that
        limit: it wraps a list of ordinary ``Effect`` objects (money, level, building
        open/close, stat, …) and applies/reverts them, while the author writes the
        description(s) to show.

        Several descriptions are supported because in the selection list they are
        joined comma-separated (via ``description``) and in the detail view they are
        listed one per row (via ``descriptions``).

        Args:
            key (str): Stable, author-chosen identity for this effect within its
                passive/measure. Must be unique among the effects of that
                passive/measure — the wrapped effect set is *not* enough, since two
                generals can wrap the same effect types.
            effects (List[Effect]): Regular effects to apply (and, unless disabled,
                revert). Not SituationEffects — ordinary game ``Effect`` objects.
            descriptions (List[str]): Player-facing description lines.
            revert (bool): If ``False``, ``revert()`` is a no-op so the wrapped
                effects are never undone (e.g. a one-way unlock or a cost that must
                not be refunded). Default ``True``.
        """

        def __init__(self, key: str, effects: List[Effect], descriptions: List[str], revert: bool = True):
            super().__init__()
            self._key = key
            self._effects = list(effects) if effects else []
            self._descriptions = list(descriptions) if descriptions else []
            self._do_revert = revert
            self._applied = False

        @property
        def local_key(self) -> str:
            return "general:" + str(self._key)

        @property
        def description(self) -> str:
            return ", ".join(self._descriptions)

        @property
        def descriptions(self) -> list:
            return list(self._descriptions)

        def clone(self) -> SituationEffectGeneral:
            return SituationEffectGeneral(
                self._key,
                list(self._effects),
                list(self._descriptions),
                self._do_revert,
            )

        def update_data(self, other: SituationEffect):
            if not isinstance(other, SituationEffectGeneral):
                return
            self._key = other._key
            self._effects = list(other._effects)
            self._descriptions = list(other._descriptions)
            self._do_revert = other._do_revert

        def run_self_test(self):
            error_messages = []
            if not isinstance(self._key, str) or self._key == "":
                error_messages.append((760, f"SituationEffectGeneral key {self._key} is invalid."))
            if not isinstance(self._effects, list) or len(self._effects) == 0:
                error_messages.append((761, "SituationEffectGeneral needs at least one effect."))
            else:
                for effect in self._effects:
                    if not isinstance(effect, Effect):
                        error_messages.append((762, f"{effect} is not an Effect."))
            if not isinstance(self._descriptions, list) or len(self._descriptions) == 0:
                error_messages.append((763, "SituationEffectGeneral needs at least one description."))
            else:
                for desc in self._descriptions:
                    if not isinstance(desc, str):
                        error_messages.append((763, f"Description {desc} is not a string."))
            if not isinstance(self._do_revert, bool):
                error_messages.append((764, f"revert flag {self._do_revert} is not a bool."))
            return error_messages

        def apply(self, **kwargs):
            for effect in self._effects:
                effect.apply(**kwargs)
            self._applied = True
            return self

        def revert(self, **kwargs):
            if not self._do_revert:
                return self
            if not self._applied:
                return self
            for effect in self._effects:
                effect.revert(**kwargs)
            self._applied = False
            return self

    # endregion
    ############################

    #################################
    # region SituationStartModifier #

    class SituationStartModifier:
        """
        Start-value modifier stored on a bar (not in global modifier collections).

        General modifiers (no stat) reshape the running start value with `*`, `value_percent`, `range_percent`, `gated_percent`, `+`.
        Stat-based modifiers read a school-stat snapshot at situation activation and
        contribute from that reading.

        Attributes:
            modifier (Modifier_Obj): Operator and value payload.
            stat (str | None): Optional school-stat key for snapshot contributions.
        """

        def __init__(self, modifier: Modifier_Obj, stat: str = None):
            """
            Args:
                modifier (Modifier_Obj): Operator/value used during start calculation.
                stat (str, optional): School-stat key. None = general modifier.
            """
            self.modifier = modifier
            self.stat = stat

        @property
        def op(self) -> str:
            return self.modifier._mod_type if isinstance(self.modifier, Modifier_Obj) else None

        @property
        def value(self) -> float:
            return self.modifier.get_value() if isinstance(self.modifier, Modifier_Obj) else None

        def validate(self, bar_key: str = None) -> list:
            """
            Validate this start modifier for runtime or definition registration.

            Args:
                bar_key (str, optional): Bar key for error context.

            Returns:
                list: ``(code, message)`` pairs; empty if valid.
            """
            errors = []
            loc = f" on bar '{bar_key}'" if bar_key else ""

            if not isinstance(self.modifier, Modifier_Obj):
                errors.append((766, f"Start modifier{loc} is not a Modifier_Obj."))
                return errors

            name = self.modifier.get_name()
            if name is None or name == "":
                errors.append((769, f"Start modifier{loc} has an empty name."))

            if self.op not in ["+", "*", "%", "value_percent", "range_percent", "gated_percent"]:
                errors.append((767, f"Start modifier op '{self.op}'{loc} is invalid. Has to be +, *, value_percent, range_percent or gated_percent."))

            if not isinstance(self.value, (int, float)):
                errors.append((770, f"Start modifier value '{self.value}'{loc} is not a number."))

            if self.stat is not None:
                if self.stat not in Stat_Data or Stat_Data[self.stat] is None:
                    errors.append((768, f"Start modifier stat '{self.stat}'{loc} not found."))

            return errors

        def clone(self) -> SituationStartModifier:
            """Return an unbound copy with the same definition."""
            mod = Modifier_Obj(
                self.modifier.get_name(),
                self.modifier._mod_type,
                self.modifier.get_value(),
            )
            return SituationStartModifier(mod, self.stat)

    #endregion
    #################################

    ############################
    # region SituationBar #

    class SituationBar:
        def __init__(self, key: str, regular_decrease_rate: float = 0, regular_decrease_interval: str = "daytime_change"):
            self.key = key

            self.min = -100
            self.max = 100
            self.value = 0

            self.stat_weights = {}

            self._weight = 1.0

            self.tendency = 0
            self.changes = [] # last 5 bar changes

            self.regular_decrease_rate = regular_decrease_rate
            self.regular_decrease_interval = regular_decrease_interval

            # Start-value snapshot (applied once on situation activate)
            self.start_base = 0.0
            self.start_modifiers = []  # authored definition
            self.start_shifts = []     # runtime (events); survives definition sync
            self._start_applied = False

            self.situation = None
            self._decrease_mod_collection = None

            self.pictograms = []

        @property
        def decrease_mod_key(self) -> str:
            """Stable modifier identity; unique per situation bar."""
            return self.situation.key + ":bar:" + self.key + ":decrease"

        @property
        def decrease_mod_stat(self) -> str:
            """Routed by change_stat to situation_manager.apply_progress_change."""
            return "situation:" + self.situation.key + ":" + self.key
            
        def run_self_test(self):
            error_messages = []
            if self.min > self.max:
                error_messages.append((760, f"Min {self.min} is greater than max {self.max}."))
            if self._weight < 0:
                error_messages.append((761, f"Weight {self._weight} is less than 0."))
            if any(Stat_Data[stat] == None for stat in self.stat_weights.keys()):
                invalid_stats = [stat for stat in self.stat_weights.keys() if Stat_Data[stat] == None]
                error_messages.append((762, f"Stat(s) {invalid_stats} not found."))
            if self.key is None or self.key == "":
                error_messages.append((763, "Key is empty. Has to be a non-empty string."))
            if self._weight == 0:
                error_messages.append((764, "Weight is 0. Has to be greater than 0."))
            if self.regular_decrease_interval not in ["daytime_change", "daily", "weekly", "monthly", "yearly"]:
                error_messages.append((765, f"Regular decrease interval {self.regular_decrease_interval} not found."))
            for entry in self.start_modifiers + self.start_shifts:
                if not isinstance(entry, SituationStartModifier):
                    error_messages.append((766, f"Start modifier on bar '{self.key}' is invalid."))
                    continue
                error_messages.extend(entry.validate(self.key))

            return error_messages

        def update_data(self, bar: SituationBar):
            if not hasattr(self, "start_base"):
                self.start_base = 0.0
            if not hasattr(self, "start_modifiers"):
                self.start_modifiers = []
            if not hasattr(self, "start_shifts"):
                self.start_shifts = []
            if not hasattr(self, "_start_applied"):
                # Preserve existing progress on old saves that are already active
                already_active = (
                    self.situation is not None
                    and getattr(self.situation, "state", None) == "active"
                )
                self._start_applied = already_active

            self.key = bar.key
            self.min = bar.min
            self.max = bar.max
            self.stat_weights = bar.stat_weights
            self.regular_decrease_rate = bar.regular_decrease_rate
            self.regular_decrease_interval = bar.regular_decrease_interval
            self.start_base = bar.start_base
            self.start_modifiers = [entry.clone() for entry in bar.start_modifiers]
            self.pictograms = [pictogram for pictogram in bar.pictograms]
            # start_shifts intentionally preserved (runtime event adjustments)
            return self

        def __str__(self):
            return "situation:" + self.situation.key + ":" + self.key

        def activate(self):
            self.apply_decrease_modifier()
            self.load_start_value()

        def add_pictogram(self, pictogram: Pictogram | str):
            pictogram_key = pictogram
            if isinstance(pictogram, Pictogram):
                pictogram_key = pictogram.key
            if pictogram_manager is None or not pictogram_manager.has_pictogram(pictogram_key):
                log(f"Pictogram {pictogram_key} not found.", log_type="error", category="situation")
                return self
            if pictogram_key not in self.pictograms:
                self.pictograms.append(pictogram_key)
            return self

        def get_pictogram_data(self) -> Dict[str, Dict[str, Any]]:
            output = {}
            if pictogram_manager is None:
                return output
            for pictogram in self.pictograms:
                values = self.get_pictogram_values()
                pictogram_label = pictogram_manager.get_label(pictogram, **values)
                pictogram_tooltip = pictogram_manager.get_tooltip(pictogram, **values)
                pictogram_icon = pictogram_manager.get_icon(pictogram, **values)
                if pictogram_icon is not None:
                    output[self.situation.key + ":" + self.key + ":" + pictogram] = {
                        "key": pictogram,
                        "label": pictogram_label,
                        "tooltip": pictogram_tooltip,
                        "icon": pictogram_icon,
                    }
            return output

        def get_pictogram_values(self) -> Dict[str, Any]:
            return {
                "bar_key": self.key,
                "bar_value": self.value,
                "bar_tendency": self.tendency,
                "bar_area": self.get_bar_value_area(),
                "bar_mood": self.get_bar_value_mood(),
                "bar_min": self.min,
                "bar_max": self.max,
                "bar_regular_decrease_rate": self.regular_decrease_rate,
                "bar_regular_decrease_interval": self.regular_decrease_interval,
            }

        def get_bar_value_area(self) -> int:
            return get_bar_value_area(self.min, self.max, self.value)

        def get_bar_value_mood(self) -> str:
            return get_bar_value_mood(self.get_bar_value_area(), self.min, self.max)

        def set_start_base(self, value: float):
            """
            Set the basis applied before start modifiers (* → value_percent → range_percent → gated_percent → +).

            Args:
                value (float): Starting basis (often 0 or a mild negative).

            Returns:
                SituationBar: self
            """
            self.start_base = float(value)
            return self

        def add_start_modifier(self, modifier: Modifier_Obj | SituationStartModifier, stat: str = None):
            """
            Add an authored start-value modifier (synced from definitions).
            Validates at registration time and rejects invalid entries.

            Args:
                modifier (Modifier_Obj | SituationStartModifier): Operator/value payload
                    or a prebuilt start modifier.
                stat (str, optional): School-stat key for snapshot contribution.
                    Ignored if ``modifier`` is already a SituationStartModifier.

            Returns:
                bool: True if the modifier was accepted and stored.
            """
            return self._register_start_modifier(self.start_modifiers, modifier, stat)

        def add_start_shift(self, op: str, value: float, name: str = None, stat: str = None):
            """
            Add a runtime start-value shift (e.g. from events before activation).
            Builds the Modifier_Obj internally, validates, then stores it.
            Survives definition sync via update_data.

            Args:
                op (str): ``+``, ``*``, ``value_percent``, ``range_percent`` or ``gated_percent``.
                value (float): Operand (flat, factor, percent, or stat weight).
                name (str, optional): Modifier identity. Auto-generated if omitted.
                stat (str, optional): School-stat key for snapshot contribution.

            Returns:
                bool: True if the shift was accepted and stored.
            """
            if name is None:
                stat_part = stat if stat is not None else "general"
                name = f"start_shift:{self.key}:{stat_part}:{op}:{value}"
            return self._register_start_modifier(
                self.start_shifts,
                Modifier_Obj(name, op, value),
                stat,
            )

        def _register_start_modifier(self, target: list, modifier, stat: str = None) -> bool:
            """
            Validate and append a start modifier to the given list.

            Args:
                target (list): ``start_modifiers`` or ``start_shifts``.
                modifier (Modifier_Obj | SituationStartModifier): Entry to register.
                stat (str, optional): Optional stat when building from Modifier_Obj.

            Returns:
                bool: True if stored; False if validation failed (errors logged).
            """
            self._ensure_start_fields()

            if isinstance(modifier, SituationStartModifier):
                entry = modifier
            elif isinstance(modifier, Modifier_Obj):
                entry = SituationStartModifier(modifier, stat)
            else:
                log(f"Start modifier on bar '{self.key}' is not a Modifier_Obj or SituationStartModifier.", log_type="error", category="situation")
                return False

            errors = entry.validate(self.key)
            if errors:
                for code, message in errors:
                    log(message, log_type="error", category="situation")
                return False

            target.append(entry)
            return True

        def reset_start_application(self):
            """Allow load_start_value to run again (e.g. after complete)."""
            self._start_applied = False
            return self

        def _ensure_start_fields(self):
            if not hasattr(self, "start_base"):
                self.start_base = 0.0
            if not hasattr(self, "start_modifiers"):
                self.start_modifiers = []
            if not hasattr(self, "start_shifts"):
                self.start_shifts = []
            if not hasattr(self, "_start_applied"):
                already_active = (
                    self.situation is not None
                    and getattr(self.situation, "state", None) == "active"
                )
                self._start_applied = already_active

        def _iter_start_modifiers(self):
            self._ensure_start_fields()
            return list(self.start_modifiers) + list(self.start_shifts)

        def _apply_start_star(self, value: float, entry: SituationStartModifier) -> float:
            if entry.stat is None:
                return value * entry.value
            # Normalized snapshot factor: (stat/100) * weight
            return value * (get_stat_number(entry.stat) / 100.0) * entry.value

        def _apply_start_percent(self, value: float, entry: SituationStartModifier) -> float:
            if entry.stat is None:
                return value + value / 100.0 * entry.value
            # Percent of the snapshot stat (not of running value)
            return value + get_stat_number(entry.stat) / 100.0 * entry.value

        def _apply_start_plus(self, value: float, entry: SituationStartModifier) -> float:
            if entry.stat is None:
                return value + entry.value
            # Weight × snapshot (e.g. happiness 50 with weight 0.1 → +5)
            return value + get_stat_number(entry.stat) * entry.value

        def compute_start_value(self) -> float:
            """
            Compute the start value from base + modifiers without writing the bar.

            Order: Handles all current modifier operators including: 
                ``+`` (add), 
                ``*`` (multiply), 
                ``value_percent`` (modulo of base value), 
                ``range_percent``, 
                ``gated_percent`` 
            and applies them as specified by the Modifier_Obj/SituationStartModifier entries. 
            Clamps to bar limits at the end.

            Returns:
                float: Clamped start value.
            """
            self._ensure_start_fields()
            value = float(self.start_base)
            entries = self._iter_start_modifiers()

            # STAR: "*"
            for entry in entries:
                if entry.op == "*" or entry.op == "mul":
                    value = self._apply_start_star(value, entry)

            # PERCENT: "%", "value_percent"
            for entry in entries:
                if entry.op == "%" or entry.op == "value_percent":
                    value = self._apply_start_percent(value, entry)

            # RANGE_PERCENT
            for entry in entries:
                if entry.op == "range_percent":
                    # Typically: add this amount of the total range to base value
                    bar_range = self.max - self.min
                    if entry.stat is None:
                        value += (bar_range * entry.value / 100.0)
                    else:
                        # If stat provided, scale by stat number
                        value += (bar_range * get_stat_number(entry.stat) * entry.value / 100.0)
            
            # GATED_PERCENT
            for entry in entries:
                if entry.op == "gated_percent":
                    # If stat is given, use as gate/reference, otherwise fall back to bar range
                    gate_range = get_gated_range(entry.stat if entry.stat else "", entry.value)
                    value += (gate_range * entry.value / 100.0)

            # PLUS: "+"
            for entry in entries:
                if entry.op == "+" or entry.op == "add":
                    value = self._apply_start_plus(value, entry)

            if value > self.max:
                value = self.max
            if value < self.min:
                value = self.min
            return value
       

        def load_start_value(self):
            """
            Apply the start-value snapshot once when the situation activates.

            Subsequent calls are no-ops until reset_start_application (complete).
            """
            self._ensure_start_fields()
            if self._start_applied:
                return self
            self.value = self.compute_start_value()
            self._start_applied = True
            return self

        def apply_decrease_modifier(self):
            """
            Register the constant bar decrease modifier in the rhythm collection.

            Skips registration while the cascading resolution breather is active.

            Returns:
                SituationBar: self
            """
            if self.situation is None or self.regular_decrease_rate == 0:
                self.revert_decrease_modifier()
                return self

            if (
                situation_manager is not None
                and situation_manager.is_resolution_breather_active()
            ):
                self.revert_decrease_modifier()
                return self

            modifier = Modifier_Obj(self.decrease_mod_key, "+", self.regular_decrease_rate)
            set_modifier(
                self.decrease_mod_key,
                modifier,
                stat=self.decrease_mod_stat,
                collection=self.regular_decrease_interval,
            )
            self.situation.track_modifier(
                self.decrease_mod_key,
                self.decrease_mod_stat,
                self.regular_decrease_interval,
                "+",
                self.regular_decrease_rate,
            )
            self._decrease_mod_collection = self.regular_decrease_interval
            return self

        def revert_decrease_modifier(self):
            """
            Remove the bar decrease modifier from the global registry.

            Returns:
                SituationBar: self
            """
            if self.situation is None:
                return self

            if lifecycle_registry.has(self.decrease_mod_key):
                self.situation.untrack_and_remove(self.decrease_mod_key)
            else:
                collection = self._decrease_mod_collection or self.regular_decrease_interval
                remove_modifier(
                    self.decrease_mod_key,
                    stat=self.decrease_mod_stat,
                    collection=collection,
                )
            self._decrease_mod_collection = None
            return self

        def sync_decrease_modifier(self):
            """
            Refresh decrease modifier definition after template reload.

            Re-applies only while the parent situation is active.

            Returns:
                SituationBar: self
            """
            self.revert_decrease_modifier()
            if self.situation is not None and self.situation.state == "active":
                self.apply_decrease_modifier()
            return self

        def add_stat_weight(self, stat: str, weight: int):
            self.stat_weights[stat] = weight
            return self

        def set_weight(self, weight: float):
            self._weight = weight
            return self

        def set_limits(self, min: int, max: int):
            self.min = min
            self.max = max
            return self

        def change_value(self, delta: float):
            if delta < 0 and self.situation is not None and self.situation.should_block_negative_delta():
                return

            old_value = self.value
            thresholds, blocking = self.situation.get_thresholds_in_range(self.value, self.key, abs(delta), delta)
            if blocking != None:
                self.value = blocking.bounds[self.key]
            else:
                self.value += delta
                if self.value > self.max:
                    self.value = self.max
                if self.value < self.min:
                    self.value = self.min

            actual_change = self.value - old_value
            self.changes.append(actual_change)
            if len(self.changes) > 5:
                self.changes.pop(0)
            self.tendency = sum(self.changes) / len(self.changes)

            for threshold in thresholds:
                if threshold.is_bar_values_reached():
                    threshold.trigger_threshold()

            self.situation.check_resolutions()

        def change_value_via_stats(self, key: str, delta: float):
            if key in self.stat_weights.keys():
                self.change_value(delta * self.stat_weights[key])

        def reached_min(self):
            return self.value == self.min       

        def reached_max(self):
            return self.value == self.max

        def get_full_range(self) -> float:
            """
            Returns the full available range of the bar.

            Returns:
                float: ``max - min``.
            """
            return self.max - self.min

        def get_gate(self, direction: int) -> float:
            """
            Returns the next blocking-threshold gate in the given direction.

            If no blocking threshold remains in that direction, the corresponding
            bar end is used (``max`` for +, ``min`` for -).

            Args:
                direction (int): Search direction. Positive for the upward gate,
                    negative for the downward gate.

            Returns:
                float: Gate value for the given direction.
            """
            if direction == 0:
                return self.value

            if self.situation is None:
                return self.max if direction > 0 else self.min

            thresholds = self.situation.get_next_blocking_thresholds(direction)
            threshold = thresholds.get(self.key)
            if threshold is None:
                return self.max if direction > 0 else self.min
            return threshold.bounds[self.key]

        def get_gated_bounds(self, modifier_value: float) -> tuple:
            """
            Returns the gated bounds for a modifier relative to the current bar value.

            Blocking thresholds act as gates. Rules:
            - modifier >= 0 and progress >= 0 → ``(0, positive_gate)``
            - modifier < 0 and progress < 0 → ``(0, negative_gate)``
            - modifier >= 0 and progress < 0 → ``(progress, positive_gate)``
            - modifier < 0 and progress >= 0 → ``(progress, negative_gate)``

            Args:
                modifier_value (float): Modifier value whose sign selects the rule.

            Returns:
                tuple: ``(start, end)`` of the gated range. Order follows the rules
                    above and is not sorted.
            """
            progress = self.value
            positive_gate = self.get_gate(1)
            negative_gate = self.get_gate(-1)

            if modifier_value >= 0 and progress >= 0:
                return (0, positive_gate)
            if modifier_value < 0 and progress < 0:
                return (0, negative_gate)
            if modifier_value >= 0 and progress < 0:
                return (progress, positive_gate)
            return (progress, negative_gate)

        def get_gated_range(self, modifier_value: float) -> float:
            """
            Returns the size of the gated range for a modifier on this bar.

            Uses ``get_gated_bounds`` and returns the absolute span between start
            and end. Intended as reference range for upcoming modifier operators.

            Args:
                modifier_value (float): Modifier value whose sign selects the gate rule.

            Returns:
                float: Absolute size of the gated range.
            """
            start, end = self.get_gated_bounds(modifier_value)
            return abs(end - start)

        def check_threshold_hold(self, threshold: SituationThreshold):
            threshold_value = threshold.bounds[self.key]
            hold = threshold.hold
            direction = threshold.direction

            if (direction < 0 and threshold_value + hold < self.value) or \
                (direction > 0 and threshold_value - hold > self.value):
                return True
            return False

    #endregion
    #################################

    ##############################
    # region SituationEventPools #

    class SituationEventPools:
        def __init__(self, key: str, min: int, max: int, bar: str = None):
            self.key = key
            self.min = min
            self.max = max
            self.situation = None
            self.bar = bar

        def __str__(self):
            return "situation_pool:" + self.situation.key + ":" + self.key

        def update_data(self, pool: SituationEventPools):
            self.key = pool.key
            self.min = pool.min
            self.max = pool.max
            self.bar = pool.bar
            return self

        def run_self_test(self):
            error_messages = []
            if self.min > self.max:
                error_messages.append((771, f"Min {self.min} is greater than max {self.max}."))
            if self.bar is not None:
                if self.bar not in self.situation.bars.keys():
                    error_messages.append((770, f"Bar {self.bar} not found."))
                else:    
                    if self.min < self.situation.bars[self.bar].min:
                        error_messages.append((772, f"Min {self.min} is less than bar {self.bar} min {self.situation.bars[self.bar].min}."))
                    if self.max > self.situation.bars[self.bar].max:
                        error_messages.append((773, f"Max {self.max} is greater than bar {self.bar} max {self.situation.bars[self.bar].max}."))
            else:
                if self.min < self.situation.get_combined_bar_min():
                    error_messages.append((774, f"Min {self.min} is less than combined bar min {self.situation.get_combined_bar_min()}."))
                if self.max > self.situation.get_combined_bar_max():
                    error_messages.append((775, f"Max {self.max} is greater than combined bar max {self.situation.get_combined_bar_max()}."))
            return error_messages

        def check_pool(self):
            if self.bar is None:
                combined_bar = self.situation.get_combined_bar_value()
                return combined_bar >= self.min and combined_bar <= self.max
            else:
                bar_value = self.situation.bars[self.bar].value
                return bar_value >= self.min and bar_value <= self.max

    #endregion
    ##############################

    ##############################
    # region SituationResolution #

    class SituationResolution(ABC):
        """
        Base resolution. Intrinsically "reached" when subclass condition holds;
        fires only when gating conditions are fulfilled (or immediately if none).
        """

        def __init__(self, key: str, value, *elements):
            self.key = key
            self.value = value
            self.situation = None
            self.effects = EffectStorage()
            self.conditions = ConditionStorage()
            self._grace_active = False

            for element in elements:
                if isinstance(element, Condition):
                    self.conditions.add_condition(element)
                elif isinstance(element, Effect):
                    self.effects.effects.append(element)

        @property
        def counter_key(self) -> str:
            """Stable key for resolution latch kwargs / LatchCounterCondition."""
            situation_key = self.situation.key if self.situation is not None else ""
            return f"situation_resolution:{situation_key}:{self.key}"

        @property
        def has_grace(self) -> bool:
            """Grace period exists when gating conditions are configured."""
            return len(self.conditions) > 0

        def bind_situation(self, situation):
            """Attach parent situation and finalize latch keys if needed."""
            self.situation = situation
            self._bind_latch_keys()
            return self

        def _bind_latch_keys(self):
            """Override latch counter_key on conditions unless NoOverride is set."""
            for condition in self.conditions.find_by_type("latch_counter"):
                if condition.get_option_set().has_option("NoOverride"):
                    continue
                condition.counter_key = self.counter_key

        def run_self_test(self):
            error_messages = []
            if len(self.effects) == 0:
                error_messages.append((780, "No effects provided."))
            return error_messages

        @abstractmethod
        def is_reached(self) -> bool:
            """Intrinsic resolution state (bar limit / deadline), ignoring gates."""
            pass

        def get_timer_conditions(self) -> list:
            return self.conditions.find_by_type("timer")

        def start_grace(self):
            """Begin grace: start timers found in the condition storage."""
            if self._grace_active:
                return
            self._grace_active = True
            for timer_condition in self.get_timer_conditions():
                set_timer(timer_condition.id, "now")
            self._on_enter_grace()

        def end_grace(self):
            """Leave grace: remove timers and clear grace flag."""
            if not self._grace_active:
                return
            for timer_condition in self.get_timer_conditions():
                remove_timer(timer_condition.id)
            self._grace_active = False

        def _build_check_kwargs(self, **kwargs) -> dict:
            check_kwargs = dict(kwargs)
            check_kwargs[self.counter_key] = self.is_reached()
            return check_kwargs

        def check_conditions(self, **kwargs) -> bool:
            if not self.has_grace:
                return True
            return self.conditions.is_fulfilled(**self._build_check_kwargs(**kwargs))

        def fire(self) -> bool:
            """Apply effects, end grace, complete situation."""
            self.end_grace()
            self.effects.apply(conditions = self.conditions)
            if self.situation is not None:
                self.situation.complete()
            return True

        def evaluate(self, **kwargs) -> bool:
            """
            Evaluate reach + grace/gates. Returns True if the resolution fired.

            Reach without grace conditions → fire immediately.
            Reach with conditions → start grace/timers; fire when conditions pass.
            Leave reach → end grace (timers removed).
            """
            reached = self.is_reached()
            check_kwargs = self._build_check_kwargs(**kwargs)

            if not reached:
                if self._grace_active:
                    self._notify_left_reach(check_kwargs)
                    self.end_grace()
                return False

            if not self.has_grace:
                return self.fire()

            if not self._grace_active:
                if not self._can_enter_grace(check_kwargs):
                    return self.fire()
                self.start_grace()

            if self.check_conditions(**kwargs):
                return self.fire()
            return False

        def _can_enter_grace(self, check_kwargs: dict) -> bool:
            """Subclasses may block further grace (e.g. latch exhausted). Default: allow."""
            return True

        def _on_enter_grace(self):
            """Hook when entering grace (e.g. negative latch rising edge)."""
            pass

        def _notify_left_reach(self, check_kwargs: dict):
            """Hook when leaving reached state (e.g. negative latch falling edge)."""
            pass

        def update_data(self, resolution: SituationResolution):
            self.value = resolution.value
            self.effects = resolution.effects
            self.conditions = resolution.conditions
            self._bind_latch_keys()
            return self

    class SituationNegativeResolution(SituationResolution):
        def __init__(self, value: str, *elements, grace_count: int = None):
            # value: ALL, ANY
            super().__init__("negative_resolution", value, *elements)
            self.grace_count = grace_count
            self.latch = None
            if grace_count is not None:
                self.latch = LatchCounterCondition(self.counter_key, grace_count)

        def bind_situation(self, situation):
            super().bind_situation(situation)
            if self.latch is not None:
                self.latch.counter_key = self.counter_key
            return self

        def run_self_test(self):
            error_messages = super().run_self_test()
            if self.value not in ["ALL", "ANY"]:
                error_messages.append((781, f"Value {self.value} is not valid. Has to be ALL or ANY."))
            if self.grace_count is not None and (not isinstance(self.grace_count, int) or self.grace_count < 1):
                error_messages.append((784, f"grace_count {self.grace_count} is invalid. Has to be a positive int or None."))
            return error_messages

        def is_reached(self) -> bool:
            if self.value == "ALL":
                return all(bar.reached_min() for bar in self.situation.bars.values())
            if self.value == "ANY":
                return any(bar.reached_min() for bar in self.situation.bars.values())
            return False

        def _can_enter_grace(self, check_kwargs: dict) -> bool:
            if self.latch is None or not self.has_grace:
                return True
            # Exhausted latch → no further grace, fire immediately on reach
            count = get_game_data(f"latch_counter_count:{self.latch.counter_key}", 0)
            return count < self.latch.max

        def _on_enter_grace(self):
            if self.latch is not None:
                self.latch.is_fulfilled(**self._build_check_kwargs())

        def _notify_left_reach(self, check_kwargs: dict):
            if self.latch is not None:
                self.latch.is_fulfilled(**check_kwargs)

        def fire(self) -> bool:
            """
            Apply negative resolution effects and trigger the cascading breather.

            Returns:
                bool: True after the resolution fires.
            """
            result = super().fire()
            if result and situation_manager is not None:
                situation_manager.trigger_resolution_breather()
            return result

        def update_data(self, resolution: SituationResolution):
            super().update_data(resolution)
            if isinstance(resolution, SituationNegativeResolution):
                self.grace_count = resolution.grace_count
                if self.grace_count is not None:
                    self.latch = LatchCounterCondition(self.counter_key, self.grace_count)
                else:
                    self.latch = None
            return self

    class SituationPositiveResolution(SituationResolution):
        def __init__(self, value: str, *elements, delta_lock: bool = False):
            # value: ALL, ANY
            super().__init__("positive_resolution", value, *elements)
            self.delta_lock = delta_lock

        def run_self_test(self):
            error_messages = super().run_self_test()
            if self.value not in ["ALL", "ANY"]:
                error_messages.append((782, f"Value {self.value} is not valid. Has to be ALL or ANY."))
            return error_messages

        def is_reached(self) -> bool:
            if self.value == "ALL":
                return all(bar.reached_max() for bar in self.situation.bars.values())
            if self.value == "ANY":
                return any(bar.reached_max() for bar in self.situation.bars.values())
            return False

        def update_data(self, resolution: SituationResolution):
            super().update_data(resolution)
            if isinstance(resolution, SituationPositiveResolution):
                self.delta_lock = resolution.delta_lock
            return self

    class SituationDeadlineResolution(SituationResolution):
        def __init__(self, value: Time, *elements):
            super().__init__("deadline_resolution", value, *elements)

        def run_self_test(self):
            error_messages = super().run_self_test()
            if not isinstance(self.value, Time):
                error_messages.append((783, "Value is not a Time object."))
            return error_messages

        def is_reached(self) -> bool:
            return time.now_is_after_time(
                self.value.get_day(),
                self.value.get_month(),
                self.value.get_year(),
                self.value.get_daytime(),
            )

    class SituationConditionResolution(SituationResolution):
        """
        Resolution that fires solely from its ConditionStorage.

        Bar fill, deadlines, and other situation progress are ignored. As soon as
        the configured conditions are fulfilled, effects apply and the situation
        completes (while the situation is still active and checked).
        """

        def __init__(self, key: str, *elements):
            """
            Args:
                key (str): Unique resolution key on the situation.
                *elements: ``Condition`` and/or ``Effect`` instances. At least one
                    of each is required (validated in ``run_self_test``).
            """
            super().__init__(key, None, *elements)

        @property
        def has_grace(self) -> bool:
            """
            Conditions are the reach criteria, not a post-reach grace gate.

            Returns:
                bool: Always ``False``.
            """
            return False

        def run_self_test(self):
            error_messages = super().run_self_test()
            if self.key is None or self.key == "":
                error_messages.append((785, "Condition resolution key is empty."))
            if len(self.conditions) == 0:
                error_messages.append((786, "Condition resolution needs at least one Condition."))
            return error_messages

        def is_reached(self) -> bool:
            """
            True when every stored condition is fulfilled.

            Returns:
                bool: Condition fulfillment, independent of bars / deadlines.
            """
            if len(self.conditions) == 0:
                return False
            return self.conditions.is_fulfilled()

    # endregion
    ##############################

    ###############################
    # region SituationDescription #

    class SituationDescription:
        def __init__(self, description: str | List[str], *conditions: Condition):
            self.description = [description] if isinstance(description, str) else description
            self.conditions = ConditionStorage(*conditions)

        def get_description(self, **kwargs):
            if self.conditions.is_fulfilled(**kwargs):
                return self.description
            return []

    #endregion
    ###############################

    ####################
    # region Situation #

    class Situation:
        def __init__(self, key: str, name: str, *elements: SituationBar | SituationPassive | SituationEventPools | SituationTeaser | SituationThreshold | SituationResolution, thumbnail: str = None):
            self.key = key
            self.name = name
            self.descriptions = []
            self.resolutions = {}
            self.add_resolution(SituationPositiveResolution("ALL"))
            self.bars = {}
            self.bar_weights = None
            self.passives = {}
            self.deadline = None
            self.event_pools = {}
            self.comments = []
            self.teasers = {}
            self.pause_until = None
            self.state = "inactive"
            # Redirect the path into the current mod's folder (base = "" prefix).
            self.thumbnail = get_mod_path(active_mod_key) + thumbnail if thumbnail else thumbnail
            self.thresholds = {}
            self.active_passive = None
            self.active_measure = None
            self.threshold_holds = {}
            self.pictograms = []

            self.invalid = False

            for element in elements:
                if isinstance(element, SituationBar):
                    self.add_bar(element)
                elif isinstance(element, SituationThreshold):
                    self.add_threshold(element)
                elif isinstance(element, SituationResolution):
                    self.add_resolution(element)
                elif isinstance(element, SituationMeasure):
                    self.add_passive(element)
                elif isinstance(element, SituationPassive):
                    self.add_passive(element)
                elif isinstance(element, SituationEventPools):
                    self.add_event_pool(element)
                elif isinstance(element, SituationTeaser):
                    self.add_teaser(element)
                elif isinstance(element, SituationDescription):
                    self.add_description(element)
                elif isinstance(element, Pictogram):
                    self.add_pictogram(element)
            self.update_weights()

        def update_weights(self):
            self.set_bar_weights({key: bar._weight for key, bar in self.bars.items()})
       
            return 

        @property
        def visible(self):
            return self.visibility_state == "active" or self.visibility_state == "teaser_active"

        @property
        def visibility_state(self):
            if self.state == "completed":
                return "completed"
            elif self.state == "active":
                return "active"
            elif any(teaser.active for teaser in self.teasers.values()):
                return "teaser_active"
            else:
                return "inactive"

        def run_self_test(self):
            error_messages = []

            for threshold in self.thresholds.values():
                error_messages.extend(threshold.run_self_test())

            for bar in self.bars.values():
                error_messages.extend(bar.run_self_test())

            if len(self.bars) == 0:
                error_messages.append((790, "No bars provided."))

            for passive in self.passives.values():
                error_messages.extend(passive.run_self_test())

            for event_pool in self.event_pools.values():
                error_messages.extend(event_pool.run_self_test())

            for teaser in self.teasers.values():
                error_messages.extend(teaser.run_self_test())

            for resolution in self.resolutions.values():
                error_messages.extend(resolution.run_self_test())

            # For each bar, collect all thresholds that have a bound for this bar.
            # Then, sort these thresholds in ascending order based on their bound value for this bar.
            # Next, for each consecutive pair of thresholds, check for all bounds they share:
            # If the difference (delta) between their bounds changes sign (i.e., from positive to negative or vice versa),
            # this indicates an inconsistent (non-monotonic) order of threshold bounds for that bar, which will be reported as an error.
            for bar_key, bar in self.bars.items():
                thresholds_with_bar = [threshold for threshold in self.thresholds.values() if bar_key in threshold.bounds]
                # Sort thresholds by bound for this bar (ascending)
                thresholds_with_bar_sorted = sorted(thresholds_with_bar, key=lambda x: x.bounds[bar_key])
                for i in range(len(thresholds_with_bar_sorted) - 1):
                    threshold_1 = thresholds_with_bar_sorted[i]
                    threshold_2 = thresholds_with_bar_sorted[i + 1]
                    direction = 0
                    for bar_key_2, value_1 in threshold_1.bounds.items():
                        # Only check bars that both thresholds have bounds for
                        if bar_key_2 not in threshold_2.bounds:
                            continue
                        delta = threshold_2.bounds[bar_key_2] - value_1
                        # Skip if the value does not change
                        if delta == 0:
                            continue
                        # Set the initial direction
                        if direction == 0:
                            direction = delta
                        # If the sign of the delta changes, report an error
                        elif delta * direction < 0:
                            error_messages.append((
                                791,
                                f"Sign change in threshold bounds on bar '{bar_key_2}' "
                                f"between {threshold_1.key} and {threshold_2.key} "
                                f"(ordered by '{bar_key}')."
                            ))

            if self.key is None or self.key == "":
                error_messages.append((792, "Key is empty. Has to be a non-empty string."))
            if self.name is None or self.name == "":
                error_messages.append((793, "Name is empty. Has to be a non-empty string."))

            for bar_weight_key in self.bar_weights.keys():
                if bar_weight_key not in self.bars.keys():
                    error_messages.append((796, f"Bar weight key '{bar_weight_key}' not found in bars."))
       

            return error_messages

        def update_data(self, situation: Situation):
            self.key = situation.key
            self.name = situation.name
            self.descriptions = situation.descriptions
            self.deadline = situation.deadline
            self.comments = situation.comments
            self.thumbnail = situation.thumbnail
            self.bar_weights = situation.bar_weights
            self.pictograms = situation.pictograms

            if not hasattr(self, "active_passive"):
                self.active_passive = None
            if not hasattr(self, "active_measure"):
                self.active_measure = None
            if not hasattr(self, "threshold_holds"):
                self.threshold_holds = {}
            if not hasattr(self, "invalid"):
                self.invalid = False

            previous_active = self.active_passive
            previous_measure = self.active_measure
            if previous_active in self.passives:
                self.passives[previous_active].revert_effects()
            if previous_measure in self.passives:
                self.passives[previous_measure].revert_effects()
            # Dropped modifiers stay in lifecycle_registry until wave sweep;
            # re-applied ones track/ping KEEP during this check wave.
            for passive in self.passives.values():
                passive.detach_effects()

            # Sync resolutions (keep runtime grace state; refresh definition from template)
            for key, resolution in situation.resolutions.items():
                if key in self.resolutions:
                    self.resolutions[key].update_data(resolution)
                    self.resolutions[key].bind_situation(self)
                else:
                    self.add_resolution(resolution)

            # Sync bars with situation's bars
            new_keys = set(situation.bars.keys())
            for key in new_keys:
                if key in self.bars:
                    self.bars[key].update_data(situation.bars[key])
                else:
                    self.add_bar(situation.bars[key])
            for key in list(self.bars.keys()):
                if key not in new_keys:
                    self.bars[key].revert_decrease_modifier()
                    del self.bars[key]

            # Sync thresholds with situation's thresholds
            new_keys = set(situation.thresholds.keys())
            for key in new_keys:
                if key in self.thresholds:
                    self.thresholds[key].update_data(situation.thresholds[key])
                else:
                    self.add_threshold(situation.thresholds[key])
            for key in list(self.thresholds.keys()):
                if key not in new_keys:
                    del self.thresholds[key]

            # Sync passives with situation's passives
            new_keys = set(situation.passives.keys())
            for key in new_keys:
                if key in self.passives:
                    self.passives[key].update_data(situation.passives[key])
                else:
                    self.add_passive(situation.passives[key])

            for key in list(self.passives.keys()):
                if key not in new_keys:
                    del self.passives[key]

            # Restore active passive / measure after definition sync
            target_passive = previous_active if previous_active in self.passives else None
            target_measure = previous_measure if previous_measure in self.passives else None

            self.active_passive = target_passive
            self.active_measure = target_measure
            if self.state == "active":
                if target_passive is not None:
                    self.set_passive(target_passive, skip_clear=True)
                if target_measure is not None:
                    self.set_measure(target_measure, skip_clear=True)
                for bar in self.bars.values():
                    bar.sync_decrease_modifier()

            # Sync event pools with situation's event pools
            new_keys = set(situation.event_pools.keys())
            for key in new_keys:
                if key in self.event_pools:
                    self.event_pools[key].update_data(situation.event_pools[key])
                else:
                    self.add_event_pool(situation.event_pools[key])
            for key in list(self.event_pools.keys()):
                if key not in new_keys:
                    del self.event_pools[key]

            # Sync teasers with situation's teasers (preserve active state via update_data)
            new_keys = set(situation.teasers.keys())
            for key in new_keys:
                if key in self.teasers:
                    self.teasers[key].update_data(situation.teasers[key])
                else:
                    self.add_teaser(situation.teasers[key])
            for key in list(self.teasers.keys()):
                if key not in new_keys:
                    del self.teasers[key]

        def activate(self):
            self.state = "active"
            if self.active_passive in self.passives:
                self.set_passive(self.active_passive, skip_clear=True)
            if self.active_measure in self.passives:
                self.set_measure(self.active_measure, skip_clear=True)
            for bar in self.bars.values():
                bar.activate()
            return self

        def complete(self):
            if self.active_passive in self.passives:
                self.passives[self.active_passive].deactivate()
            if self.active_measure in self.passives:
                self.passives[self.active_measure].deactivate()
            for bar in self.bars.values():
                bar.revert_decrease_modifier()
                bar.reset_start_application()
            self.clear_tracked_modifiers()
            for passive in self.passives.values():
                passive.detach_effects()
            self.active_passive = None
            self.active_measure = None
            self.state = "completed"

        def cancel(self):
            """
            Abort the situation and clear owned runtime resources.

            Also drops a pending PTA ``voteProposal`` when it points at this situation.
            """
            self.state = "cancelled"
            if self.active_passive in self.passives:
                self.passives[self.active_passive].deactivate()
            if self.active_measure in self.passives:
                self.passives[self.active_measure].deactivate()
            for bar in self.bars.values():
                bar.revert_decrease_modifier()
            self.clear_tracked_modifiers()
            for passive in self.passives.values():
                passive.detach_effects()
            self.active_passive = None
            self.active_measure = None

            proposal = get_game_data("voteProposal")
            if proposal is self or (getattr(proposal, "key", None) == self.key):
                if isinstance(proposal, Unlockable):
                    proposal.release_vote_money()
                set_game_data("voteProposal", None)
            return self

        def add_pictogram(self, pictogram: Pictogram | str):
            pictogram_key = pictogram.key if isinstance(pictogram, Pictogram) else pictogram
            if (
                pictogram_manager is not None
                and pictogram_manager.has_pictogram(pictogram_key)
                and pictogram_key not in self.pictograms
            ):
                self.pictograms.append(pictogram_key)
            return self

        def get_pictogram_values(self) -> Dict[str, Any]:
            return {
                "visibility_state": self.visibility_state,
                "active_passive": self.active_passive if self.active_passive else "",
                "active_measure": self.active_measure if self.active_measure else "",
                "combined_bar_value": self.get_combined_bar_value(),
                "combined_bar_tendency": self.get_combined_bar_tendency(),
                "combined_bar_area": self.get_combined_bar_value_area(),
                "combined_bar_mood": self.get_combined_bar_value_mood(),
            }

        def get_combined_bar_value_area(self) -> int:
            return get_bar_value_area(self.get_combined_bar_min(), self.get_combined_bar_max(), self.get_combined_bar_value())

        def get_combined_bar_value_mood(self) -> str:
            return get_bar_value_mood(
                self.get_combined_bar_value_area(),
                self.get_combined_bar_min(),
                self.get_combined_bar_max(),
            )

        def get_pictogram_data(self) -> Dict[str, Dict[str, Any]]:
            output = {}

            for bar in self.bars.values():
                update_dict(output, bar.get_pictogram_data())

            if pictogram_manager is None:
                return output

            for pictogram in self.pictograms:
                values = self.get_pictogram_values()
                pictogram_label = pictogram_manager.get_label(pictogram, **values)
                pictogram_tooltip = pictogram_manager.get_tooltip(pictogram, **values)
                pictogram_icon = pictogram_manager.get_icon(pictogram, **values)
                if pictogram_icon is not None:
                    output[self.key + ":" + pictogram] = {
                        "key": pictogram,
                        "label": pictogram_label,
                        "tooltip": pictogram_tooltip,
                        "icon": pictogram_icon,
                    }
            return output

        def set_bar_weights(self, weights: Dict[str, float]):
            # Normalize weights so that their sum is 1.0
            total = sum(weights.values())
            if total != 0:
                for key in weights:
                    weights[key] = weights[key] / total
            self.bar_weights = weights
            return self
   
        def add_comments(self, *comments: str):
            self.comments.extend(comments)
            return self

        def add_description(self, description: SituationDescription):
            self.descriptions.append(description)
            return self

        def add_threshold(self, threshold: SituationThreshold):
            threshold.situation = self
            self.thresholds[threshold.key] = threshold
            return self

        def add_deadline(self, deadline: Time):
            self.deadline = deadline
            return self

        def add_resolution(self, resolution: SituationResolution):
            resolution.bind_situation(self)
            self.resolutions[resolution.key] = resolution
            return self

        def should_block_negative_delta(self) -> bool:
            """True while positive resolution is reached and delta_lock is enabled."""
            resolution = self.resolutions.get("positive_resolution")
            if resolution is None or not isinstance(resolution, SituationPositiveResolution):
                return False
            return resolution.delta_lock and resolution.is_reached()

        def check_resolutions(self, **kwargs) -> bool:
            """
            Evaluate all resolutions (reach + grace/gates). Stops after first fire.

            Returns:
                bool: True if a resolution fired and the situation completed.
            """
            if self.state != "active":
                return False
            for resolution in self.resolutions.values():
                if resolution.evaluate(**kwargs):
                    return True
            return False

        def try_resolution(self, key: str, **kwargs) -> bool:
            """Evaluate a single named resolution."""
            if self.state != "active" or key not in self.resolutions:
                return False
            return self.resolutions[key].evaluate(**kwargs)

        def apply_progress_change(self, key: str, value: float):
            self.change_bar_value(key, value)

        def load_thumbnail(self, **kwargs):
            refined_thumbnail = refine_image(self.thumbnail, **kwargs)
            if refined_thumbnail is not None:
                return refined_thumbnail
            return None

        def get_current_thumbnail(self, **kwargs):
            thumbnail_out = self.load_thumbnail()
            combined = self.get_combined_bar_value()
            closest = None
            closest_dist = None
            for threshold in self.thresholds.values():
                if threshold.thumbnail is None:
                    continue
                pos = self.get_combined_threshold_value(threshold)
                dist = abs(pos - combined)
                if closest_dist is None or dist < closest_dist:
                    closest = threshold
                    closest_dist = dist
            if closest is not None:
                closest_thumbnail = closest.load_thumbnail(**kwargs)
                if closest_thumbnail is not None:
                    thumbnail_out = closest_thumbnail
            if thumbnail_out == None:
                thubmnail_out = "images/journal/empty_image.webp"
            return thumbnail_out

        def get_descriptions(self, **kwargs):
            descriptions_out = []
            for description in self.descriptions:
                descriptions_out.extend(description.get_description(**kwargs))
            return descriptions_out

        ##################
        # region Teasers #

        def add_teaser(self, teaser: SituationTeaser):
            teaser.situation = self
            self.teasers[teaser.key] = teaser
            return self

        def check_teasers(self, **kwargs):
            for teaser in self.teasers.values():
                if teaser.active:
                    continue
                if teaser.check_conditions(**kwargs):
                    teaser.activate(**kwargs)
            return self

        def get_active_teasers(self):
            return sorted([teaser for teaser in self.teasers.values() if teaser.active], key=lambda x: x.activation_order)

        # endregion
        ##################

        ################
        # region Pools #

        def check_pool(self, pool_key: str):
            if pool_key not in self.event_pools.keys():
                return False
            return self.event_pools[pool_key].check_pool()

        def add_event_pool(self, event_pool: SituationEventPools):
            event_pool.situation = self
            self.event_pools[event_pool.key] = event_pool
            return self

        # endregion
        ################

        ####################
        # region Passsives #

        def add_passive(self, passive: SituationPassive):
            passive.bind_situation(self)
            self.passives[passive.name] = passive
            return self

        def set_passive(self, passive_key: str, skip_clear: bool = False):
            """
            Activate a lasting passive. Replaces any previously active passive.
            Selecting the already-active passive deactivates it (toggle off).
            Does not touch the active measure slot.

            Args:
                passive_key (str): Key/name of the passive to activate.
                skip_clear (bool): If True, skip deactivate of the previous passive
                    and do not toggle off when re-selecting the same key.

            Returns:
                bool: True if the passive was activated or toggled off.
            """
            if passive_key not in self.passives:
                return False
            target = self.passives[passive_key]
            if target.type == "measure":
                return self.set_measure(passive_key, skip_clear=skip_clear)

            # Re-select active passive → deactivate (player toggle)
            if not skip_clear and self.active_passive == passive_key and target.active:
                target.deactivate()
                target.detach_effects()
                self.active_passive = None
                return True

            if not skip_clear and self.active_passive in self.passives:
                previous = self.passives[self.active_passive]
                previous.deactivate()
                previous.detach_effects()

            self.active_passive = passive_key
            target.activate()
            return True

        def set_measure(self, measure_key: str, skip_clear: bool = False):
            """
            Activate a temporary measure. Does not touch the active passive slot.
            A new measure cannot be started while another is still active; wait for expiry.

            Args:
                measure_key (str): Key/name of the measure to activate.
                skip_clear (bool): If True, skip availability checks and re-apply only
                    lasting effects (no instant/counter/timer side effects).

            Returns:
                bool: True if the measure was activated.
            """
            if measure_key not in self.passives:
                return False
            target = self.passives[measure_key]
            if target.type != "measure":
                return False

            if skip_clear:
                self.active_measure = measure_key
                target.active = True
                target.run_effects()
                return True

            # Block replacement — only duration expiry (deactivate) frees the slot
            if self.active_measure is not None:
                return False

            if not target.check_available():
                return False

            self.active_measure = measure_key
            target.activate()
            return True

        def get_passives(self, type: str = None):
            if type is not None:
                return sorted([passive for passive in self.passives.values() if passive.type == type], key=lambda x: x.name)
            return sorted([passive for passive in self.passives.values()], key=lambda x: x.name)

        def get_passive(self, key: str):
            if key not in self.passives.keys():
                if self.active_passive is None:
                    return None
                return self.passives.get(self.active_passive)
            return self.passives[key]

        def get_measure(self, key: str = None):
            if key is None:
                if self.active_measure is None:
                    return None
                return self.passives.get(self.active_measure)
            return self.passives.get(key)

        def check_passives(self, **kwargs):
            if self.active_passive in self.passives:
                self.passives[self.active_passive].check(**kwargs)
            if self.active_measure in self.passives:
                self.passives[self.active_measure].check(**kwargs)
        
        def track_modifier(self, key: str, stat: str, collection: str, op: str = "+", value=0):
            """
            Record a modifier owned by this situation in the global lifecycle registry.

            Args:
                key (str): Modifier key.
                stat (str): Stat the modifier applies to.
                collection (str): Modifier collection name.
                op (str): Modifier operation (+, *, value_percent, range_percent, gated_percent).
                value: Modifier value (needed for hibernate resume).
            """
            lifecycle_registry.track(
                key,
                owner="situations",
                category=self.key,
                kind="modifier",
                stat=stat,
                collection=collection,
                op=op,
                value=value,
            )

        def untrack_and_remove(self, key: str):
            """
            Remove a tracked modifier from the global modifier system and registry.

            Args:
                key (str): Modifier key.
            """
            lifecycle_registry.ping(key, REMOVE)

        def clear_tracked_modifiers(self):
            """Remove all modifiers tracked by this situation."""
            lifecycle_registry.clear(owner="situations", category=self.key)



        # endregion
        ####################

        ################
        # region Holds #

        def add_threshold_hold(self, threshold: SituationThreshold, hold: int):
            self.threshold_holds[threshold.key] = hold
            return self

        def release_threshold_hold(self, threshold_key: str):
            if threshold_key not in self.threshold_holds.keys():
                return
            del self.threshold_holds[threshold_key]
            return self

        def check_threshold_holds(self):
            for threshold_key in list(self.threshold_holds.keys()):
                threshold = self.thresholds[threshold_key]
                for bar_key in threshold.bounds.keys():
                    bar = self.bars[bar_key]
                    if not bar.check_threshold_hold(threshold):
                        break
                else:
                    threshold.release_hold()

        # endregion
        ################

        ###############
        # region Bars #

        def get_bar_weights(self):
            if self.bar_weights == None:
                bars_amount = len(self.bars.keys())
                return {key: 1 / bars_amount for key in self.bars.keys()}
            return self.bar_weights

        def get_combined_bar_min(self) -> float:
            output = 0.0
            weights = self.get_bar_weights()
            for key, bar in self.bars.items():
                output += bar.min * weights[key]
            return output

        def get_combined_bar_max(self) -> float:
            output = 0.0
            weights = self.get_bar_weights()
            for key, bar in self.bars.items():
                output += bar.max * weights[key]
            return output

        def get_combined_bar_value(self) -> float:
            output = 0.0
            weights = self.get_bar_weights()
            for key, bar in self.bars.items():
                output += bar.value * weights[key]
            return output

        def change_bar_value(self, bar_key: str, delta: float):
            if bar_key == "ALL":
                for bar in self.bars.values():
                    bar.change_value(delta)
                return
            if bar_key not in self.bars.keys():
                return
            self.bars[bar_key].change_value(delta)

            self.check_threshold_holds()

        def get_full_bar_range(self, bar_key: str):
            if bar_key == "ALL":
                return {bar.key: bar.get_full_range() for bar in self.bars.values()}
            if bar_key not in self.bars.keys():
                return
            return {bar_key: bar.get_full_range()}

        def get_gated_bar_range(self, bar_key: str, modifier_value: float):
            if bar_key == "ALL":
                return {bar.key: bar.get_gated_range(modifier_value) for bar in self.bars.values()}
            if bar_key not in self.bars.keys():
                return
            return {bar_key: bar.get_gated_range(modifier_value)}

        def get_combined_bar_tendency(self) -> int:
            """
            Direction of the weighted combined bar from recent changes.

            Returns:
                int: 1 if positive, -1 if negative, 0 if neutral / no history.
            """
            output = 0.0
            weights = self.get_bar_weights()
            for key, bar in self.bars.items():
                output += bar.tendency * weights[key]
            if output > 0:
                return 1
            if output < 0:
                return -1
            return 0

        def change_bar_values_via_stats(self, key: str, delta: float):
            for bar in self.bars.values():
                bar.change_value_via_stats(key, delta)

            self.check_threshold_holds()

        def add_bar(self, bar: SituationBar):
            bar.situation = self
            self.bars[bar.key] = bar
            return self

        def get_bar(self, key: str):
            if key not in self.bars.keys():
                return None
            return self.bars[key]

        def get_bars(self):
            return self.bars.values()

        def add_start_modifier(self, bar_key: str, modifier: Modifier_Obj | SituationStartModifier, stat: str = None):
            """
            Add an authored start modifier to a bar (validated on registration).

            Args:
                bar_key (str): Target bar key.
                modifier (Modifier_Obj | SituationStartModifier): Operator/value payload.
                stat (str, optional): School-stat key for snapshot contribution.

            Returns:
                bool: True if stored on the bar.
            """
            bar = self.get_bar(bar_key)
            if bar is None:
                log(f"Cannot add start modifier: bar '{bar_key}' not found on situation '{self.key}'.", log_type="error", category="situation")
                return False
            return bar.add_start_modifier(modifier, stat)

        def shift_start_value(self, bar_key: str, op: str, value: float, name: str = None, stat: str = None):
            """
            Runtime start-value shift (events before activation). Survives definition sync.
            Builds the Modifier_Obj internally and validates at registration time.

            Args:
                bar_key (str): Target bar key.
                op (str): ``+``, ``*``, ``value_percent``, ``range_percent`` or ``gated_percent``.
                value (float): Operand (flat, factor, percent, or stat weight).
                name (str, optional): Modifier identity. Auto-generated if omitted.
                stat (str, optional): School-stat key for snapshot contribution.

            Returns:
                bool: True if the bar existed and the shift was stored.
            """
            bar = self.get_bar(bar_key)
            if bar is None:
                log(f"Cannot shift start value: bar '{bar_key}' not found on situation '{self.key}'.", log_type="error", category="situation")
                return False
            return bar.add_start_shift(op, value, name=name, stat=stat)

        # endregion
        ###############

        #####################
        # region Thresholds #

        def get_combined_threshold_value(self, threshold: SituationThreshold):
            output = 0.0
            weights = self.get_bar_weights()
            for key, bar in self.bars.items():
                if key in threshold.bounds.keys():
                    output += threshold.bounds[key] * weights[key]
                else:
                    output += bar.value * weights[key]
            return output

        def get_next_blocking_thresholds(self, direction: float, include_reached: bool = False):
            output = {key: None for key in self.bars.keys()}
            for threshold in self.thresholds.values():
                if (not include_reached and threshold.reached) or \
                    (threshold.hold != -1) or \
                    not threshold.is_blocking():
                    continue
                for key, value in threshold.bounds.items():
                    bar_value = self.bars[key].value
                    if direction > 0 and value > bar_value and (output[key] == None or output[key].bounds[key] > value):
                        output[key] = threshold
                    elif direction < 0 and value < bar_value and (output[key] == None or output[key].bounds[key] < value):
                        output[key] = threshold

            return output

        def get_closest_next_blocking_threshold(self, origin: float, direction: float, include_reached: bool = False):
            thresholds = self.get_next_blocking_thresholds(direction, include_reached)
            if len(thresholds.keys()) == 0:
                return None
            # Get the threshold (blocking) with a combined value closest to origin.
            closest_threshold = None
            closest_dist = None
            for threshold in self.thresholds.values():
                if threshold.reached or \
                    threshold.hold != -1 or \
                    not threshold.is_blocking():
                    continue
                combined_value = self.get_combined_threshold_value(threshold)
                dist = abs(combined_value - origin)
                if closest_threshold is None or dist < closest_dist:
                    closest_threshold = threshold
                    closest_dist = dist
            return closest_threshold
   

        def get_thresholds_in_range(self, origin: float, bar_key: str, range: float, direction: float, stop_at_blocking: bool = True, include_auto: bool = True, include_reached: bool = False):
            blocking = None
            output = []
            thresholds = sorted(
                (t for t in self.thresholds.values() if bar_key in t.bounds),
                key=lambda t: t.bounds[bar_key],
                reverse=(direction < 0),
            )
       
            for threshold in thresholds:
                if (not include_auto and not threshold.is_blocking()) or \
                    (direction * threshold.direction <= 0) or \
                    (not include_reached and threshold.reached) or \
                    (threshold.hold != -1):
                    continue

                bound = threshold.bounds[bar_key]
                if (direction > 0 and bound < origin) or (direction < 0 and bound > origin):
                    continue

                if (direction > 0 and bound > origin + range) or (direction < 0 and bound < origin - range):
                    break

                output.append(threshold)

                if stop_at_blocking and threshold.is_blocking():
                    blocking = threshold
                    break
                
            return output, blocking

        def get_thresholds_in_direction_for_all_bars(
            self,
            direction: int,
            stop_at_blocking: bool = True,
            include_auto: bool = True,
            include_reached: bool = False,
        ):
            """
            Unique thresholds ahead in the given direction for every bar.

            Collects per bar up to the next blocking threshold (inclusive), then
            sorts by distance of each threshold's combined value to the combined
            bar value (closest first).

            Args:
                direction (int): Search direction, 1 or -1.
                stop_at_blocking (bool): Stop at the first blocking threshold per bar.
                include_auto (bool): Include auto-fire thresholds.
                include_reached (bool): Include already reached thresholds.

            Returns:
                list: Unique SituationThresholds, closest combined value first.
            """
            thresholds_set = set()
            for bar_key, bar in self.bars.items():
                origin = bar.value
                thresholds_sorted = sorted(
                    (t for t in self.thresholds.values() if bar_key in t.bounds),
                    key=lambda t: t.bounds[bar_key],
                    reverse=(direction < 0),
                )

                for threshold in thresholds_sorted:
                    if (not include_auto and not threshold.is_blocking()) or \
                        (direction * threshold.direction <= 0) or \
                        (not include_reached and threshold.reached) or \
                        (threshold.hold != -1):
                        continue

                    bound = threshold.bounds[bar_key]
                    if (direction > 0 and bound < origin) or (direction < 0 and bound > origin):
                        continue

                    thresholds_set.add(threshold)

                    if stop_at_blocking and threshold.is_blocking():
                        break

            combined = self.get_combined_bar_value()
            return sorted(
                thresholds_set,
                key=lambda t: abs(self.get_combined_threshold_value(t) - combined),
            )

        def get_hints(self):
            """
            Journal hint texts for the current bar tendency.

            Uses positive direction when tendency is neutral. For each threshold,
            shows threshold_hint when bar values are reached, otherwise approach_hint.

            Returns:
                list: Hint strings, closest combined threshold first. Empty hints omitted.
            """
            direction = self.get_combined_bar_tendency()
            if direction == 0:
                direction = 1

            hints = []
            for threshold in self.get_thresholds_in_direction_for_all_bars(direction):
                if threshold.is_bar_values_reached():
                    hint = threshold.threshold_hint
                else:
                    hint = threshold.approach_hint
                if hint:
                    hints.append(hint)
            return hints

        def is_threshold_reached(self, threshold_key: str):
            threshold = self.thresholds.get(threshold_key)
            if threshold is None:
                return False
            return threshold.is_reached()

        # endregion
        #####################

    #endregion
    ####################

    ###########################
    # region SituationManager #

    class SituationManager:
        def __init__(self):
            self._situations = {}
            self.threshold_checks = {}
            # Rules: ("situation", key|"*"), ("stat", key|"*"), ("pair", situation, stat)
            self._progress_blocks = set()
            self._loaded_this_wave = set()
            # Cascading resolution breather (pauses base wear after negative resolve)
            self.resolution_breather_days = 0
            self.resolution_breather_active = False

        def begin_situation_load_wave(self):
            """
            Clear the per-wave registration set before definitions load.

            Safe for old saves that lack ``_loaded_this_wave``.
            """
            self._loaded_this_wave = set()

        def _ensure_loaded_this_wave(self):
            if not hasattr(self, "_loaded_this_wave") or self._loaded_this_wave is None:
                self._loaded_this_wave = set()

        def load_situation(self, situation: Situation):
            """
            Insert or sync a situation definition for this load wave.

            Revive order when previously invalid: update_data → uninvalidate →
            resume_category → re-announce pending threshold checks.
            """
            self._ensure_loaded_this_wave()
            self._loaded_this_wave.add(situation.key)

            live = self._situations.get(situation.key)
            was_invalid = bool(live is not None and getattr(live, "invalid", False))

            if live is not None:
                live.update_data(situation)
            else:
                self._situations[situation.key] = situation
                live = situation

            error_messages = live.run_self_test()
            if len(error_messages) > 0:
                for error_message in error_messages:
                    log(error_message[1], log_type="error", category="situation")
                self.invalidate_situation(live)
                return self

            if was_invalid:
                self.uninvalidate_situation(live)
                lifecycle_registry.resume_category("situations", live.key)

            self._reannounce_threshold_checks(live.key)
            return self

        def _reannounce_threshold_checks(self, situation_key: str):
            """
            Re-track pending threshold checks for a live situation in this wave.

            Keeps ACTIVE entries pinged so finalize_check does not sweep them.
            Does not restart timers (unlike hibernate→resume).

            A check whose threshold no longer exists in the reloaded definition
            (threshold removed on a live reload) is dropped instead of kept alive,
            mirroring the resume path (_resume_resource → REMOVE).
            """
            situation = self._situations.get(situation_key)
            prefix = "situation:" + situation_key + ":"
            for check_key, threshold in list(self.threshold_checks.items()):
                belongs = False
                if getattr(threshold, "situation", None) is not None and threshold.situation.key == situation_key:
                    belongs = True
                elif check_key.startswith(prefix):
                    belongs = True
                if not belongs:
                    continue
                if situation is None or check_key not in situation.thresholds:
                    del self.threshold_checks[check_key]
                    remove_timer(check_key)
                    lifecycle_registry.ping(check_key, REMOVE)
                    continue
                lifecycle_registry.track(
                    check_key,
                    "situations",
                    situation_key,
                    "threshold_check",
                )

        def invalidate_situation(self, situation: Situation):
            self._situations[situation.key].invalid = True
            # Keep modifiers / threshold_check meta while definition is temporarily broken.
            lifecycle_registry.hibernate_category("situations", situation.key)

        def uninvalidate_situation(self, situation: Situation):
            self._situations[situation.key].invalid = False

        def reconcile_orphan_situations(self):
            """
            Soft-invalidate situations present in the save but not re-registered
            in this load wave. Preserves runtime state for a possible definition return.
            """
            if situation_manager is None:
                return
            self._ensure_loaded_this_wave()
            loaded = self._loaded_this_wave
            for key in list(self._situations.keys()):
                if key in loaded:
                    continue
                situation = self._situations[key]
                log(
                    f"Situation '{key}' has no definition in this load wave "
                    f"(mod removed/deactivated or key renamed) → invalidated, "
                    f"save state kept for possible return.",
                    log_type="info",
                    category="situation",
                )
                self.invalidate_situation(situation)

                # Legacy threshold_checks without registry entries.
                prefix = "situation:" + key + ":"
                for check_key, threshold in list(self.threshold_checks.items()):
                    belongs = False
                    if getattr(threshold, "situation", None) is not None and threshold.situation.key == key:
                        belongs = True
                    elif check_key.startswith(prefix):
                        belongs = True
                    if belongs and not lifecycle_registry.has(check_key):
                        del self.threshold_checks[check_key]
                        remove_timer(check_key)

                # Drop progress blocks referencing this situation.
                to_drop = set()
                for rule in self._progress_blocks:
                    if len(rule) >= 2 and rule[0] == "situation" and rule[1] == key:
                        to_drop.add(rule)
                    elif len(rule) >= 2 and rule[0] == "pair" and rule[1] == key:
                        to_drop.add(rule)
                self._progress_blocks.difference_update(to_drop)

                proposal = get_game_data("voteProposal")
                if proposal is situation or (getattr(proposal, "key", None) == key):
                    if isinstance(proposal, Unlockable):
                        proposal.release_vote_money()
                    set_game_data("voteProposal", None)

        def get_pictogram_data(self, situation_key: str) -> Dict[str, Dict[str, Any]]:
            situation = self.get_situation(situation_key)
            if situation is None:
                return {}
            return situation.get_pictogram_data()

        def add_pictogram(self, situation_key: str, pictogram: Pictogram | str):
            situation = self.get_situation(situation_key)
            if situation is None:
                return
            if isinstance(pictogram, str):
                pictogram = pictogram_manager.get_pictogram(pictogram)
            if pictogram is None:
                return
            situation.add_pictogram(pictogram)
            return

        def get_situations(self, include_invalid: bool = False):
            if include_invalid:
                return list(self._situations.values())
            return [situation for situation in self._situations.values() if not situation.invalid]

        def get_situation(self, key: str):
            if key not in self._situations.keys() or self._situations[key].invalid:
                return None
            return self._situations[key]

        def get_completed_situations(self):
            return [situation for situation in self._situations.values() if situation.state == "completed" and not situation.invalid]

        def get_visible_situations(self, include_completed: bool = False):
            return [situation for situation in self._situations.values() if (situation.visible or (include_completed and situation.state == "completed")) and not situation.invalid]

        def get_visible_teaser_titles(self, *situations: Situation, tab: str = ""):
            out = []
            for situation in situations:
                key = situation.key
                if tab != "":
                    key = f"{key}:{tab}"
                if situation.visibility_state == "active" or situation.state == "completed":
                    out.append((situation.name, key))
                elif situation.visibility_state == "teaser_active":
                    out.append(("????????", key))
            return out

        def count_active_situations(self) -> int:
            """
            Count live situations currently in the active state.

            Returns:
                int: Number of non-invalid situations with state ``active``.
            """
            return sum(
                1
                for situation in self.get_situations()
                if situation.state == "active"
            )

        def is_resolution_breather_active(self) -> bool:
            """
            Whether base wear is paused after a negative resolution.

            Returns:
                bool: True while the cascading resolution breather is active.
            """
            return bool(getattr(self, "resolution_breather_active", False))

        def get_resolution_breather_display_days(self) -> int:
            """
            Remaining breather duration for journal display.

            While the counter is positive, return it. On the final inclusive day
            (active but counter already 0) return 1 so the UI still shows one day.

            Returns:
                int: Days remaining to show, or 0 when inactive.
            """
            if not self.is_resolution_breather_active():
                return 0
            days = getattr(self, "resolution_breather_days", 0) or 0
            return days if days > 0 else 1

        def trigger_resolution_breather(self):
            """
            Start or refresh the cascading resolution breather.

            Duration is ``min(4, remaining active situations)`` after the failed
            situation has already completed. Extension uses max, never sum.
            """
            new_days = min(4, self.count_active_situations())
            if new_days <= 0:
                return

            was_active = self.is_resolution_breather_active()
            old_days = getattr(self, "resolution_breather_days", 0) or 0
            self.resolution_breather_days = max(old_days, new_days)
            self.resolution_breather_active = True
            if not was_active:
                self._suspend_all_decrease_modifiers()

        def tick_resolution_breather(self):
            """
            Advance the breather on day-change (check before decrement).

            If the counter is still positive, the pause continues and the counter
            decrements. If it is already 0 while active, the pause ends and base
            wear resumes. Daytime-change must not call this.
            """
            if not self.is_resolution_breather_active():
                return

            days = getattr(self, "resolution_breather_days", 0) or 0
            if days > 0:
                self.resolution_breather_days = days - 1
            else:
                self.resolution_breather_active = False
                self.resolution_breather_days = 0
                self._resume_all_decrease_modifiers()

        def _suspend_all_decrease_modifiers(self):
            """Remove base-wear decrease modifiers from all active situation bars."""
            for situation in self.get_situations():
                if situation.state != "active":
                    continue
                for bar in situation.bars.values():
                    bar.revert_decrease_modifier()

        def _resume_all_decrease_modifiers(self):
            """Re-apply base-wear decrease modifiers on all active situation bars."""
            for situation in self.get_situations():
                if situation.state != "active":
                    continue
                for bar in situation.bars.values():
                    bar.apply_decrease_modifier()

        def check_pool(self, situation_key: str, pool_key: str, **kwargs):
            situation = self.get_situation(situation_key)
            if situation is None:
                return False
            return situation.check_pool(pool_key, **kwargs)

        def check_passives(self, **kwargs):
            for situation in self.get_situations():
                situation.check_passives(**kwargs)

        def check_teasers(self, **kwargs):
            """
            Evaluate Chronicle Teasers for all situations.

            The event system always passes `event_name` context into end-of-event
            checks. For teaser conditions that reference *specific* event keys,
            we must evaluate them against the teaser's own event_name parameter,
            not against the currently evaluated event.
            """
            teaser_kwargs = dict(kwargs)
            teaser_kwargs.pop("event_name", None)
            for situation in self.get_situations():
                situation.check_teasers(**teaser_kwargs)

        def check_resolutions(self, **kwargs):
            for situation in self.get_situations():
                if situation.state != "active":
                    continue
                if situation.check_resolutions(**kwargs):
                    return True
            return False

        def shift_start_value(self, situation_key: str, bar_key: str, op: str, value: float, name: str = None, stat: str = None):
            """
            Runtime start-value shift for a not-yet-resolved bar snapshot.
            Builds the Modifier_Obj internally.

            Args:
                situation_key (str): Situation key.
                bar_key (str): Bar key within the situation.
                op (str): ``+``, ``*``, ``value_percent``, ``range_percent`` or ``gated_percent``.
                value (float): Operand (flat, factor, percent, or stat weight).
                name (str, optional): Modifier identity. Auto-generated if omitted.
                stat (str, optional): School-stat key for snapshot contribution.

            Returns:
                bool: True if stored on the bar.
            """
            situation = self.get_situation(situation_key)
            if situation is None:
                log(f"Cannot shift start value: situation '{situation_key}' not found.", log_type="error", category="situation")
                return False
            return situation.shift_start_value(bar_key, op, value, name=name, stat=stat)

        ###########################
        # region Progress Blocker #

        def _normalize_progress_keys(self, value):
            """
            Normalize block/unblock keys to a list of strings.

            Args:
                value: None, \"all\", a key string, or a list/tuple of keys.

            Returns:
                list: Normalized keys, or empty list if value is None.
            """
            if value is None:
                return []
            if isinstance(value, (list, tuple, set)):
                return [("*" if str(v) == "all" else str(v)) for v in value]
            if value == "all":
                return ["*"]
            return [str(value)]

        def _progress_block_rules(self, situations=None, stats=None):
            """
            Build the rule tuples for the given situation/stat filters.

            Args:
                situations: None, \"all\", str, or list — situation keys to filter.
                stats: None, \"all\", str, or list — stat keys to filter.

            Returns:
                set: Rule tuples to add or remove.
            """
            situation_keys = self._normalize_progress_keys(situations)
            stat_keys = self._normalize_progress_keys(stats)
            rules = set()

            if situation_keys and stat_keys:
                for situation_key in situation_keys:
                    for stat_key in stat_keys:
                        rules.add(("pair", situation_key, stat_key))
            elif situation_keys:
                for situation_key in situation_keys:
                    rules.add(("situation", situation_key))
            elif stat_keys:
                for stat_key in stat_keys:
                    rules.add(("stat", stat_key))

            return rules

        def block_progress(self, situations=None, stats=None):
            """
            Add progress-exclude rules for stat→bar auto updates.

            Only situations / only stats → block that axis.
            Both → block each situation|stat pair.
            Use \"all\" to block every entry on that axis.

            Args:
                situations: None, \"all\", str, or list of situation keys.
                stats: None, \"all\", str, or list of stat keys.

            Returns:
                SituationManager: self for chaining.
            """
            self._progress_blocks.update(self._progress_block_rules(situations, stats))
            return self

        def unblock_progress(self, situations=None, stats=None):
            """
            Remove matching progress-exclude rules. Other rules stay active.

            Args must mirror the block that should be removed.

            Args:
                situations: None, \"all\", str, or list of situation keys.
                stats: None, \"all\", str, or list of stat keys.

            Returns:
                SituationManager: self for chaining.
            """
            self._progress_blocks.difference_update(self._progress_block_rules(situations, stats))
            return self

        def clear_progress_blocks(self):
            """
            Remove all progress-exclude rules (e.g. at end_event).

            Returns:
                SituationManager: self for chaining.
            """
            self._progress_blocks.clear()
            return self

        def is_progress_blocked(self, situation_key: str, stat_key: str) -> bool:
            """
            Check whether auto progress is blocked for a situation and stat.

            Args:
                situation_key (str): Situation key.
                stat_key (str): Stat type key.

            Returns:
                bool: True if the auto update should be skipped.
            """
            blocks = self._progress_blocks
            if ("situation", "*") in blocks or ("situation", situation_key) in blocks:
                return True
            if ("stat", "*") in blocks or ("stat", stat_key) in blocks:
                return True
            if ("pair", "*", "*") in blocks or ("pair", situation_key, "*") in blocks:
                return True
            if ("pair", "*", stat_key) in blocks or ("pair", situation_key, stat_key) in blocks:
                return True
            return False

        # endregion
        ###########################

        ##########################
        # region Progress Change #

        def apply_progress_change_via_stats(self, key: str, delta: float):
            if delta == 0:
                return
            for situation in self.get_situations():
                if situation.state != "active":
                    continue
                if self.is_progress_blocked(situation.key, key):
                    continue
                situation.change_bar_values_via_stats(key, delta)
            return

        def apply_progress_change(self, key: str, value: float):
            parsed = parse_situation_stat_key(key)
            if parsed is None:
                return
            situation_key, bar_key = parsed
            situation = self.get_situation(situation_key)
            if situation is None:
                return
            situation.apply_progress_change(bar_key, value)
            return

        def get_full_range(self, key: str):
            """
            Full available range for a situation bar referenced by a progress key.

            Args:
                key (str): ``situation:<situation_key>:<bar_key>``.

            Returns:
                float: ``max - min`` for the bar, or ``0`` if unresolved.
            """
            parsed = parse_situation_stat_key(key)
            if parsed is None:
                return 0
            situation_key, bar_key = parsed
            situation = self.get_situation(situation_key)
            if situation is None:
                return 0
            bar = situation.get_bar(bar_key)
            if bar is None:
                return 0
            return bar.get_full_range()

        def get_gated_range(self, key: str, modifier_value: float):
            """
            Gated range for a situation bar referenced by a progress key.

            Args:
                key (str): ``situation:<situation_key>:<bar_key>``.
                modifier_value (float): Modifier value whose sign selects the gate.

            Returns:
                float: Gated range size, or ``0`` if unresolved.
            """
            parsed = parse_situation_stat_key(key)
            if parsed is None:
                return 0
            situation_key, bar_key = parsed
            situation = self.get_situation(situation_key)
            if situation is None:
                return 0
            bar = situation.get_bar(bar_key)
            if bar is None:
                return 0
            return bar.get_gated_range(modifier_value)


        # endregion
        ##########################

        #####################
        # region Thresholds #

        def add_threshold_check(self, SituationThreshold: SituationThreshold):
            self.threshold_checks[SituationThreshold.key] = SituationThreshold
            situation_key = SituationThreshold.situation.key if SituationThreshold.situation is not None else ""
            lifecycle_registry.track(
                SituationThreshold.key,
                "situations",
                situation_key,
                "threshold_check",
            )
            return self

        def check_threshold(self, key: str, **kwargs):
            if key not in self.threshold_checks.keys():
                return
            threshold = self.threshold_checks[key]
            if threshold.timed_release is not None:
                if threshold.timed_release.check_condition(**kwargs):
                    threshold.trigger_effects()
                    threshold.set_hold()
                    del self.threshold_checks[key]
                    lifecycle_registry.ping(key, REMOVE)
                elif threshold.blocking.is_fulfilled(**kwargs):
                    threshold.set_hold()
                    del self.threshold_checks[key]
                    lifecycle_registry.ping(key, REMOVE)
            elif threshold.blocking.is_fulfilled(**kwargs):
                threshold.trigger_effects()
                threshold.reached = True
                del self.threshold_checks[key]
                lifecycle_registry.ping(key, REMOVE)

            return

        def check_all_thresholds(self, **kwargs):
            for key in list(self.threshold_checks.keys()):
                self.check_threshold(key, **kwargs)
            return

        def is_threshold_reached(self, situation_key: str, threshold_key: str):
            situation = self.get_situation(situation_key)
            if situation is None:
                return False
            return situation.is_threshold_reached(threshold_key)


        # endregion
        #####################
    # endregion
    ###########################

    ###################################
    # region Definition helpers ----- #
    # Definition helpers — declarative syntax for load_situations authors.
    # Chain methods (add_*, set_*) return self; __init__ must not return self.

    def AutoThreshold(approach_hint, *effects, direction=1, visible_range=100, thumbnail=None, default_hold=5, **bounds):
        """Auto-fire threshold with empty threshold_hint. Bounds via kwargs, e.g. main=10."""
        return SituationThreshold(approach_hint, "", *effects, direction=direction, visible_range=visible_range, thumbnail=thumbnail, default_hold=default_hold).add_bounds(**bounds)

    def BlockingThreshold(approach_hint, threshold_hint, *conditions, direction=1, visible_range=100, thumbnail=None, default_hold=-1, **bounds):
        """
        Blocking threshold — progress stops until a Condition is fulfilled.

        ``default_hold=-1`` (default): no hysteresis; once cleared, stays reached
        and cannot re-arm. Set ``default_hold`` to ``0`` or higher to enable a
        reactivation hysteresis zone. Bounds via kwargs, e.g. main=20.
        """
        return SituationThreshold(approach_hint, threshold_hint, *conditions, direction=direction, visible_range=visible_range, thumbnail=thumbnail, default_hold=default_hold).add_bounds(**bounds)

    def Bar(key, *elements: Pictogram, weight: float = None, limits = (-100, 100), stat_weights = None, regular_decrease_rate: float = 0, regular_decrease_interval: str = "daytime_change", start_base: float = 0, start_modifiers = None):
        """
        Situation bar with limits and optional start-value / wear setup.

        Bar("main",
            limits=(-30, 60),
            stat_weights={HAPPINESS: 0.5},
            regular_decrease_rate=-0.5,
            start_base=-20,
            start_modifiers=[
                StartModifier("+", -5),
                StartModifier("+", 0.05, stat=HAPPINESS),
            ],
        )
        """
        bar = SituationBar(key, regular_decrease_rate, regular_decrease_interval).set_limits(limits[0], limits[1])
        bar.set_start_base(start_base)
        if start_modifiers:
            for entry in start_modifiers:
                bar.add_start_modifier(entry)
        if stat_weights:
            for stat, weight in stat_weights.items():
                bar.add_stat_weight(stat, weight)
        if weight:
            bar.set_weight(weight)
        for element in elements:
            if isinstance(element, Pictogram):
                bar.add_pictogram(element)
        return bar

    def StartModifier(op: str, value: float, name: str = None, stat: str = None):
        """
        Authoring helper for bar start-value modifiers.

        Args:
            op (str): ``+``, ``*``, ``value_percent``, ``range_percent`` or ``gated_percent``.
            value (float): Operand (flat, factor, percent, or stat weight).
            name (str, optional): Modifier identity. Auto-generated if omitted.
            stat (str, optional): School-stat key for snapshot contribution.

        Returns:
            SituationStartModifier: Entry for Bar(..., start_modifiers=[...]).
        """
        if name is None:
            stat_part = stat if stat is not None else "general"
            name = f"start:{stat_part}:{op}:{value}"
        return SituationStartModifier(Modifier_Obj(name, op, value), stat)

    def SituationPool(key, bar_min, bar_max):
        return SituationEventPools(key, bar_min, bar_max)

    def PassiveOption(key, description, *effects):
        return SituationPassive(key, description, *effects)

    def MeasureOption(key, description, duration, *limits, instant=None, permanent=None):
        """
        Temporary measure (Schicht 3).

        Args:
            key: Stable measure id.
            description: Player-facing text.
            duration: TimerCondition for active duration.
            *limits: Cooldown TimerCondition, ManualCounterCondition, and/or other Conditions.
            instant: Optional list of SituationEffect applied once on activate (no revert).
            permanent: List of SituationEffect active for the duration (reverted on end).
        """
        return SituationMeasure(
            key,
            description,
            duration,
            list(limits),
            list(instant or []),
            list(permanent or []),
        )

    def Teaser(key, text, *conditions, interpretation=None, note_type=None, image=None, layout=None):
        """
        Chronicle note / pre-activation teaser.

        Args:
            key: Stable teaser id.
            text: Observation text (supports kwargs interpolation).
            *conditions: Unlock conditions (at least one required).
            interpretation: Optional psychologist reading line.
            note_type: Optional type key: observation|suspicion|insight|setback.
            image: Optional instant-photo pattern path (resolved on activate).
            layout: Optional forced layout id. None = random on activate.
                Text: text_full, text_aside.
                Photo: photo_left, photo_right, photo_top.
        """
        return SituationTeaser(
            key,
            text,
            *conditions,
            interpretation=interpretation,
            note_type=note_type,
            image=image,
            layout=layout,
        )

    def PositiveResolution(mode="ALL", *elements, delta_lock=False):
        """
        Positive end of a situation. mode: ALL | ANY (bars at max).
        *elements: Effect and/or Condition. Conditions enable grace until fulfilled.
        delta_lock: while reached, block negative bar deltas.
        """
        return SituationPositiveResolution(mode, *elements, delta_lock=delta_lock)

    def NegativeResolution(mode="ANY", *elements, grace_count=None):
        """
        Negative end of a situation. mode: ALL | ANY (bars at min).
        *elements: Effect and/or Condition. Conditions enable grace until fulfilled.
        grace_count: optional LatchCounter max (resolution-owned latch).
        """
        return SituationNegativeResolution(mode, *elements, grace_count=grace_count)

    def DeadlineResolution(deadline, *elements):
        """
        Resolution after deadline Time. Optional Conditions delay fire until fulfilled.
        """
        return SituationDeadlineResolution(deadline, *elements)

    def ConditionResolution(key, *elements):
        """
        Resolution that fires when its Conditions are fulfilled, ignoring bars.

        Args:
            key: Unique resolution key on the situation.
            *elements: Condition and/or Effect. Needs at least one of each.
        """
        return SituationConditionResolution(key, *elements)

    def Picto(key):
        if pictogram_manager is None:
            return None
        return pictogram_manager.get_pictogram(key)

    def activate_situation_teaser(situation_key, teaser_key, **kwargs):
        """Manually activate a teaser (e.g. from the Ren'Py console). Does not activate the situation."""
        if situation_manager is None:
            return None
        situation = situation_manager.get_situation(situation_key)
        if situation is None or teaser_key not in situation.teasers:
            return None
        return situation.teasers[teaser_key].activate(**kwargs)

    def register_situations(*situations):
        """Load or update templates. Call from label load_situations.

        Registration is gated on the current mod being active (like event
        `add_event`), so a disabled mod's situations are not registered.
        """
        if is_mod_active(active_mod_key):
            for situation in situations:
                situation_manager.load_situation(situation)

    # endregion Definition helpers ---#
    ###################################


label load_situations:
    $ set_current_mod('base')

    if not situation_manager:
        $ situation_manager = SituationManager()

    $ situation_manager.begin_situation_load_wave()

    $ register_situations(
        Situation("cafeteria_crisis", "Cafeteria Crisis", "The school doesn't have a proper cafeteria. The students have to rely on the expensive snack bar. Adelaide Hall has agreed to help, but she has no experience managing a commercial kitchen. The protagonist must get the cafeteria up and running and support Adelaide.",
            Teaser("kiosk_complaints", "There's a heated discussion about prices at the snack bar. It seems the students are paying double for a regular lunch.", PlaceholderCondition(), interpretation="Money pressure shows first at the lunch counter—everyday friction before anyone calls it a crisis.", note_type="observation"),
            Teaser("abandoned_kitchen", "There's an abandoned building next to the courtyard. A yellowed menu is still stuck to the door—there must have been a kitchen there at one time.", PlaceholderCondition(), interpretation="A leftover function, not a secret. The school already solved this once.", note_type="insight"),
            Teaser("adelaide_offers", "Adelaide Hall has heard rumors about the food problem. She says she'd help—if the school lets her.", PlaceholderCondition(), interpretation="Willingness without mandate. She needs cover more than she needs skill.", note_type="suspicion"),
            Teaser("snack_line_photo", "I snapped a quick note of the snack-bar queue at peak hour. Same crowd, same complaints, same overpriced trays.", PlaceholderCondition(), interpretation="A repeating scene is data. The problem is structural, not a bad day.", note_type="observation", image="images/journal/rules/Level_10.webp", layout="photo_left"),
            Teaser("kitchen_door_photo", "Photo of the courtyard annex door—padlocked, menu faded, paint peeling. Still waiting for someone to claim it.", PlaceholderCondition(), interpretation="The building is an unused answer sitting in plain sight.", note_type="insight", image="images/journal/rules/Level_10.webp", layout="photo_right"),
            Teaser("adelaide_handshake_photo", "Adelaide in the office doorway, half-promise written on her face. She wants in—if we open the door.", PlaceholderCondition(), interpretation="Alliance forming. Document it before the moment softens into rumor.", note_type="suspicion", image="images/journal/rules/Level_10.webp", layout="photo_top"),
            Teaser("menu_board_photo", "Close-up of the yellowed annex menu board. Prices from another decade, still stuck to the glass.", PlaceholderCondition(), interpretation="A fossil of the old cafeteria. Proof the school already knew how to feed students.", note_type="insight", image="images/journal/rules/Level_10.webp", layout="text_full"),
            Teaser("queue_aside_photo", "Side note with a snap of the afternoon queue spilling past the kiosk railing.", PlaceholderCondition(), interpretation="Capacity failure made visible. The line is the complaint.", note_type="observation", image="images/journal/rules/Level_10.webp", layout="text_aside"),
            Bar("main", limits = (-30, 60), stat_weights = {HAPPINESS: 0.5, EDUCATION: 0.2, REPUTATION: 0.2}),
            BlockingThreshold("The students need a permanent place to eat lunch. There must be somewhere on campus—I just need to look a little closer.", "The vacant building next to the courtyard—there used to be a kitchen there. I should inspect it and see if it's suitable for a cafeteria", PlaceholderCondition(), main = -5),
            AutoThreshold("If I push forward with the cafeteria idea, someone from the PTA will surely reach out. I should be open to suggestions.", main = 10, visible_range = 10),
            BlockingThreshold("A school cafeteria isn't something I can do on my own. The PTA has to be on board—I need their approval before we can move forward.", "The PTA must approve the opening of the cafeteria. I should plan a vote and gather enough support.", PlaceholderCondition(), main = 20, visible_range = 10),
            AutoThreshold("With the PTA's approval, the renovation can begin. The kitchen will take a while to be ready for use again.", main = 35),
            BlockingThreshold("Adelaide has agreed to help, but managing a commercial kitchen is new to her. At some point, she'll need concrete support.", "Adelaide is stuck on the meal plan. I should work in the office or check on her in the cafeteria and help her.", PlaceholderCondition(), main = 40),
            AutoThreshold("Once the kitchen and menu are set, the crucial test comes—the first real lunch service for the students.", main = 50),
            AutoThreshold("The cafeteria is up and running. Just a few more steps, and Adelaide will have gotten the hang of it, and the whole thing will run on its own.", main = 60),
            PassiveOption(
                "leave_adelaide",
                "Leave Adelaide alone",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("cafeteria_crisis_leave_adelaide_noop", 0, "No-op"),
            ),
            PassiveOption(
                "hire_staff",
                "Hire additional staff",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("cafeteria_crisis_hire_staff_noop", 0, "No-op"),
            ),
            PassiveOption(
                "train_adelaide",
                "Train Adelaide personally",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("cafeteria_crisis_train_adelaide_noop", 0, "No-op"),
            ),
            SituationPool("Delivery problem", 35, 54),
            SituationPool("Student Complaints", -10, 54),
            SituationPool("Adelaide Overwhelmed", 10, 48),
            SituationPool("Teacher Feedback", -5, 54),
            PositiveResolution("ALL", DummyEffect()),
            NegativeResolution("ANY", DummyEffect()),
            thumbnail="images/Test/Test-1.png",
        ),
        # Trigger: sb_event_6. Startwert -20 at activation (events can shift via shift_start_value).
        Situation("body_conflict", "Body Conflict", "Body-related conflicts among female students are escalating. Aona uses her physical development as a status symbol. Miwa is the primary target, but the toxic dynamic affects the entire school. The protagonist must decide how to handle this.",
            Teaser("gym_tension", "There’s a strange tension in gym class. Girls openly compare themselves—and some force others onto the defensive.", PlaceholderCondition(), interpretation="Status performance in a body-visible space. Comparison is the weapon.", note_type="observation"),
            Teaser("changing_room_rumors", "Rumors from the locker room: Someone is bragging about her body and belittling others. This sounds like more than just childish nonsense.", PlaceholderCondition(), interpretation="Private space, public hierarchy. The rumor names a pattern, not an incident.", note_type="suspicion"),
            Teaser("miwa_withdraws", "Miwa avoids the dining hall. She eats alone or not at all. Something is going on there that I can’t quite put my finger on yet.", PlaceholderCondition(), interpretation="Classic avoidance. She retreats instead of confronting.", note_type="setback", image="images/misc/Test_4_3.png", layout="text_full"),
            Teaser("gym_bench_photo", "Caught the gym bench after class—bags piled, whispered scores still hanging in the air.", PlaceholderCondition(), interpretation="The room keeps the hierarchy even after the whistle.", note_type="observation", image="images/misc/Test_4_3.png", layout="photo_left"),
            Teaser("locker_mirror_photo", "Locker-room mirror, fogged edge, empty center. Someone practiced a smile there before walking out sharp.", PlaceholderCondition(), interpretation="Performance prep. The cruelty is rehearsed.", note_type="suspicion", image="images/misc/Test_4_3.png", layout="photo_right"),
            Teaser("empty_lunch_seat_photo", "Miwa's usual seat left cold. Tray untouched two tables over.", PlaceholderCondition(), interpretation="Absence as evidence. The conflict has a body count without bruises.", note_type="setback", image="images/misc/Test_4_3.png", layout="photo_top"),
            Teaser("hallway_aside_photo", "Margin note: a hallway snap where the crowd parts around Miwa without looking at her.", PlaceholderCondition(), interpretation="Social invisibility as punishment. The group polices by omission.", note_type="suspicion", image="images/misc/Test_4_3.png", layout="text_aside"),
            Bar("main", limits = (-50, 60), stat_weights = {HAPPINESS: 1.0, INHIBITION: -0.8, CHARM: 0.3}, start_base=-20),
            AutoThreshold("Things are getting ugly between Aona and Miwa. If this keeps up, someone’s going to break down.", main = -45, direction = -1),
            AutoThreshold("Aona is getting bolder and bolder. Someone needs to stop this before the whole school becomes complicit.", main = -35, direction = -1),
            AutoThreshold("Not everything stays hidden. At some point, someone has to call this problem out.", main = 0),
            BlockingThreshold("Aona is at the center of all this. I won’t get anywhere here without talking to her.", "I need to talk to Aona—a counseling session in the office, not a lecture.", PlaceholderCondition(), main = 20),
            AutoThreshold("Miwa seems to be slowly reappearing. Maybe there’s more hope than I thought.", main = 35),
            BlockingThreshold("This needs to be resolved. Aona and Miwa will have to face each other eventually—whether they want to or not.", "The moment has come. Aona and Miwa must face each other—how this turns out depends on me, too.", PlaceholderCondition(), main = 50),
            AutoThreshold("The school is changing. The girls are no longer distinguished by their bodies—at least not the way Aona wanted.", main = 60),
            PassiveOption(
                "wait_and_observe",
                "Wait and see",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("body_conflict_wait_and_observe_noop", 0, "No-op"),
            ),
            PassiveOption(
                "fund_counseling",
                "Fund school counseling",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("body_conflict_fund_counseling_noop", 0, "No-op"),
            ),
            PassiveOption(
                "accelerate_exposure",
                "Accelerate exposure",
                # No-op effect so SituationPassive self-check passes.
                SituationEffectSetGameData("body_conflict_accelerate_exposure_noop", 0, "No-op"),
            ),
            SituationPool("gym_enter_changing_tension", -50, 54),
            SituationPool("cafeteria_look_around_dynamics", -40, 54),
            SituationPool("school_dormitory_peek_students_night_talk", -35, 50),
            SituationPool("courtyard_patrol_bodies", -45, 54),
            SituationPool("school_building_teach_class_body", -25, 54),
            SituationPool("office_building_counseling_teacher", 0, 54),
            PositiveResolution("ALL", DummyEffect()),
            NegativeResolution("ANY", DummyEffect()),
            thumbnail="images/misc/Test_16_9.png",
        ),
        # Multi-bar smoke test: three stakeholder bars + mixed bounds (subset vs all).
        # Combined handle uses bar_weights; each bar starts at -10.
        Situation("pta_multi_bar_test", "PTA Multi-Bar Test", "Test situation with separate teacher, parent, and student progress bars. Used to validate multi-bar thresholds, projected markers, and combined resolution.",
            Bar("teachers", weight = 0.4, limits=(-40, 60), stat_weights={REPUTATION: 0.4, EDUCATION: 0.3}, start_base=-10),
            Bar("parents", weight = 0.4, limits=(-40, 60), stat_weights={REPUTATION: 0.5, HAPPINESS: 0.2}, start_base=-10),
            Bar("students", weight = 0.2, limits=(-40, 60), stat_weights={HAPPINESS: 0.5, EDUCATION: 0.2}, start_base=-10),
            AutoThreshold("Opposition is hardening on all sides. If this keeps sliding, the PTA idea dies quietly.", teachers=-35, parents=-35, direction=-1),
            BlockingThreshold("Nobody will even discuss a PTA while the factions refuse to admit there's a problem.", "I need a first acknowledgment from teachers and parents—something that puts the issue on record.", PlaceholderCondition(), teachers=-10, parents=-10),
            AutoThreshold("The faculty seems more open lately. Parent opinion may still lag behind.", teachers=15, visible_range=15),
            BlockingThreshold("A PTA only works if staff and parents both commit. Students can wait—the vote can't.", "I should schedule a PTA vote and secure enough teacher and parent support.", PlaceholderCondition(), teachers=25, parents=30, visible_range=15),
            AutoThreshold("Momentum is building across the school. Even the students are starting to notice.", teachers=40, parents=40, students=20),
            BlockingThreshold("Almost there—but all three groups have to land in the same place before this sticks.", "Final consensus: teachers, parents, and students each need a clear win before we lock this in.", PlaceholderCondition(), teachers=50, parents=50, students=45),
            AutoThreshold("The PTA structure is stable. The rest should run without constant firefighting.", teachers=60, parents=60, students=60),
            PassiveOption("court_teachers", "Prioritize teacher outreach", SituationEffectStatChangeModifier("corruption", 10, "+")),
            PassiveOption("court_parents", "Prioritize parent outreach", SituationEffectStatChangeModifier("inhibition", 10, "+")),
            PassiveOption("court_students", "Prioritize student voice", SituationEffectStatChangeModifier("happiness", 10, "+")),
            MeasureOption(
                "faculty_briefing",
                "Call a short faculty briefing. Steady teacher support for a few periods.",
                TimerCondition("pta_multi_bar_faculty_duration", daytime=3),
                TimerCondition("pta_multi_bar_faculty_cooldown", daytime=2),
                ManualCounterCondition("pta_multi_bar_faculty_count", 3),
                instant=[SituationEffectSetGameData("pta_multi_bar_faculty_ping", 1, "Staff puts the PTA on today's agenda")],
                permanent=[SituationEffectBarChangeModifier("teachers", 3, "+", "daytime_change")],
            ),
            MeasureOption(
                "parent_coffee",
                "Host a parent coffee hour. Softens parent resistance while it runs.",
                TimerCondition("pta_multi_bar_parent_duration", daytime=4),
                TimerCondition("pta_multi_bar_parent_cooldown", daytime=3),
                ManualCounterCondition("pta_multi_bar_parent_count", 2),
                instant=[SituationEffectSetGameData("pta_multi_bar_parent_ping", 1, "Parents feel heard—for now")],
                permanent=[SituationEffectBarChangeModifier("parents", 3, "+", "daytime_change")],
            ),
            MeasureOption(
                "student_forum",
                "Open a student forum. Quick bump in student voice, short burn.",
                TimerCondition("pta_multi_bar_student_duration", daytime=2),
                TimerCondition("pta_multi_bar_student_cooldown", daytime=2),
                ManualCounterCondition("pta_multi_bar_student_count", 3),
                instant=[SituationEffectSetGameData("pta_multi_bar_student_ping", 1, "Students get a microphone")],
                permanent=[SituationEffectBarChangeModifier("students", 4, "+", "daytime_change")],
            ),
            MeasureOption(
                "all_hands_push",
                "All-hands outreach week. Mild lift on every stakeholder bar.",
                TimerCondition("pta_multi_bar_allhands_duration", daytime=5),
                TimerCondition("pta_multi_bar_allhands_cooldown", day=1),
                ManualCounterCondition("pta_multi_bar_allhands_count", 1),
                instant=[SituationEffectSetGameData("pta_multi_bar_allhands_ping", 1, "School-wide attention spike")],
                permanent=[
                    SituationEffectBarChangeModifier("teachers", 1, "+", "daytime_change"),
                    SituationEffectBarChangeModifier("parents", 1, "+", "daytime_change"),
                    SituationEffectBarChangeModifier("students", 2, "+", "daytime_change"),
                ],
            ),
            SituationPool("office_building_work_pta_faculty", -10, 50),
            SituationPool("courtyard_patrol_pta_parents", -10, 50),
            SituationPool("school_building_teach_pta_students", 15, 55),
            PositiveResolution("ALL", DummyEffect()),
            NegativeResolution("ANY", DummyEffect()),
            thumbnail="images/Test/Test-1.png",
       
        ),
        Situation("new_management", "New Management",
            SituationDescription([
                "The extreme potion effects of the first week have faded. Memories are fuzzy — a vague unease remains.",
                "Teachers are cautious, students test boundaries, parents watch. The school is deciding whether it still has a headmaster.",
            ]),
            Bar(
                "main",
                limits=(-25, 40),
                start_base=0,
                regular_decrease_rate=-0.4,
                stat_weights={REPUTATION: 0.4, HAPPINESS: 0.3, EDUCATION: 0.2, CHARM: 0.2},
            ),
            # Thresholds = campus reactions (Auto only)
            AutoThreshold(
                "Emiko has stopped hiding the pink slips. Parent messages are stacking. She hasn't said anything — she doesn't have to.",
                EventEffect("nm_thresh_emiko_nudge"),
                main=-12,
                direction=-1,
            ),
            AutoThreshold(
                "One more empty stretch and someone at the district picks up the phone. ",
                EventEffect("nm_thresh_district_letter"),
                main=-20,
                direction=-1,
            ),
            AutoThreshold(
                "Emiko wished me luck this morning without being asked. Small thing. Not nothing.",
                EventEffect("nm_thresh_first_warmth"),
                main=5,
                direction=1,
            ),
            AutoThreshold(
                "Yulan stopped me between periods — the students are settling. She sounded like she'd been holding her breath.",
                EventEffect("nm_thresh_yulan_thaw"),
                main=15,
                direction=1,
            ),
            AutoThreshold(
                "They've dropped the word 'new'. I'm just 'the headmaster' now.",
                EventEffect("nm_thresh_adelaide_note"),
                main=25,
                direction=1,
            ),
            AutoThreshold(
                "The paperwork calls me headmaster. No qualifiers.",
                EventEffect("nm_thresh_near_end"),
                main=36,
                direction=1,
            ),
            PassiveOption(
                "guided_orientation",
                "Guided tips on",
                SituationEffectSetGameData("new_management_guided", 1, "Guided tips on"),
                SituationEffectBarChangeModifier("main", 0.15, "+", "daytime_change"),
            ),
            PassiveOption(
                "self_directed",
                "Guided tips off",
                SituationEffectSetGameData("new_management_guided", 0, "Guided tips off"),
            ),
            MeasureOption(
                "review_map",
                "Review the map interface.",
                TimerCondition("nm_review_map_duration", daytime=2),
                TimerCondition("nm_review_map_cooldown", day=2),
                instant=[
                    SituationEffectGeneral(
                        "nm_review_map_ping",
                        [EventEffect("map_tutorial")],
                        ["Open the Map tutorial."],
                        revert=False,
                    )
                ],
            ),
            MeasureOption(
                "review_journal",
                "Review the Journal interface.",
                TimerCondition("nm_review_journal_duration", daytime=2),
                TimerCondition("nm_review_journal_cooldown", day=2),
                instant=[
                    SituationEffectGeneral(
                        "nm_review_journal_ping",
                        [EventEffect("journal_tutorial")],
                        ["Open the Journal tutorial."],
                        revert=False,
                    )
                ],
            ),
            MeasureOption(
                "review_actions",
                "Review the Action interface.",
                TimerCondition("nm_review_actions_duration", daytime=2),
                TimerCondition("nm_review_actions_cooldown", day=2),
                instant=[
                    SituationEffectGeneral(
                        "nm_review_actions_ping",
                        [EventEffect("action_tutorial")],
                        ["Open the Action tutorial."],
                        revert=False,
                    )
                ],
            ),
            # Chronicle Teasers (13)
            Teaser(
                "nm_wrong_face",
                "Someone printed my name — wrong spelling, wrong tape.\nStudents outside were pointing at the janitor.\nThe office doesn't label me. Neither do they.",
                OR(
                    EventSeenCondition(True, "nm_ghost_office_nameplate"),
                    EventSeenCondition(True, "nm_ghost_office_janitor"),
                ),
                interpretation="A name that doesn't match a face. The school is misreading presence as rumor.",
                note_type="observation",
            ),
            Teaser(
                "nm_private_line",
                "Emiko answered too warmly on the phone.\nHer voice snapped tight when footsteps passed.\nShe knows me privately; performs the distance publicly.",
                EventSeenCondition(True, "nm_ghost_office_private_line"),
                interpretation="Private warmth with public restraint. An intimacy that knows where it is allowed to stand.",
                note_type="suspicion",
            ),
            Teaser(
                "nm_frozen_hallway",
                "Yulan didn't lift her eyes when I passed.\nThe corridor kept its temperature.\nSilence as verdict. Staff won't grant a title on air.",
                EventSeenCondition(True, "nm_ghost_office_empty_corridor"),
                interpretation="A learned pause. When respect is withheld, it becomes an atmosphere instead of a sentence.",
                note_type="setback",
            ),
            Teaser(
                "nm_miwa_gap",
                "Miwa couldn't remember Tuesday morning.\nHer notebook was blank where the week should be.\nThe potion took the day; no one has offered her one back.",
                EventSeenCondition(True, "nm_potion_hangover_miwa"),
                interpretation="A missing morning creates emotional permission. The gap makes uncertainty feel safe.",
                note_type="setback",
            ),
            Teaser(
                "nm_lily_shaken",
                "Lily's mug rattled against the desk.\nShe asked if last week was real.\nThe staff need a witness before they can name it.",
                EventSeenCondition(True, "nm_potion_hangover_lily"),
                interpretation="Fear becomes a question when it finally finds someone who can listen.",
                note_type="observation",
            ),
            Teaser(
                "nm_vial_found",
                "Green glass by the bike rack, sticky at the neck.\nSame smell as the corridor last Tuesday.\nThe evidence didn't leave. It just stopped being obvious.",
                EventSeenCondition(True, "nm_potion_hangover_vial"),
                interpretation="A trace that refuses to fade. The truth is still here, but the school learned to look away.",
                note_type="insight",
                image="images/journal/rules/Level_10.webp",
                layout="photo_left",
            ),
            Teaser(
                "nm_pink_slips",
                "Pink slips no longer hidden — Emiko stopped filing them.\nOne was signed 'concerned observer'.\nNeglect has a paper trail. The floor is close.",
                OR(
                    EventSeenCondition(True, "nm_thresh_emiko_nudge"),
                    EventSeenCondition(True, "nm_thresh_district_letter"),
                ),
                interpretation="Paper becomes pressure. When anxiety is paperwork-shaped, it travels farther than speeches.",
                note_type="setback",
            ),
            Teaser(
                "nm_clipboard_precedents",
                "Yuriko asked three questions with grey answers.\nMy words were on paper before lunch.\nCasual replies are precedents now. She's mapping the office.",
                OR(
                    EventSeenCondition(True, "nm_testing_the_waters_clipboard"),
                    EventSeenCondition(True, "nm_testing_the_waters_memo"),
                ),
                interpretation="Policy as memory: she turns his uncertainty into something she can cite later.",
                note_type="suspicion",
            ),
            Teaser(
                "nm_face_sticks",
                "\"That's him from the assembly — I remember now.\"\nAona corrected herself mid-sentence.\nThe face has caught up with the title. It sticks now.",
                EventSeenCondition(True, "nm_rumors_in_bloom_kiosk"),
                interpretation="Recognition as repair. The school doesn't just learn you — it re-labels you in public.",
                note_type="observation",
            ),
            Teaser(
                "nm_chalk_portrait",
                "A chalk portrait behind the bike shed.\nRoughly me — and, oddly, flattering.\nThe world is drawing me back in.",
                EventSeenCondition(True, "nm_rumors_in_bloom_chalk"),
                interpretation="A reflection drawn by gossip. When the sketch is kind, legitimacy follows.",
                note_type="observation",
                image="images/journal/rules/Level_10.webp",
                layout="photo_right",
            ),
            Teaser(
                "nm_yulan_thaw",
                "Yulan stopped me between periods.\nThe students are settling, she said, quietly.\nStaff temperature is rising. Legitimacy earned in pieces.",
                OR(
                    EventSeenCondition(True, "nm_thresh_yulan_thaw"),
                    EventSeenCondition(True, "nm_thresh_first_warmth"),
                ),
                interpretation="A controlled thaw. Care is being practiced, not declared.",
                note_type="insight",
            ),
            Teaser(
                "nm_care_channel",
                "Miwa thanked me and left before I could answer.\nLily returned my outline: \"Actually… better.\"\nCare flowed and returned. The channel opened both ways.",
                OR(
                    EventSeenCondition(True, "nm_quiet_endorsements_after_bell"),
                    EventSeenCondition(True, "nm_quiet_endorsements_second_coffee"),
                    EventSeenCondition(True, "nm_quiet_endorsements_curriculum"),
                ),
                interpretation="Mutual responsiveness. The school is treating you as someone who can hold care without asking for it back.",
                note_type="insight",
            ),
            Teaser(
                "nm_title_earned",
                "The plaque arrived with my name spelled right.\nFinola raised her mug in the staff room.\nThe word 'new' has fallen off. I'm just 'the headmaster' now.",
                OR(
                    EventSeenCondition(True, "nm_welcome_committee_plaque"),
                    EventSeenCondition(True, "nm_welcome_committee_mug"),
                    EventSeenCondition(True, "nm_welcome_committee_assembly"),
                    EventSeenCondition(True, "nm_thresh_adelaide_note"),
                    EventSeenCondition(True, "nm_thresh_near_end"),
                ),
                interpretation="A ritual that seals identity. The school speaks your title the way it speaks rules: consistently.",
                note_type="insight",
                image="images/journal/rules/Level_10.webp",
                layout="photo_top",
            ),
            # Event pools (mood bands)
            SituationPool("nm_ghost_office", -25, -8),
            SituationPool("nm_potion_hangover", -20, 5),
            SituationPool("nm_testing_the_waters", -5, 20),
            SituationPool("nm_rumors_in_bloom", 0, 25),
            SituationPool("nm_quiet_endorsements", 10, 30),
            SituationPool("nm_welcome_committee", 22, 40),
            # Resolutions
            PositiveResolution(
                "ALL",
                ValueEffect("new_management_resolved", "positive"),
                EventEffect("new_management_positive_resolve"),
            ),
            NegativeResolution(
                "ANY",
                ValueEffect("new_management_resolved", "negative"),
                EventEffect("game_over_new_management"),
                grace_count=1,
            ),
            thumbnail="images/Test/Test-1.png",
        ),
    )
    
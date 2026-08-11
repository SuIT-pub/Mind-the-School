init -99 python:
    building_manager = None

    def expand_keyboard_shortcut(shortcut: str) -> List[str]:
        """Expand a canonical shortcut into Ren'Py key names.

        Digits bind both the main keyboard and the keypad. Letters bind a
        single key. Full Ren'Py key names (``K_…``) are passed through.

        Args:
            shortcut: Canonical shortcut such as ``"1"``, ``"j"``, or a full
                Ren'Py key name such as ``"K_KP_ENTER"``.

        Returns:
            List of Ren'Py key name strings for screen ``key`` bindings.
        """
        s = shortcut.strip()
        if not s:
            return []
        if s.startswith("K_"):
            return [s]
        if len(s) == 1 and s.isdigit():
            return [f"K_{s}", f"K_KP{s}"]
        if len(s) == 1 and s.isalpha():
            return [f"K_{s.lower()}"]
        return [f"K_{s}"]

    class Building:
        def __init__(
            self,
            key: str,
            image: str,
            x_pos: int,
            y_pos: int,
            open_conditions: List[Condition],
            close_conditions: List[Condition],
            keyboard_shortcuts: List[str] = None,
        ):
            """Create a map building entry.

            Args:
                key: Building identifier used by events and availability checks.
                image: Base image path for the building sprite.
                x_pos: Horizontal position on the overview map.
                y_pos: Vertical position on the overview map.
                open_conditions: Conditions that open the building when any match.
                close_conditions: Conditions that keep the building closed when any match.
                keyboard_shortcuts: Canonical shortcuts for this building
                    (e.g. ``["1"]`` or ``["j"]``). Digits expand to main and
                    keypad Ren'Py keys at bind time.
            """
            self.key = key
            # Redirect the path into the current mod's folder (base = "" prefix).
            self.image = get_mod_path(active_mod_key) + image if image else image
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.open_conditions = open_conditions
            self.close_conditions = close_conditions
            self.open_conditions.append(HasAnythingInCollectionGameDataCondition(key + ":open"))
            self.close_conditions.append(HasAnythingInCollectionGameDataCondition(key + ":closed"))
            self.keyboard_shortcuts = list(keyboard_shortcuts) if keyboard_shortcuts else []

        def check_open_conditions(self, **kwargs):
            return any(condition.is_fulfilled(**kwargs) for condition in self.open_conditions)

        def check_close_conditions(self, **kwargs):
            return any(condition.is_fulfilled(**kwargs) for condition in self.close_conditions)

        def is_open(self, **kwargs):
            return self.check_open_conditions(**kwargs) and not self.check_close_conditions(**kwargs)

        def get_image(self, state: str = "empty"):
            return refine_image(self.image, state = state)

        def has_highlight(self):
            return get_available_highlight(self.key)

        def get_renpy_keys(self) -> List[str]:
            """Return Ren'Py key names for all configured shortcuts.

            Returns:
                Expanded key list suitable for screen ``key`` statements.
            """
            keys = []
            for shortcut in self.keyboard_shortcuts:
                keys.extend(expand_keyboard_shortcut(shortcut))
            return keys

        def has_shortcut(self) -> bool:
            return len(self.keyboard_shortcuts) > 0

        def get_shortcut_label(self) -> str:
            """Return the tooltip suffix for the primary shortcut.

            Returns:
                Label such as ``" [[1]"``, or an empty string when no shortcut
                is configured. The doubled bracket is the Ren'Py escape for a
                literal ``[``.
            """
            if not self.keyboard_shortcuts:
                return ""
            return " [[" + self.keyboard_shortcuts[0].upper() + "]"

        def get_name(self, with_shortcut: bool = False) -> str:
            """Return the display name of this building.

            Args:
                with_shortcut: If True, append the primary shortcut label when
                    one is configured.

            Returns:
                Human-readable building name, optionally with shortcut suffix.
            """
            name = self.key.replace("_", " ").title()
            if with_shortcut:
                name += self.get_shortcut_label()
            return name

    class BuildingManager:
        """Registry for overview map buildings.

        Holds definition objects only. Open/closed state is evaluated from
        conditions at call time; nothing here is persisted in the save.
        """

        def __init__(self):
            self._buildings = {}

        def load_building(self, building: Building):
            """Insert or replace a building definition by key.

            Args:
                building: Map building definition to register.

            Returns:
                This manager, for chained registration.
            """
            self._buildings[building.key] = building
            return self

        def get_building(self, key: str):
            """Return a building by key, or None if unknown.

            Args:
                key: Building identifier.

            Returns:
                The registered building, or None.
            """
            return self._buildings.get(key)

        def get_buildings(self) -> List[Building]:
            """Return all registered buildings.

            Returns:
                List of building definitions in registration order is not
                guaranteed; treat as an unordered collection.
            """
            return list(self._buildings.values())

        def has_building(self, key: str) -> bool:
            """Return whether a building key is registered.

            Args:
                key: Building identifier.

            Returns:
                True if the key exists in the registry.
            """
            return key in self._buildings

        def is_open(self, key: str, **kwargs) -> bool:
            """Return whether the building is currently open.

            Args:
                key: Building identifier.
                **kwargs: Passed through to condition checks.

            Returns:
                True if the building exists and ``is_open`` succeeds.
            """
            building = self.get_building(key)
            if building is None:
                return False
            return building.is_open(**kwargs)

        def get_open_buildings(self, **kwargs) -> List[Building]:
            """Return all buildings that are currently open.

            Args:
                **kwargs: Passed through to condition checks.

            Returns:
                List of open building definitions.
            """
            return [building for building in self._buildings.values() if building.is_open(**kwargs)]

        def clear(self):
            """Remove all registered buildings."""
            self._buildings.clear()

    def register_buildings(*buildings: Building):
        """Load building definitions into the global building manager.

        Creates ``building_manager`` if it does not exist yet. Call from a
        load label after creating or resetting the manager.

        Args:
            *buildings: Map building definitions to register.
        """
        global building_manager
        if building_manager is None:
            building_manager = BuildingManager()
        # Gated on the current mod being active (like event `add_event`): a disabled
        # mod's buildings are not registered. Base loaders set `set_current_mod('base')`.
        if is_mod_active(active_mod_key):
            for building in buildings:
                building_manager.load_building(building)

    def add_building_collection_key(building_key: str, state: str, entry_key: str):
        """Add an entry to a building open/closed game-data collection.

        Multiple systems can contribute distinct keys. The building reacts to
        whether the collection is non-empty, not to any single caller.

        Args:
            building_key: Building key (e.g. ``\"school_building\"``).
            state: ``\"open\"`` or ``\"closed\"``.
            entry_key: Caller-specific reason key to insert.
        """
        if is_in_replay:
            return
        if state not in ("open", "closed"):
            return
        collection_key = building_key + ":" + state
        data = get_game_data(collection_key)
        if data is None or not isinstance(data, list):
            data = []
        if entry_key in data:
            return
        set_game_data(collection_key, list(data) + [entry_key])

    def remove_building_collection_key(building_key: str, state: str, entry_key: str):
        """Remove one entry from a building open/closed collection.

        Only ``entry_key`` is removed; other callers' keys stay in place.

        Args:
            building_key: Building key (e.g. ``\"school_building\"``).
            state: ``\"open\"`` or ``\"closed\"``.
            entry_key: Caller-specific reason key to remove.
        """
        if is_in_replay:
            return
        if state not in ("open", "closed"):
            return
        collection_key = building_key + ":" + state
        data = get_game_data(collection_key)
        if data is None or not isinstance(data, list) or entry_key not in data:
            return
        set_game_data(collection_key, [item for item in data if item != entry_key])

    def add_all_buildings_collection_key(state: str, entry_key: str):
        """Add ``entry_key`` to every registered building's open/closed collection.

        Args:
            state: ``\"open\"`` or ``\"closed\"``.
            entry_key: Caller-specific reason key to insert.
        """
        if is_in_replay or building_manager is None:
            return
        for building in building_manager.get_buildings():
            add_building_collection_key(building.key, state, entry_key)

    def remove_all_buildings_collection_key(state: str, entry_key: str):
        """Remove ``entry_key`` from every registered building's collection.

        Args:
            state: ``\"open\"`` or ``\"closed\"``.
            entry_key: Caller-specific reason key to remove.
        """
        if is_in_replay or building_manager is None:
            return
        for building in building_manager.get_buildings():
            remove_building_collection_key(building.key, state, entry_key)

    def get_location_title(key: str) -> str:
        """Return a display title for a location key.

        Prefers the map building name when registered.

        Args:
            key: Location / building key.

        Returns:
            Human-readable title, or ``key`` if unknown.
        """
        if building_manager is not None:
            building = building_manager.get_building(key)
            if building is not None:
                return building.get_name()
        return key

label load_buildings:
    $ set_current_mod('base')

    if building_manager is None:
        $ building_manager = BuildingManager()

    $ register_buildings(
        Building(
            "school_building", 
            "images/background/school_building_<state>.webp", 
            563,
            620,
            [ManualCondition(True)],
            [],
            ["1"],
        ),
        Building(
            "school_dormitory",
            "images/background/school_dormitory_<state>.webp",
            1202,
            410,
            [ManualCondition(True)],
            [],
            ["2"],
        ),
        Building(
            "labs",
            "images/background/labs_<state>.webp",
            722,
            176,
            [],
            [],
            [],
        ),
        Building(
            "sports_field",
            "images/background/sports_field_<state>.webp",
            241,
            130,
            [],
            [],
            [],
        ),
        Building(
            "beach",
            "images/background/beach_<state>.webp",
            952,
            728,
            [],
            [],
            [],
        ),
        Building(
            "staff_lodges",
            "images/background/staff_lodges_<state>.webp",
            -19,
            624,
            [],
            [],
            [],
        ),
        Building(
            "gym",
            "images/background/gym_<state>.webp",
            140,
            289,
            [ManualCondition(True)],
            [],
            ["6"],
        ),
        Building(
            "swimming_pool",
            "images/background/swimming_pool_<state>.webp",
            354,
            348,
            [],
            [],
            [],
        ),
        Building(
            "cafeteria",
            "images/background/cafeteria_<state>.webp",
            825,
            473,
            [],
            [],
            ["7"],
        ),
        Building(
            "bath",
            "images/background/bath_<state>.webp",
            441,
            -19,
            [],
            [],
            [],
        ),
        Building(
            "kiosk",
            "images/background/kiosk_<state>.webp",
            269,
            510,
            [ManualCondition(True)],
            [],
            ["5"],
        ),
        Building(
            "courtyard",
            "images/background/courtyard_<state>.webp",
            452,
            490,
            [ManualCondition(True)],
            [],
            ["4"],
        ),
        Building(
            "office_building",
            "images/background/office_building_<state>.webp",
            976,
            70,
            [ManualCondition(True)],
            [],
            ["3"],
        ),
    )
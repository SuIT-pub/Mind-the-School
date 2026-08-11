default time_freeze = False
default debug_mode = False
default game_log_entries = []
default log_entry_seq = 0
default log_filter_type = "all"
default log_filter_category = "all"
default log_filter_origin = "all"
default log_json_expanded = {}

init -100 python:
    import inspect
    import os
    import pprint

    LOG_TYPES = ("info", "debug", "warning", "error")
    LOG_TYPE_COLORS = {
        "info": "#3a7ebd",
        "debug": "#7a7a7a",
        "warning": "#c47a00",
        "error": "#a00000",
    }
    LOG_MAX_ENTRIES = 500
    _LOG_INTERNAL_FUNCS = frozenset({
        "_append_log_entry",
        "_format_log_prefix",
        "_normalize_log_type",
        "_resolve_log_origin",
        "log",
        "log_count",
        "log_json",
        "log_separator",
        "log_val",
    })

    class FloatInputValue(InputValue):
        def __init__(self, variable, default=0.0):
            self.variable = variable
            self.default = default

        def get_text(self):
            return str(getattr(store, self.variable))

        def set_text(self, s):
            try:
                setattr(store, self.variable, float(s))
            except ValueError:
                setattr(store, self.variable, self.default)
            renpy.restart_interaction()

        def enter(self):
            renpy.run(RestartInteraction())
            return True

    def _normalize_log_type(log_type: str) -> str:
        """
        Normalizes a log type string to a known value.

        ### Parameters:
        1. log_type: str
            - The requested log type.

        ### Returns:
        1. str
            - One of LOG_TYPES; defaults to "info".
        """
        if log_type is None:
            return "info"
        normalized = str(log_type).strip().lower()
        if normalized in LOG_TYPES:
            return normalized
        return "info"

    def _resolve_log_origin(origin=None) -> str:
        """
        Resolves the call origin for a log entry.

        Uses an explicit override when provided, otherwise inspects the stack
        for the first non-internal caller frame.

        ### Parameters:
        1. origin: Optional[str]
            - Explicit origin override.

        ### Returns:
        1. str
            - Origin string such as "helper.rpy:get_setting" or "unknown".
        """
        if origin is not None and str(origin).strip() != "":
            return str(origin)

        try:
            frame = inspect.currentframe()
            try:
                caller = frame.f_back if frame is not None else None
                while caller is not None:
                    func_name = caller.f_code.co_name
                    if func_name not in _LOG_INTERNAL_FUNCS:
                        filename = os.path.basename(caller.f_code.co_filename)
                        class_name = None
                        locals_map = caller.f_locals
                        for key in ("self", "cls"):
                            if key in locals_map:
                                obj = locals_map[key]
                                class_name = getattr(obj, "__name__", None)
                                if class_name is None:
                                    class_name = getattr(getattr(obj, "__class__", None), "__name__", None)
                                break
                        if class_name:
                            return f"{filename}:{class_name}.{func_name}"
                        return f"{filename}:{func_name}"
                    caller = caller.f_back
            finally:
                del frame
        except Exception:
            pass
        return "unknown"

    def _format_log_prefix(log_type: str, category=None, origin=None) -> str:
        """
        Builds a console prefix for a log line.

        ### Parameters:
        1. log_type: str
            - Normalized log type.
        2. category: Optional[str]
            - Optional category label.
        3. origin: Optional[str]
            - Optional origin label.

        ### Returns:
        1. str
            - Prefix such as "[INFO][cat] file:func | ".
        """
        parts = [f"[{str(log_type).upper()}]"]
        if category:
            parts.append(f"[{category}]")
        if origin:
            parts.append(str(origin))
        return " ".join(parts) + " | "

    def _prepare_log_json_data(value, depth: int = 0, max_depth: int = 20):
        """
        Converts a value into a JSON-tree friendly structure for journal display.

        ### Parameters:
        1. value: Any
            - The value to convert.
        2. depth: int (default: 0)
            - Current recursion depth.
        3. max_depth: int (default: 20)
            - Maximum recursion depth.

        ### Returns:
        1. Any
            - Nested dict/list/primitives suitable for the expandable tree UI.
        """
        if depth > max_depth:
            return "<max depth>"
        if value is None or isinstance(value, (bool, int, float)):
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            return {
                str(key): _prepare_log_json_data(child, depth + 1, max_depth)
                for key, child in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [_prepare_log_json_data(child, depth + 1, max_depth) for child in value]
        try:
            if hasattr(value, "__dict__"):
                return _prepare_log_json_data(vars(value), depth + 1, max_depth)
        except Exception:
            pass
        return repr(value)

    def _append_log_entry(message: str, log_type: str = "info", category=None, origin=None, is_separator: bool = False, data=None, is_json: bool = False):
        """
        Appends a log entry to the session log store.

        ### Parameters:
        1. message: str
            - The log message body.
        2. log_type: str (default: "info")
            - Log severity type.
        3. category: Optional[str]
            - Optional category label.
        4. origin: Optional[str]
            - Explicit origin override; auto-resolved when omitted.
        5. is_separator: bool (default: False)
            - Whether this entry represents a visual separator.
        6. data: Any (default: None)
            - Optional structured payload (used for JSON tree entries).
        7. is_json: bool (default: False)
            - Whether the entry should render as an expandable JSON tree.
        """
        resolved_category = str(category) if category else None

        if not hasattr(store, "game_log_entries") or store.game_log_entries is None:
            store.game_log_entries = []
        if not hasattr(store, "log_entry_seq") or store.log_entry_seq is None:
            store.log_entry_seq = 0

        store.log_entry_seq += 1
        if is_separator:
            entry = {
                "type": None,
                "category": None,
                "origin": None,
                "message": "##################################################",
                "is_separator": True,
                "is_json": False,
                "data": None,
                "id": store.log_entry_seq,
            }
        else:
            resolved_type = _normalize_log_type(log_type)
            resolved_origin = _resolve_log_origin(origin)
            entry = {
                "type": resolved_type,
                "category": resolved_category,
                "origin": resolved_origin,
                "message": str(message),
                "is_separator": False,
                "is_json": is_json,
                "data": data,
                "id": store.log_entry_seq,
            }
        store.game_log_entries.append(entry)
        overflow = len(store.game_log_entries) - LOG_MAX_ENTRIES
        if overflow > 0:
            store.game_log_entries = store.game_log_entries[overflow:]

    def clear_game_logs():
        """Clears all stored session log entries."""
        store.game_log_entries = []
        store.log_json_expanded = {}

    def escape_renpy_log_text(text: str) -> str:
        """
        Escapes text for safe Ren'Py text display.

        ### Parameters:
        1. text: str
            - Raw text that may contain Ren'Py tag/interpolation characters.

        ### Returns:
        1. str
            - Escaped text safe for Ren'Py text nodes.
        """
        return str(text).replace("{", "{{").replace("}", "}}").replace("[", "[[")

    def format_log_json_summary(data) -> str:
        """
        Builds a short summary label for a JSON tree node.

        ### Parameters:
        1. data: Any
            - Node value.

        ### Returns:
        1. str
            - Compact summary text.
        """
        if isinstance(data, dict):
            return f"{{...}} ({len(data)} keys)"
        if isinstance(data, list):
            return f"[...] ({len(data)} items)"
        if data is None:
            return "null"
        if isinstance(data, bool):
            return "true" if data else "false"
        if isinstance(data, str):
            preview = data if len(data) <= 80 else data[:77] + "..."
            return f'"{preview}"'
        return str(data)

    def is_log_json_expanded(path: str) -> bool:
        """
        Returns whether a JSON tree path is expanded.

        ### Parameters:
        1. path: str
            - Expand-state key for the node.

        ### Returns:
        1. bool
            - True when the node is expanded.
        """
        expanded = getattr(store, "log_json_expanded", None) or {}
        return bool(expanded.get(path, False))

    def toggle_log_json_node(path: str):
        """
        Toggles expand/collapse state for a JSON tree path.

        ### Parameters:
        1. path: str
            - Expand-state key for the node.
        """
        if not hasattr(store, "log_json_expanded") or store.log_json_expanded is None:
            store.log_json_expanded = {}
        store.log_json_expanded[path] = not store.log_json_expanded.get(path, False)
        renpy.restart_interaction()

    def is_log_json_branch(value) -> bool:
        """
        Returns whether a value should render as an expandable branch.

        ### Parameters:
        1. value: Any
            - Node value.

        ### Returns:
        1. bool
            - True for dict/list branches.
        """
        return isinstance(value, (dict, list))

    def get_log_json_tree_rows(data, path: str, depth: int = 0):
        """
        Flattens a JSON tree into currently visible rows for journal rendering.

        Ren'Py screens cannot recurse via ``use``, so expand state is resolved
        in Python and returned as a flat row list.

        ### Parameters:
        1. data: Any
            - Current tree node.
        2. path: str
            - Expand-state path prefix for this node.
        3. depth: int (default: 0)
            - Visual indent depth.

        ### Returns:
        1. List[Dict]
            - Visible rows with path, key, summary, depth and branch flags.
        """
        rows = []

        if isinstance(data, dict):
            items = [(str(key), value) for key, value in data.items()]
        elif isinstance(data, list):
            items = [("[" + str(index) + "]", value) for index, value in enumerate(data)]
        else:
            return [{
                "path": path,
                "key": None,
                "summary": format_log_json_summary(data),
                "depth": depth,
                "is_branch": False,
                "expanded": False,
            }]

        for key, value in items:
            child_path = path + "." + key
            branch = is_log_json_branch(value)
            expanded = is_log_json_expanded(child_path) if branch else False
            rows.append({
                "path": child_path,
                "key": key,
                "summary": format_log_json_summary(value),
                "depth": depth,
                "is_branch": branch,
                "expanded": expanded,
            })
            if branch and expanded:
                rows.extend(get_log_json_tree_rows(value, child_path, depth + 1))

        return rows

    def get_filtered_game_logs(log_type=None, category=None, origin=None):
        """
        Returns filtered log entries, newest first.

        ### Parameters:
        1. log_type: Optional[str]
            - Filter by type, or None/"all" for no type filter.
        2. category: Optional[str]
            - Filter by category, or None/"all" for no category filter.
        3. origin: Optional[str]
            - Filter by origin, or None/"all" for no origin filter.

        ### Returns:
        1. List[Dict]
            - Matching log entries, newest first.
        """
        entries = list(getattr(store, "game_log_entries", []) or [])
        type_filter = None if log_type in (None, "", "all") else str(log_type).lower()
        category_filter = None if category in (None, "", "all") else str(category)
        origin_filter = None if origin in (None, "", "all") else str(origin)

        result = []
        for entry in reversed(entries):
            if entry.get("is_separator"):
                result.append(entry)
                continue
            if type_filter is not None and entry.get("type") != type_filter:
                continue
            if category_filter is not None and entry.get("category") != category_filter:
                continue
            if origin_filter is not None and entry.get("origin") != origin_filter:
                continue
            result.append(entry)
        return result

    def get_log_categories():
        """
        Returns sorted unique categories from stored logs.

        ### Returns:
        1. List[str]
            - Category labels present in the log store.
        """
        categories = set()
        for entry in getattr(store, "game_log_entries", []) or []:
            category = entry.get("category")
            if category:
                categories.add(category)
        return sorted(categories)

    def get_log_origins():
        """
        Returns sorted unique origins from stored logs.

        ### Returns:
        1. List[str]
            - Origin labels present in the log store.
        """
        origins = set()
        for entry in getattr(store, "game_log_entries", []) or []:
            origin = entry.get("origin")
            if origin:
                origins.add(origin)
        return sorted(origins)

    def format_game_log_entry(entry) -> str:
        """
        Formats a log entry for journal display with color tags.

        ### Parameters:
        1. entry: Dict
            - A stored log entry.

        ### Returns:
        1. str
            - Ren'Py-tagged display string.
        """
        if entry.get("is_separator"):
            return "{color=#888888}────────────────────────{/color}"

        log_type = _normalize_log_type(entry.get("type", "info"))
        color = LOG_TYPE_COLORS.get(log_type, "#000000")
        type_label = escape_renpy_log_text(f"[{log_type.upper()}]")
        parts = [f"{{color={color}}}{type_label}{{/color}}"]

        category = entry.get("category")
        if category:
            category_label = escape_renpy_log_text(f"[{category}]")
            parts.append(f"{{color=#666666}}{category_label}{{/color}}")

        origin = entry.get("origin")
        if origin:
            parts.append(f"{{color=#888888}}{escape_renpy_log_text(origin)}{{/color}}")

        message = entry.get("message", "")
        if entry.get("is_json"):
            parts.append(escape_renpy_log_text(str(message)))
        else:
            parts.append(escape_renpy_log_text(message))
        return " ".join(parts)

    def cycle_log_filter_value(filter_key: str):
        """
        Cycles a journal log filter to the next available value.

        ### Parameters:
        1. filter_key: str
            - One of "type", "category", or "origin".
        """
        if filter_key == "type":
            options = ["all"] + list(LOG_TYPES)
            current = getattr(store, "log_filter_type", "all")
            index = options.index(current) if current in options else 0
            store.log_filter_type = options[(index + 1) % len(options)]
        elif filter_key == "category":
            options = ["all"] + get_log_categories()
            current = getattr(store, "log_filter_category", "all")
            if current not in options:
                current = "all"
            index = options.index(current)
            store.log_filter_category = options[(index + 1) % len(options)]
        elif filter_key == "origin":
            options = ["all"] + get_log_origins()
            current = getattr(store, "log_filter_origin", "all")
            if current not in options:
                current = "all"
            index = options.index(current)
            store.log_filter_origin = options[(index + 1) % len(options)]

    def log_separator():
        """
        Prints a plain separator line and stores it without type metadata.
        """
        print("##################################################")
        _append_log_entry(
            "##################################################",
            is_separator=True,
        )

    def log_json(key: str, value: Any, *, log_type: str = "info", category=None, origin=None):
        """
        Prints a key and JSON-like value and stores a structured tree entry.

        Console output keeps a normal pretty-printed dump. The journal stores
        structured data for an expandable inline tree.

        ### Parameters:
        1. key: str
            - The key to print.
        2. value: Any
            - The value to pretty-print / store.
        3. log_type: str (default: "info")
            - Log severity type.
        4. category: Optional[str]
            - Optional category label.
        5. origin: Optional[str]
            - Explicit origin override.
        """
        resolved_type = _normalize_log_type(log_type)
        resolved_origin = _resolve_log_origin(origin)
        print()
        print(_format_log_prefix(resolved_type, category, resolved_origin) + key + ":")
        pprint.pprint(value, compact=False)
        _append_log_entry(
            str(key),
            log_type=resolved_type,
            category=category,
            origin=resolved_origin,
            data=_prepare_log_json_data(value),
            is_json=True,
        )

    def log_val(key: str, *values: Any, log_type: str = "info", category=None, origin=None):
        """
        Prints a key and value and stores it in the session log.

        ### Parameters:
        1. key: str
            - The key to print.
        2. values: Any
            - One or more values to print.
        3. log_type: str (default: "info")
            - Log severity type.
        4. category: Optional[str]
            - Optional category label.
        5. origin: Optional[str]
            - Explicit origin override.
        """
        value = ", ".join(map(str, values))
        resolved_type = _normalize_log_type(log_type)
        resolved_origin = _resolve_log_origin(origin)
        message = f"{key}: {value}"
        print(_format_log_prefix(resolved_type, category, resolved_origin) + message)
        _append_log_entry(message, log_type=resolved_type, category=category, origin=resolved_origin)

    def log(msg: str, *, log_type: str = "info", category=None, origin=None):
        """
        Prints a message and stores it in the session log.

        ### Parameters:
        1. msg: str
            - The message to print.
        2. log_type: str (default: "info")
            - Log severity type.
        3. category: Optional[str]
            - Optional category label.
        4. origin: Optional[str]
            - Explicit origin override.
        """
        resolved_type = _normalize_log_type(log_type)
        resolved_origin = _resolve_log_origin(origin)
        message = str(msg)
        print(_format_log_prefix(resolved_type, category, resolved_origin) + message)
        _append_log_entry(message, log_type=resolved_type, category=category, origin=resolved_origin)
        if resolved_type == "error":
            add_notify_message("|ERROR| " + message)

    log_number = 0

    def log_count(msg: str, start=False):
        if start:
            log_number = 0

        log_number += 1
        log_val(msg, log_number)

init -1 python:
    test_events = EventStorage("test_events", "misc")

# init 1 python:
    # test_events.add_event(
    #     Event(3, "test_event",
    #         Pattern("main", "images/background/school building/9 0 1.webp"),
    #         thumbnail = "images/background/school building/9 0 1.webp"),
    # )

label test_label():

    $ hide_all()

    call call_available_event(test_events) from test_label_1

    jump map_entry

   
label test_event (**kwargs):
    $ begin_event(**kwargs)

    $ luna = Person["luna_clark"]
    $ luna.register_paperdoll(level = 10, mood = "happy", mouth = "closed")
    $ paperdoll_manager.set_background("images/background/school building/9 0 1.webp", blur = True)
    $ luna.display(PDAMove(alignX = 0.5, duration = 2.0))
    $ renpy.pause()
    $ luna.display(PDAImage(level = 9), PDABlur(10.0, duration = 3.0))
    $ paperdoll_manager.set_background("images/background/school building/9 0 1.webp", blur = False)
    $ renpy.pause()

    $ end_event('new_daytime', **kwargs)

label show_paperdoll_test():

    $ hide_all()

    $ paperdoll_test_character = ""
    $ paperdoll_test_char_var = "$"
    $ paperdoll_test_pose = -1
    $ paperdoll_test_outfit = ""
    $ paperdoll_test_level = -1
    $ paperdoll_test_state = ""
    $ paperdoll_test_emotion = ""
    $ paperdoll_test_mouth = ""

    $ old_paperdoll_test_character = paperdoll_test_character
    $ old_paperdoll_test_pose = paperdoll_test_pose
    $ old_paperdoll_test_outfit = paperdoll_test_outfit
    $ old_paperdoll_test_level = paperdoll_test_level
    $ old_paperdoll_test_state = paperdoll_test_state
    $ old_paperdoll_test_emotion = paperdoll_test_emotion
    $ old_paperdoll_test_mouth = paperdoll_test_mouth

    $ paperdoll_test_override_y_2 = 0.0
    $ paperdoll_test_override_x_2 = 0.0

    $ paperdoll_test_state_values = []
    $ paperdoll_test_level_values = []

    $ paperdoll_show_selection = True
    $ paperdoll_show_values = True
    $ paperdoll_show_presets = True
    $ paperdoll_active_field = None
    $ paperdoll_active_preset = None
    
    $ paperdoll_alignX = 1.0
    $ paperdoll_alignY = 0.0
    $ paperdoll_rotation = 0.0
    $ paperdoll_zoom = 1.0
    $ paperdoll_blur = 0.0
    $ paperdoll_flip = False

    $ paperdoll_sync_buffers()

    $ init_paperdoll_manager()
    $ charact = None

    while(True):
        $ log_separator()
        call screen paperdoll_test_screen()

        $ log_val("paperdoll_test_character", paperdoll_test_character)
        $ log_val("paperdoll_test_char_var", paperdoll_test_char_var)
        $ log_val("paperdoll_test_pose", paperdoll_test_pose)
        $ log_val("paperdoll_test_outfit", paperdoll_test_outfit)
        $ log_val("paperdoll_test_level", paperdoll_test_level)
        $ log_val("paperdoll_test_emotion", paperdoll_test_emotion)
        $ log_val("paperdoll_test_mouth", paperdoll_test_mouth)
        $ log_val("paperdoll_test_state", paperdoll_test_state)
        $ log_val("character", charact)

        if paperdoll_test_character != "" and paperdoll_test_pose > 0 and paperdoll_test_outfit != "" and paperdoll_test_level >= 0 and paperdoll_test_emotion != "" and paperdoll_test_mouth != "":
            $ log_val("displaying paperdoll", paperdoll_test_character)
            if old_paperdoll_test_character != paperdoll_test_character or charact == None:
                $ log_val("registering paperdoll", paperdoll_test_character)
                $ unload_paperdoll_manager()
                $ init_paperdoll_manager()
                $ kwargs = {}
                $ charact = find_person(paperdoll_test_character)
                $ log_val("character", charact)
                $ charact.register_paperdoll()
                
                $ paperdoll_obj = paperdoll_manager.get_obj(paperdoll_test_character)

            $ paperdoll_test_char_var_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ")})

            if paperdoll_test_char_var not in paperdoll_test_char_var_values and len(paperdoll_test_char_var_values) > 0:
                $ paperdoll_test_char_var = paperdoll_test_char_var_values[0]

            $ paperdoll_test_level_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ")})

            if len(paperdoll_test_level_values) > 0 and (len(paperdoll_test_level_values) > 1 or paperdoll_test_level_values[0] != "$"):
                $ paperdoll_test_level_values = sorted(int(i) for i in paperdoll_test_level_values)
                if paperdoll_test_level not in paperdoll_test_level_values:
                    $ paperdoll_test_level = paperdoll_test_level_values[0]

            $ paperdoll_test_state_values = list({s.replace(".png", "").replace(".webp", "").replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} {paperdoll_test_level} ", "").replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} $ ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} {paperdoll_test_level} ") or s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} $ ")})

            if paperdoll_test_state not in paperdoll_test_state_values and len(paperdoll_test_state_values) > 0:
                $ paperdoll_test_state = paperdoll_test_state_values[0]

            if paperdoll_test_state == "$":
                $ paperdoll_test_state = ""

            $ log_val("paperdoll_test_state_values", paperdoll_test_state_values)
            $ log_val("paperdoll_test_state", paperdoll_test_state)

            if paperdoll_active_preset is not None:
                $ paperdoll_sync_preset_to_test_state()

            $ charact.display(*paperdoll_build_test_display_actions())
screen paperdoll_test_screen():
    vbox:
        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_selection", not paperdoll_show_selection), Return()]

            if paperdoll_show_selection:
                $ paperdoll_selector_character = list({s.replace("images/paperdoll/", "").split("/")[0] for s in renpy.list_files() if s.startswith("images/paperdoll/")})
                frame:
                    area(0, 0, 300, 900)
                    background Solid("#fff6")
                    vbox:
                        text "Characters" style "journal_text"
                        if paperdoll_test_character != "":
                            $ log_val("paperdoll_test_character", paperdoll_test_character)
                            $ log_val("paperdoll_selector_character", paperdoll_selector_character)
                            hbox:
                                if paperdoll_selector_character.index(paperdoll_test_character) != 0:
                                    textbutton "<":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[paperdoll_selector_character.index(paperdoll_test_character) - 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                else:
                                    textbutton "<":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[len(paperdoll_selector_character) - 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                if paperdoll_selector_character.index(paperdoll_test_character) != len(paperdoll_selector_character) - 1:
                                    textbutton ">":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[paperdoll_selector_character.index(paperdoll_test_character) + 1]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                                else:
                                    textbutton ">":
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_character", paperdoll_selector_character[0]), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                        viewport id "paperdoll_selector_characters":
                            mousewheel True
                            draggable "touch"
                            vbox:
                                for character in paperdoll_selector_character:
                                    if character == paperdoll_test_character:
                                        textbutton character:
                                            text_style "buttons_active"
                                            action NullAction()
                                    else:
                                        textbutton character:
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_character", character), SetVariable("paperdoll_test_char_var", ""), SetVariable("paperdoll_test_pose", -1), SetVariable("paperdoll_test_outfit", ""), SetVariable("paperdoll_test_level", 1), SetVariable("paperdoll_test_emotion", ""), SetVariable("paperdoll_test_mouth", ""), SetVariable("paperdoll_test_state", ""), SetVariable("paperdoll_test_state_values", []), Return()]
                        vbar value YScrollValue("paperdoll_selector_characters"):
                            unscrollable "hide"
                            xalign 1.05


                if paperdoll_test_character != "":
                    $ paperdoll_selector_char_var = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} ")})
                    if len(paperdoll_selector_char_var) == 0:
                        $ paperdoll_selector_char_var = ["$"]
                    if len(paperdoll_selector_char_var) == 1:
                        $ paperdoll_test_char_var = paperdoll_selector_char_var[0]

                    if len(paperdoll_selector_char_var) > 1:
                        frame:
                            area(0, 0, 200, 900)
                            background Solid("#fff6")
                            vbox:
                                text "char_var" style "journal_text"
                                if paperdoll_test_char_var != "":
                                    hbox:
                                        if paperdoll_selector_char_var.index(paperdoll_test_char_var) != 0:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[paperdoll_selector_char_var.index(paperdoll_test_char_var) - 1]), Return()]
                                        else:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[len(paperdoll_selector_char_var) - 1]), Return()]
                                        if paperdoll_selector_char_var.index(paperdoll_test_char_var) != len(paperdoll_selector_char_var) - 1:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[paperdoll_selector_char_var.index(paperdoll_test_char_var) + 1]), Return()]
                                        else:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_char_var", paperdoll_selector_char_var[0]), Return()]
                                viewport id "paperdoll_selector_char_var":
                                    mousewheel True
                                    draggable "touch"
                                    vbox:
                                        for cv in paperdoll_selector_char_var:
                                            if cv == paperdoll_test_char_var:
                                                textbutton cv:
                                                    text_style "buttons_active"
                                                    action NullAction()
                                            else:
                                                textbutton cv:
                                                    text_style "buttons_idle"
                                                    action [SetVariable("paperdoll_test_char_var", cv), Return()]
                                vbar value YScrollValue("paperdoll_selector_char_var"):
                                    unscrollable "hide"
                                    xalign 1.05

                if paperdoll_test_character != "":
                    frame:
                        area(0, 0, 120, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Pose" style "journal_text"
                            hbox:
                                vbox:
                                    if paperdoll_test_pose > 1:
                                        textbutton "-":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", paperdoll_test_pose - 1), Return()]
                                    else:
                                        textbutton "-":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", 34), Return()]
                                    for i in range(1, 18):
                                        if i == paperdoll_test_pose:
                                            textbutton str(i):
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton str(i):
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_pose", i), Return()]
                                vbox:
                                    if paperdoll_test_pose < 34:
                                        textbutton "+":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", paperdoll_test_pose + 1), Return()]
                                    else:
                                        textbutton "+":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_pose", 1), Return()]
                                    for i in range(18, 35):
                                        if i == paperdoll_test_pose:
                                            textbutton str(i):
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton str(i):
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_pose", i), Return()]
                            
                if paperdoll_test_pose > 0:
                    $ log_val("paperdoll_test_char_var", paperdoll_test_char_var)
                    $ paperdoll_selector_outfit = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ")})
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Outfits" style "journal_text"
                            if paperdoll_test_outfit != "":
                                hbox:
                                    if paperdoll_selector_outfit.index(paperdoll_test_outfit) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[paperdoll_selector_outfit.index(paperdoll_test_outfit) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[len(paperdoll_selector_outfit) - 1]), Return()]
                                    if paperdoll_selector_outfit.index(paperdoll_test_outfit) != len(paperdoll_selector_outfit) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[paperdoll_selector_outfit.index(paperdoll_test_outfit) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_outfit", paperdoll_selector_outfit[0]), Return()]
                            viewport id "paperdoll_selector_outfits":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for outfit in paperdoll_selector_outfit:
                                        if outfit == paperdoll_test_outfit:
                                            textbutton outfit:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton outfit:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_outfit", outfit), Return()]
                            vbar value YScrollValue("paperdoll_selector_outfits"):
                                unscrollable "hide"
                                xalign 1.05
                                        
                if paperdoll_test_outfit != "":
                    $ paperdoll_test_level_values = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/bottom/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} {paperdoll_test_outfit} ")})
                    if len(paperdoll_test_level_values) > 1 or paperdoll_test_level_values[0] != "$":
                        $ paperdoll_test_level_values = [int(i) for i in paperdoll_test_level_values]
                        $ paperdoll_test_level_values.sort()
                        if paperdoll_test_level not in paperdoll_test_level_values:
                            $ paperdoll_test_level = paperdoll_test_level_values[0]
                        frame:
                            area(0, 0, 200, 900)
                            background Solid("#fff6")
                            vbox:
                                text "Levels" style "journal_text"
                                if isinstance(paperdoll_test_level, int):
                                    hbox:
                                        if paperdoll_test_level_values.index(paperdoll_test_level) != 0:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[paperdoll_test_level_values.index(paperdoll_test_level) - 1]), Return()]
                                        else:
                                            textbutton "<":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[len(paperdoll_test_level_values) - 1]), Return()]
                                        if paperdoll_test_level_values.index(paperdoll_test_level) != len(paperdoll_test_level_values) - 1:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[paperdoll_test_level_values.index(paperdoll_test_level) + 1]), Return()]
                                        else:
                                            textbutton ">":
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_level", paperdoll_test_level_values[0]), Return()]
                                viewport id "paperdoll_selector_levels":
                                    mousewheel True
                                    draggable "touch"
                                    vbox:
                                        for level in paperdoll_test_level_values:
                                            if level == paperdoll_test_level:
                                                textbutton str(level):
                                                    text_style "buttons_active"
                                                    action NullAction()
                                            else:
                                                textbutton str(level):
                                                    text_style "buttons_idle"
                                                    action [SetVariable("paperdoll_test_level", level), Return()]
                                vbar value YScrollValue("paperdoll_selector_levels"):
                                    unscrollable "hide"
                                    xalign 1.05
                            
                    $ paperdoll_selector_emotion = list({s.replace(f"images/paperdoll/{paperdoll_test_character}/top/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ", "").split(" ")[0] for s in renpy.list_files() if s.startswith(f"images/paperdoll/{paperdoll_test_character}/top/{paperdoll_test_character} {paperdoll_test_char_var} {paperdoll_test_pose} ")})
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Emotions" style "journal_text"
                            if paperdoll_test_emotion != "":
                                hbox:
                                    if paperdoll_selector_emotion.index(paperdoll_test_emotion) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[paperdoll_selector_emotion.index(paperdoll_test_emotion) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[len(paperdoll_selector_emotion) - 1]), Return()]
                                    if paperdoll_selector_emotion.index(paperdoll_test_emotion) != len(paperdoll_selector_emotion) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[paperdoll_selector_emotion.index(paperdoll_test_emotion) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_emotion", paperdoll_selector_emotion[0]), Return()]
                            viewport id "paperdoll_selector_emotions":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for emotion in paperdoll_selector_emotion:
                                        if emotion == paperdoll_test_emotion:
                                            textbutton emotion:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton emotion:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_emotion", emotion), Return()]
                            vbar value YScrollValue("paperdoll_selector_emotions"):
                                unscrollable "hide"
                                xalign 1.05
                if paperdoll_test_emotion not in ["pout", "suprised"] and paperdoll_test_emotion != "":
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "Mouths" style "journal_text"
                            if paperdoll_test_mouth != "":
                                hbox:
                                    if paperdoll_test_mouth != "closed":
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "closed"), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "open"), Return()]
                                    if paperdoll_test_mouth != "open":
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "open"), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_mouth", "closed"), Return()]
                            for mouth in ["closed", "open"]:
                                if mouth == paperdoll_test_mouth:
                                    textbutton mouth:
                                        text_style "buttons_active"
                                        action NullAction()
                                else:
                                    textbutton mouth:
                                        text_style "buttons_idle"
                                        action [SetVariable("paperdoll_test_mouth", mouth), Return()]

                if len(paperdoll_test_state_values) > 1:
                    frame:
                        area(0, 0, 200, 900)
                        background Solid("#fff6")
                        vbox:
                            text "States" style "journal_text"
                            if paperdoll_test_state != "":
                                hbox:
                                    if paperdoll_test_state_values.index(paperdoll_test_state) != 0:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[paperdoll_test_state_values.index(paperdoll_test_state) - 1]), Return()]
                                    else:
                                        textbutton "<":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[len(paperdoll_test_state_values) - 1]), Return()]
                                    if paperdoll_test_state_values.index(paperdoll_test_state) != len(paperdoll_test_state_values) - 1:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[paperdoll_test_state_values.index(paperdoll_test_state) + 1]), Return()]
                                    else:
                                        textbutton ">":
                                            text_style "buttons_idle"
                                            action [SetVariable("paperdoll_test_state", paperdoll_test_state_values[0]), Return()]
                            viewport id "paperdoll_selector_states":
                                mousewheel True
                                draggable "touch"
                                vbox:
                                    for state in paperdoll_test_state_values:
                                        if state == paperdoll_test_state:
                                            textbutton state:
                                                text_style "buttons_active"
                                                action NullAction()
                                        else:
                                            textbutton state:
                                                text_style "buttons_idle"
                                                action [SetVariable("paperdoll_test_state", state), Return()]
                            vbar value YScrollValue("paperdoll_selector_states"):
                                unscrollable "hide"
                                xalign 1.05



        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_values", not paperdoll_show_values), Return()]
            if paperdoll_show_values:
                for label, key in [("AlignX", "paperdoll_alignX"), ("AlignY", "paperdoll_alignY"), ("Zoom", "paperdoll_zoom"), ("Blur", "paperdoll_blur")]:
                    textbutton "[label]":
                        text_style "buttons_idle"
                        if paperdoll_active_field == key:
                            text_color "#0f0"
                        action [SetVariable("paperdoll_active_preset", None), SetVariable("paperdoll_active_field", key)]
                    null width 10

                textbutton f"Flip: {paperdoll_flip}":
                    text_style "buttons_idle"
                    action [SetVariable("paperdoll_active_preset", None), SetVariable("paperdoll_flip", not paperdoll_flip), Return()]

        if paperdoll_active_field and paperdoll_show_values:
            hbox:
                text "Edit {}: ".format(paperdoll_active_field)
                input id paperdoll_active_field:
                    value DictInputValue(paperdoll_buf, paperdoll_active_field)
                    length 6
                null width 10
                textbutton "OK":
                    text_style "buttons_idle"
                    action [SetVariable("paperdoll_active_preset", None), Function(paperdoll_apply_buffers), Return()]

        hbox:
            textbutton "^":
                text_style "buttons_idle"
                action [SetVariable("paperdoll_show_presets", not paperdoll_show_presets), Return()]
            if paperdoll_show_presets:
                frame:
                    area (0, 0, 1700, 60)
                    background Solid("#fff6")
                    vbox:
                        viewport id "paperdoll_selector_presets":
                            mousewheel "horizontal"
                            draggable "touch"
                            hbox:
                                if paperdoll_active_preset is None:
                                    textbutton "custom":
                                        text_style "buttons_active"
                                        action NullAction()
                                else:
                                    textbutton "custom":
                                        text_style "buttons_idle"
                                        action [Function(paperdoll_clear_preset), Return()]
                                for preset_key in sorted(paperdoll_presets.keys()):
                                    if preset_key == paperdoll_active_preset:
                                        textbutton preset_key:
                                            text_style "buttons_active"
                                            action NullAction()
                                    else:
                                        textbutton preset_key:
                                            text_style "buttons_idle"
                                            action [Function(paperdoll_sync_preset_to_test_state, preset_key), Return()]
                        bar value XScrollValue("paperdoll_selector_presets"):
                            unscrollable "hide"

    imagebutton:
        idle "icons/stop_idle.webp"
        hover "icons/stop_hover.webp"
        xalign 1.0 yalign 1.0
        action Call("end_paperdoll_test")

init python:
    # Puffer-Strings für die Eingabe
    paperdoll_buf = {}

    def paperdoll_sync_buffers():
        """Aktuelle Float-Werte in die String-Puffer kopieren."""
        paperdoll_buf["paperdoll_alignX"] = str(paperdoll_alignX)
        paperdoll_buf["paperdoll_alignY"] = str(paperdoll_alignY)
        paperdoll_buf["paperdoll_zoom"] = str(paperdoll_zoom)
        paperdoll_buf["paperdoll_blur"] = str(paperdoll_blur)

    def paperdoll_apply_buffers():
        """Puffer-Strings zurück in Float-Variablen schreiben."""
        global paperdoll_alignX, paperdoll_alignY, paperdoll_zoom, paperdoll_blur
        try:
            paperdoll_alignX = float(paperdoll_buf["paperdoll_alignX"])
        except ValueError:
            pass
        try:
            paperdoll_alignY = float(paperdoll_buf["paperdoll_alignY"])
        except ValueError:
            pass
        try:
            paperdoll_zoom = float(paperdoll_buf["paperdoll_zoom"])
        except ValueError:
            pass
        try:
            paperdoll_blur = float(paperdoll_buf["paperdoll_blur"])
        except ValueError:
            pass

    def paperdoll_get_test_pd_obj():
        """
        Returns the active paperdoll object for the current test character, if available.

        ### Returns:
        1. Optional[Paperdoll_Obj]
            - The paperdoll object, or None when it is not registered yet.
        """
        if charact is None or paperdoll_manager is None or paperdoll_test_character == "":
            return None
        try:
            return paperdoll_manager.get_obj(paperdoll_test_character)
        except Exception:
            return None

    class _PaperdollConfigProxy(object):
        """Minimal stand-in for Paperdoll_Obj.config resolution during preset preview."""

        def __init__(self, alignX, alignY, zoom, blur):
            self.config = {
                "alignX": alignX,
                "alignY": alignY,
                "zoom": zoom,
                "blur": blur,
            }

    def paperdoll_flatten_preset(preset_key, **overrides):
        """
        Expands a preset into a flat action list, recursively resolving nested presets.

        ### Parameters:
        1. preset_key: str
            - The preset key to flatten.
        2. **overrides
            - Optional override values passed to nested preset actions.

        ### Returns:
        1. List[PDAction]
            - Flat list of non-preset actions in execution order.
        """
        result = []
        for action in get_preset_with_overrides(preset_key, **overrides):
            if action.key == "preset":
                result.extend(paperdoll_flatten_preset(action.preset, **action.values))
            else:
                result.append(action)
        return result

    def paperdoll_format_preset_actions(preset_key):
        """
        Formats the flattened preset actions as a comma-separated string for UI display.

        ### Parameters:
        1. preset_key: str
            - The preset key to format.

        ### Returns:
        1. str
            - Comma-separated action keys, e.g. "move, blur, flip".
        """
        return ", ".join(action.key for action in paperdoll_flatten_preset(preset_key))

    def paperdoll_apply_action_to_test_state(action, alignX, alignY, zoom, blur, flip, config_proxy):
        """
        Applies a single paperdoll action to simulated test state values.

        ### Parameters:
        1. action: PDAction
            - The action to apply.
        2. alignX: float
            - Current alignX value.
        3. alignY: float
            - Current alignY value.
        4. zoom: float
            - Current zoom value.
        5. blur: float
            - Current blur value.
        6. flip: bool
            - Current flip value.
        7. config_proxy: _PaperdollConfigProxy
            - Config proxy used for partial action resolution.

        ### Returns:
        1. Tuple[float, float, float, float, bool]
            - Updated alignX, alignY, zoom, blur and flip values.
        """
        if action.key == "move":
            alignX, alignY, zoom, _ = action.get_values(config_proxy)
            config_proxy.config["alignX"] = alignX
            config_proxy.config["alignY"] = alignY
            config_proxy.config["zoom"] = zoom
        elif action.key == "blur":
            blur, _ = action.get_values(config_proxy)
            config_proxy.config["blur"] = blur
        elif action.key == "flip":
            flip = action.flip < 0

        return alignX, alignY, zoom, blur, flip

    def paperdoll_sync_preset_to_test_state(preset_key=None):
        """
        Selects a preset and syncs editable test fields from its resolved actions.

        Move, blur and flip values are simulated sequentially, matching run_paperdoll_actions.
        Other action types remain part of the preset and are shown in the UI, but have no editable field.

        ### Parameters:
        1. preset_key: Optional[str]
            - Preset key to activate. When omitted, re-syncs the currently active preset.
        """
        global paperdoll_active_preset, paperdoll_alignX, paperdoll_alignY, paperdoll_zoom, paperdoll_blur, paperdoll_flip
        if preset_key is not None:
            paperdoll_active_preset = preset_key
        if paperdoll_active_preset is None:
            return

        pd_obj = paperdoll_get_test_pd_obj()
        if pd_obj is not None:
            alignX = pd_obj.config["alignX"]
            alignY = pd_obj.config["alignY"]
            zoom = pd_obj.config["zoom"]
            blur = pd_obj.config["blur"]
        else:
            alignX = paperdoll_alignX
            alignY = paperdoll_alignY
            zoom = paperdoll_zoom
            blur = paperdoll_blur

        flip = paperdoll_flip
        config_proxy = _PaperdollConfigProxy(alignX, alignY, zoom, blur)

        for action in paperdoll_flatten_preset(paperdoll_active_preset):
            alignX, alignY, zoom, blur, flip = paperdoll_apply_action_to_test_state(
                action, alignX, alignY, zoom, blur, flip, config_proxy
            )

        paperdoll_alignX = alignX
        paperdoll_alignY = alignY
        paperdoll_zoom = zoom
        paperdoll_blur = blur
        paperdoll_flip = flip
        paperdoll_sync_buffers()

    def paperdoll_build_test_display_actions():
        """
        Builds the paperdoll action list for the current test screen state.

        ### Returns:
        1. List[PDAction]
            - Actions passed to Person.display for the current test configuration.
        """
        image_action = PDAImage(
            char_var = paperdoll_test_char_var,
            pose = paperdoll_test_pose,
            outfit = paperdoll_test_outfit,
            level = paperdoll_test_level,
            state = paperdoll_test_state,
            mood = paperdoll_test_emotion,
            mouth = paperdoll_test_mouth,
        )

        if paperdoll_active_preset is not None:
            return [image_action, PDAPreset(paperdoll_active_preset)]

        return [
            image_action,
            PDAMove(alignX = paperdoll_alignX, alignY = paperdoll_alignY, zoom = paperdoll_zoom),
            PDABlur(blur = paperdoll_blur),
            PDAFlip(flip = paperdoll_flip),
        ]

    def paperdoll_clear_preset():
        """Clears the active preset selection without changing the current move values."""
        global paperdoll_active_preset
        paperdoll_active_preset = None

label end_paperdoll_test():
    $ unload_paperdoll_manager()
    $ hide_all()
    jump map_entry


init -6 python:
    
    ########################
    # region CLASSES ----- #
    ########################

    class Modifier_Obj:
        """
        Modifiers are used to change the rate of a stat change. They are mostly used when a stat changes by an event.
        Modifiers are stored in a dictionary, with the key being the name of the modifier, and the value being the modifier object.

        ### Attributes:
        1. mod_type: 
            - The type of modifier. Can be "+", "*", or "%".
            - "+" adds a flat value to the stat.
            - "*" multiplies the stat by a value.
            - "%" multiplies the stat by a percentage.
        2. value:
            - The value of the modifier. This is the value that is used to calculate the change in the stat.

        ### Methods:
        1. get_name() -> str:
            - Gets the name of the modifier.
            - Returns the name of the modifier.
        2. get_change() -> str:
            - Gets the change in the stat based on the mod_type and value.
            - Returns the change in the stat.
        3. calculate_change(base_value: num) -> float:
            - Calculates the change in the stat based on the mod_type and value.
            - Returns the change in the stat.
        """

        def __init__(self, name: str, mod_type: str, value: num):
            self._name = name
            self._mod_type = mod_type
            self._value = value

        def get_name(self) -> str:
            """
            Gets the name of the modifier.

            ### Returns:
            1. str
                - The name of the modifier.
            """

            return self._name

        def get_value(self) -> num:
            """
            Gets the value of the modifier.

            ### Returns:
            1. num
                - The value of the modifier.
            """

            return self._value

        def set_value(self, value: num):
            """
            Sets the value of the modifier.

            ### Parameters:
            1. value: num
                - The value of the modifier.
            """

            self._value = value

        def get_mod_type(self) -> str:
            """
            Gets the operator/type of the modifier ("+", "*", "value_percent",
            "range_percent", "gated_percent"; "%" is the legacy alias).

            ### Returns:
            1. str
                - The modifier's operator.
            """

            return self._mod_type

        def get_change(self) -> str:
            """
            Gets the change in the stat based on the mod_type and value.

            ### Returns:
            1. float
                - The change in the stat.
            """

            if self._mod_type == "%":
                self.mod_type = "value_percent"

            if self._mod_type == "*":
                return f"x {self._value}"
            elif self._mod_type == "value_percent":
                return f"{self._value}% of the value"
            elif self._mod_type == "range_percent":
                return f"{self._value}% of the entire range"
            elif self._mod_type == "gated_percent":
                return f"{self._value}% of the gated range"

            else:
                return str(self._value)

        def calculate_change(self, base_value: num, range_stat: str = None) -> float:
            """
            Calculates the change in the stat based on the mod_type and value.

            ### Parameters:
            1. base_value: num
                - The base value of the stat. This is the value that is being changed.
            2. range_stat: str (optional)
                - Stat / situation bar key used for ``range_percent`` and
                    ``gated_percent`` range lookups.

            ### Returns:
            1. float
                - The change in the stat.
            """

            if self._mod_type == "%":
                self.mod_type = "value_percent"

            if self._mod_type == "+":
                return self._value
            elif self._mod_type == "*":
                return base_value * self._value
            elif self._mod_type == "value_percent":
                return base_value / 100 * self._value
            elif self._mod_type == "range_percent":
                full_range = get_full_range(range_stat) if range_stat else 0
                return self._value / 100 * full_range + base_value
            elif self._mod_type == "gated_percent":
                gated_range = get_gated_range(range_stat, self._value) if range_stat else 0
                return self._value / 100 * gated_range + base_value
            else:
                return base_value

    # endregion
    ########################

    ##############################
    # region Modifier Beef ----- #
    ##############################

    def get_modifier_collection(collection: str | List[str] = 'default') -> Dict[str, Dict[str, Modifier_Obj]]:
        """
        Gets the collection of modifiers.

        ### Parameters:
        1. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then multiple collections are returned.

        ### Returns:
        1. Dict[str, Dict[str, Modifier_Obj]]
            - The collection of modifiers. The key is the stat, and the value is a dictionary of modifiers.
        """
        
        if not contains_game_data('stat_modifier'):
            set_game_data('stat_modifier', {})

        modifier = get_game_data('stat_modifier')

        if isinstance(collection, str):
            collection = [collection]

        output = []

        for col in collection:
            if col not in modifier.keys():
                modifier[col] = {}

            output.append(modifier[col])

        return output

    def prepare_for_modifier(key: str, stat: str = "all", collection: str | List[str] = 'default'):
        """
        Prepares the game data for a modifier. This is used to make sure that the game data is ready for a modifier to be added.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
            - if "all", then the modifier is applied to all stats.
        3. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then multiple collections are prepared.
        """

        modifier_list = get_modifier_collection(collection)

        for modifier in modifier_list:
            if stat not in modifier.keys():
                modifier[stat] = {}

            modifier[stat][key] = None

    def get_modifier_lists(stat: str, collection: str | List[str] = 'default') -> Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]:
        """
        Gets a list of modifiers from the game data or from the character.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]
            - A dictionary of modifiers. The key is the name of the modifier, and the value is the modifier object.
        """

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None or len(modifier_list) == 0:
            return {}

        output = {}

        for modifier in modifier_list:
            if stat in modifier.keys():
                output = update_dict(output, modifier[stat])
                # output.append(modifier[stat])
            if stat != 'all' and 'all' in modifier.keys():
                output = update_dict(output, modifier['all'])
                # output.append(modifier['all'])

        # Drop soft-deleted / placeholder None entries so callers can iterate safely
        return {key: value for key, value in output.items() if value != None}

    def get_total_modifier_change(mod_obj: Modifier_Obj, base_value: num, collection: str = 'default', range_stat: str = None) -> float:
        """
        Gets the total change in the stat based on the modifier.
        DOES NOT USE THIS METHOD! Use change_stats_with_modifier() instead.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. base_value: num
            - The base value of the stat. This is the value that is being changed.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        5. range_stat: str (optional)
            - Override key used for range-based modifier operators.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        value = 0
        value += mod_obj.calculate_change(base_value, range_stat=range_stat)

        return value

    def get_total_stat_modifier_change(stat: str, base_value: num, collection: str = 'default', range_stat: str = None) -> float:
        """
        Gets the total change in the stat based on all of the modifiers.
        DOES NOT USE THIS METHOD! Use change_stats_with_modifier() instead.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. base_value: num
            - The base value of the stat. This is the value that is being changed.
        3. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        4. range_stat: str (optional)
            - Override key used for range-based modifier operators.
            - Defaults to ``stat``.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        modifier = get_modifier_lists(stat, collection)
        target_range_stat = range_stat if range_stat is not None else stat

        value = 0
        if modifier != None:
            for key in modifier.keys():
                value += get_total_modifier_change(modifier[key], base_value, collection, range_stat=target_range_stat)

        return value

    def apply_stat_modifier(stat: str, value: num, collection: str = 'default', range_stat: str = None) -> float:
        """
        Applies the stat modifier to the value.
        DOES NOT USE THIS METHOD! Use change_stats_with_modifier() instead.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. value: num
            - The value of the stat. This is the value that is being changed.
        3. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        4. range_stat: str (optional)
            - Override key used for range-based modifier operators.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        value = value + get_total_stat_modifier_change(stat, value, collection, range_stat=range_stat)
        
        return value

    def sort_payroll_modifier(weekly: Dict[str, Modifier_Obj], monthly: Dict[str, Modifier_Obj]) -> Tuple[List[Tuple[str, int, int]], List[Tuple[str, int, int]], int, int]:
        """
        Sorts the payroll modifier into positive and negative income.

        ### Parameters:
        1. weekly: Dict[str, Modifier_Obj]
            - The weekly payroll modifier.
        2. monthly: Dict[str, Modifier_Obj]
            - The monthly payroll modifier.

        ### Returns:
        1. Tuple[List[Tuple[str, int, int]], List[Tuple[str, int, int]], int, int]
            - A tuple of the positive income list, negative income list, net weekly income, and net monthly income.
        """

        positive_income = {}
        negative_income = {}

        net_weekly = 0
        net_monthly = 0

        if weekly != None:
            for modifier in weekly.values():
                if modifier == None:
                    continue
                key = modifier.get_name()
                net_weekly += modifier.get_value()
                if modifier.get_value() > 0:
                    if key not in positive_income.keys():
                        positive_income[key] = (0, 0)
                    income = positive_income[key]
                    positive_income[key] = (income[0] + modifier.get_value(), income[1])
                else:
                    if key not in negative_income.keys():
                        negative_income[key] = (0, 0)
                    income = negative_income[key]
                    negative_income[key] = (income[0] + modifier.get_value(), income[1])

        if monthly != None:
            for modifier in monthly.values():
                if modifier == None:
                    continue
                key = modifier.get_name()
                net_monthly += modifier.get_value()
                if modifier.get_value() > 0:
                    if key not in positive_income.keys():
                        positive_income[key] = (0, 0)
                    income = positive_income[key]
                    positive_income[key] = (income[0], income[1] + modifier.get_value())
                else:
                    if key not in negative_income.keys():
                        negative_income[key] = (0, 0)
                    income = negative_income[key]
                    negative_income[key] = (income[0], income[1] + modifier.get_value())

        positive_income_list = [(key, value[0], value[1]) for key, value in positive_income.items()]
        negative_income_list = [(key, value[0], value[1]) for key, value in negative_income.items()]

        return (positive_income_list, negative_income_list, net_weekly, net_monthly)

    # endregion
    ##############################

    ###########################################
    # region Modifier Getter and Setter ----- #
    ###########################################

    def set_modifier(key: str, mod_obj: Modifier_Obj, *, stat: str = "all", collection: str | List[str] = 'default'):
        """
        Sets a modifier in the game data.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
            - if "all", then the modifier is applied to all stats.
        3. mod_obj: Modifier_Obj
            - The modifier object that is being added.
        4. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then the modifier is added to multiple collections.
        """

        prepare_for_modifier(key, stat, collection)

        modifier_list = get_modifier_collection(collection)

        for modifier in modifier_list:
            modifier[stat][key] = mod_obj

    def remove_modifier(key: str, stat: str = "all", collection: str = 'default'):
        """
        Removes a modifier from the game data.

        Deletes the key from the collection entirely. Soft-deleting to None is
        not used, because iterators (e.g. payroll sorting / stat application)
        expect Modifier_Obj values and crash on None entries.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then the modifier is removed from multiple collections.
        """

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None or len(modifier_list) == 0:
            return

        modifier = modifier_list[0]
        remove_modifier = modifier
        if stat not in remove_modifier.keys():
            return
        if key not in remove_modifier[stat].keys():
            return
        
        del remove_modifier[stat][key]

    def track_managed_modifier(key: str, mod_obj: Modifier_Obj, owner: str, *, category: str = None, stat: str = "all", collection: str = 'default'):
        """
        Apply a modifier **and** register it with the lifecycle registry so it can
        never orphan.

        Use this for modifiers set **outside** a Situation (mod / systems code) —
        the counterpart to what the situation types do automatically. Call it once
        when the modifier is activated: it sets the modifier and records an ownership
        entry. Then, from a label registered via ``register_start_method``, call
        ``keep_managed_modifier(key)`` for this specific modifier on every load wave so
        the entry is re-pinged and survives the sweep. Keep each modifier on its own —
        stop re-pinging a key (feature off, key retired, mod disabled) and the next
        ``finalize_check`` sweep removes it — no orphan.

        Both the modifier collection (``stat_modifier`` game data) and the registry
        entry persist across saves, so the wave hook only needs to KEEP-ping — it
        does not have to re-apply the modifier.

        ### Parameters:
        1. key: str
            - Modifier key. Globally unique; also the registry entry key.
        2. mod_obj: Modifier_Obj
            - The modifier to apply.
        3. owner: str
            - Owning system / mod id, recorded on the entry for clear/bookkeeping.
        4. category: str (default = owner)
            - Instance id within the owner (for finer-grained keep/clear).
        5. stat: str (default "all")
            - Target stat, or a ``situation:<key>:<bar>`` pseudo-stat key.
        6. collection: str (default "default")
            - Modifier collection. A single collection only (symmetric with the registry's remove); for several, call once per collection with distinct keys.
        """

        set_modifier(key, mod_obj, stat=stat, collection=collection)
        lifecycle_registry.track(
            key,
            owner=owner,
            category=category if category is not None else owner,
            kind="modifier",
            stat=stat,
            collection=collection,
            op=mod_obj.get_mod_type(),
            value=mod_obj.get_value(),
        )

    def keep_managed_modifier(key: str):
        """
        Keep **one** managed modifier alive for this load wave.

        Call this from a label registered via ``register_start_method`` (those run
        inside the lifecycle check wave), **once per modifier your mod still wants**,
        from the code path that decides it should still exist. It pings KEEP on that
        single entry so the finalize sweep spares it.

        Keep every modifier individually — never in bulk. A modifier is only spared
        while something actively re-affirms it each wave: stop pinging a key (feature
        turned off, key retired, mod disabled) and the sweep removes it. A blanket
        "keep all my entries" would instead resurrect stale keys forever and resurface
        the very orphans the registry exists to prevent. If the key is not tracked
        (never activated, or already swept), this is a harmless no-op.

        ### Parameters:
        1. key: str
            - The modifier / registry entry key passed to ``track_managed_modifier``.
        """

        lifecycle_registry.ping(key, KEEP)

    def remove_managed_modifier(key: str):
        """
        Deactivate a managed modifier: remove it from the modifier system and drop
        its registry entry.

        Use this when the owner intentionally turns the modifier off (as opposed to
        the automatic sweep that fires when the owner disappears entirely).

        ### Parameters:
        1. key: str
            - The modifier / registry entry key.
        """

        lifecycle_registry.ping(key, REMOVE)

    def get_modifier(key: str, stat: str = "all", collection: str = 'default') -> Modifier_Obj:
        """
        Gets a modifier from the game data or from the character.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. Modifier_Obj
            - The modifier object that is searched.
        """

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None or len(modifier_list) == 0:
            return None

        for modifier in modifier_list:
            if stat in modifier.keys() and key in modifier[stat].keys():
                return modifier[stat][key]

        return None

    # endregion
    ###########################################

##################################
# region Modify Stat Label ----- #
##################################

label change_money(value):
    # """
    # Changes the money with the modifier.

    # ### Parameters:
    # 1. value: num
    #     - The value of the money. This is the value that is being changed.
    # 2. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # """

    if is_in_replay:
        return

    if isinstance(value, str):
        $ value = get_stat_levels(value)

    $ change_stat('money', value)

    return

label change_money_with_modifier(value, collection = 'default'):
    # """
    # Changes the money with the modifier.

    # ### Parameters:
    # 1. value: num
    #     - The value of the money. This is the value that is being changed.
    # 2. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # """

    if is_in_replay:
        return

    if isinstance(value, str):
        $ value = get_stat_levels(value)

    $ value = apply_stat_modifier('money', value, collection)

    $ change_stat('money', value)

    return

label change_stat_with_modifier(stat, value, collection = 'default'):
    # """
    # Changes the stat with the modifier.

    # ### Parameters:
    # 1. stat: str
    #     - The stat that the modifier is changing.
    # 2. value: num
    #     - The value of the stat. This is the value that is being changed.
    # 3. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # """

    if is_in_replay:
        return

    if isinstance(value, str):
        $ value = get_stat_levels(value)

    python:
        cswm_stat_list = [stat]
        cswm_modifier_stat = None
        parsed = parse_situation_stat_key(stat) if isinstance(stat, str) else None
        if parsed is not None:
            situation_key, bar_key = parsed
            if bar_key == "ALL":
                situation = situation_manager.get_situation(situation_key)
                if situation is not None:
                    cswm_modifier_stat = stat
                    cswm_stat_list = [
                        "situation:" + situation_key + ":" + bar.key
                        for bar in situation.get_bars()
                    ]

    $ cswm_i = 0
    $ cswm_base_value = value
    while cswm_i < len(cswm_stat_list):
        $ cswm_target_stat = cswm_stat_list[cswm_i]
        if cswm_modifier_stat is not None:
            $ value = apply_stat_modifier(cswm_modifier_stat, cswm_base_value, collection, range_stat=cswm_target_stat)
        else:
            $ value = apply_stat_modifier(cswm_target_stat, cswm_base_value, collection)
        $ change_stat(cswm_target_stat, value)
        $ cswm_i += 1

    if not str(stat).startswith("situation:"):
        $ add_stat_notification(get_school().get_name(), stat, value)

    return

label change_stats_with_modifier(collection = 'default', **kwargs):
    # """
    # Changes multiple stats with the modifier.

    # ### Parameters:
    # 1. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # 2. **kwargs:
    #     - The stats that are being changed. The key is the stat, and the value is the value of the stat.
    # """

    $ in_replay = get_kwargs('in_replay', False, **kwargs)

    if in_replay:
        return

    $ cswsm_keys = list(kwargs.keys())

    $ cswsm_i = 0
    while cswsm_i < len(cswsm_keys):
        $ cswsm_stat = cswsm_keys[cswsm_i]
        $ cswsm_i += 1
        call change_stat_with_modifier(cswsm_stat, kwargs[cswsm_stat], collection) from _call_change_stat_with_modifier

    return

label change_stats_via_modifier(collection = 'default'):
    $ modifier_collection_list = get_modifier_collection(collection)

    python:
        csvm_stats_to_process = set()
        for modifier_collection in modifier_collection_list:
            for csvm_stat in modifier_collection.keys():
                if csvm_stat != "all":
                    csvm_stats_to_process.add(csvm_stat)
        csvm_stats_to_process = list(csvm_stats_to_process)

    $ csvm_i = 0
    while csvm_i < len(csvm_stats_to_process):
        $ csvm_stat = csvm_stats_to_process[csvm_i]
        $ csvm_i += 1
        call change_stat_with_modifier(csvm_stat, 0, collection) from _call_change_stat_via_modifier

    return

# endregion
#################################
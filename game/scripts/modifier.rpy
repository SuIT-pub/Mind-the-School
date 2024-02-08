init -6 python:
    
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

        def get_change(self) -> str:
            """
            Gets the change in the stat based on the mod_type and value.

            ### Returns:
            1. float
                - The change in the stat.
            """

            if self._mod_type == "*":
                return f"x {self._value}"
            elif self._mod_type == "%":
                return f"{self._value}%"
            else:
                return str(self._value)

        def calculate_change(self, base_value: num) -> float:
            """
            Calculates the change in the stat based on the mod_type and value.

            ### Parameters:
            1. base_value: num
                - The base value of the stat. This is the value that is being changed.

            ### Returns:
            1. float
                - The change in the stat.
            """

            if self._mod_type == "+":
                return self._value
            elif self._mod_type == "*":
                return base_value * self._value
            elif self._mod_type == "%":
                return base_value / 100 * self._value
            else:
                return base_value

    def get_modifier_collection(collection: str = 'default') -> Dict[str, Modifier_Obj]:
        """
        Gets the collection of modifiers.

        ### Parameters:
        1. collection: str
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. Dict[str, Modifier_Obj]
            - The collection of modifiers.
        """
        
        if not contains_game_data('stat_modifier'):
            set_game_data('stat_modifier', {})

        modifier = get_game_data('stat_modifier')

        if collection not in modifier.keys():
            modifier[collection] = {}

        return modifier[collection]

    def prepare_for_modifier(key: str, stat: str, char_obj: Char = None, collection: str = 'default'):
        """
        Prepares the game data for a modifier. This is used to make sure that the game data is ready for a modifier to be added.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        """

        modifier = get_modifier_collection(collection)

        if char_obj != None:
            if char_obj.get_name() not in modifier.keys():
                modifier[char_obj.get_name()] = {}
            modifier = modifier[char_obj.get_name()]

        if stat not in modifier.keys():
            modifier[stat] = {}

        modifier[stat][key] = None

    def set_modifier(key: str, stat: str, mod_obj: Modifier_Obj, *, char_obj: Char = None, collection: str = 'default'):
        """
        Sets a modifier in the game data.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. mod_obj: Modifier_Obj
            - The modifier object that is being added.
        4. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        5. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        """

        prepare_for_modifier(key, stat, char_obj, collection)

        modifier = get_modifier_collection(collection)

        if char_obj != None:
            modifier[char_obj.get_name()][stat][key] = mod_obj
        else:
            modifier[stat][key] = mod_obj

    def remove_modifier(key: str, stat: str, char_obj: Char = None, collection: str = 'default'):
        """
        Removes a modifier from the game data.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        """

        modifier = get_modifier_collection(collection)

        if modifier == None:
            return

        remove_modifier = modifier
        if char_obj != None:
            if char_obj.get_name() not in remove_modifier.keys():
                return
            remove_modifier = remove_modifier[char_obj.get_name()]
        if stat not in remove_modifier.keys():
            return
        if key not in remove_modifier[stat].keys():
            return
        
        remove_modifier[stat][key] = None

    def get_modifier(key: str, stat: str, char_obj: Char = None, collection: str = 'default') -> Modifier_Obj:
        """
        Gets a modifier from the game data or from the character.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. Modifier_Obj
            - The modifier object that is searched.
        """

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None:
            return None

        if char_obj != None and char_obj.get_name() in modifier_list.keys():
            if stat in modifier_list[char_obj.get_name()].keys() and key in modifier_list[char_obj.get_name()][stat].keys():
                return modifier_list[char_obj.get_name()][stat][key]
        else:
            if stat in modifier_list.keys() and key in modifier_list[stat].keys():
                return modifier_list[stat][key]

        return None

    def get_modifier_lists(stat: str, char_obj: Char = None, collection: str = 'default') -> Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]:
        """
        Gets a list of modifiers from the game data or from the character.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        3. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]
            - A dictionary of modifiers. The key is the name of the modifier, and the value is the modifier object.
        """

        modifier = get_modifier_collection(collection)

        if modifier == None:
            return

        if char_obj != None:
            if char_obj.get_name() in modifier.keys() and stat in modifier[char_obj.get_name()].keys():
                return modifier[char_obj.get_name()][stat]
        else:
            if stat in modifier.keys():
                return modifier[stat]

        return None

    def get_total_modifier_change(key: str, stat: str, base_value: num, char_obj: Char = None, collection: str = 'default') -> float:
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
        4. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        5. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        modifier = get_modifier(key, stat, None, collection)

        modifier_char = None
        if char_obj != None:
            modifier_char = get_modifier(key, stat, char_obj, collection)

        value = 0
        if modifier != None:
            value += modifier.calculate_change(base_value)
        if modifier_char != None:
            value += modifier_char.calculate_change(base_value)

        return value

    def get_total_stat_modifier_change(stat: str, base_value: num, char_obj: Char = None, collection: str = 'default') -> float:
        """
        Gets the total change in the stat based on all of the modifiers.
        DOES NOT USE THIS METHOD! Use change_stats_with_modifier() instead.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. base_value: num
            - The base value of the stat. This is the value that is being changed.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        modifier = get_modifier_lists(stat, None, collection)
        modifier_char = None
        if char_obj != None:
            modifier_char = get_modifier_lists(stat, char_obj, collection)

        value = 0
        if modifier != None:
            for key in modifier.keys():
                value += get_total_modifier_change(key, stat, base_value, None, collection)
        if modifier_char != None:
            for key in modifier_char.keys():
                value += get_total_modifier_change(key, stat, base_value, char_obj, collection)

        return value

    def apply_stat_modifier(stat: str, value: num, char_obj: Char = None, collection: str = 'default') -> float:
        """
        Applies the stat modifier to the value.
        DOES NOT USE THIS METHOD! Use change_stats_with_modifier() instead.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. value: num
            - The value of the stat. This is the value that is being changed.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.

        ### Returns:
        1. float
            - The total change in the stat.
        """

        value = value + get_total_stat_modifier_change(stat, value, char_obj, collection)
        
        return value

    def change_money_with_modifier(value: num, collection: str = 'default'):
        """
        Changes the money with the modifier.

        ### Parameters:
        1. value: num
            - The value of the money. This is the value that is being changed.
        2. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        """

        if is_in_replay:
            return

        if isinstance(value, str):
            value = get_stat_levels(value)

        value = apply_stat_modifier('money', value, None, collection)

        log_val('value', value)

        change_stat('money', value)

    def change_stat_with_modifier(stat: str, value: num, char_obj: Char, collection: str = 'default'):
        """
        Changes the stat with the modifier.

        ### Parameters:
        1. stat: str
            - The stat that the modifier is changing.
        2. value: num
            - The value of the stat. This is the value that is being changed.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        """

        if is_in_replay:
            return

        if isinstance(value, str):
            value = get_stat_levels(value)

        value = apply_stat_modifier(stat, value, char_obj, collection)

        char_obj.change_stat(stat, value)

    def change_stats_with_modifier(char_obj: Char, collection: str = 'default', **kwargs):
        """
        Changes multiple stats with the modifier.

        ### Parameters:
        1. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        2. collection: str (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
        3. **kwargs:
            - The stats that are being changed. The key is the stat, and the value is the value of the stat.
        """

        in_replay = get_kwargs('in_replay', False, **kwargs)

        if char_obj == None or in_replay:
            return

        for stat in kwargs.keys():
            if stat == "char_obj":
                continue

            # if stat in Stat_Data:
            change_stat_with_modifier(stat, kwargs[stat], char_obj, collection)

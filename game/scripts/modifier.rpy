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

    # endregion
    ########################

    ##############################
    # region Modifier Beef ----- #
    ##############################

    def get_modifier_collection(collection: str | List[str] = 'default') -> Dict[str, Modifier_Obj]:
        """
        Gets the collection of modifiers.

        ### Parameters:
        1. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then multiple collections are returned.

        ### Returns:
        1. Dict[str, Modifier_Obj]
            - The collection of modifiers.
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

    def prepare_for_modifier(key: str, stat: str = "all", char_obj: Char = None, collection: str | List[str] = 'default'):
        """
        Prepares the game data for a modifier. This is used to make sure that the game data is ready for a modifier to be added.

        ### Parameters:
        1. key: str
            - The key of the modifier. This is the name of the modifier.
        2. stat: str
            - The stat that the modifier is changing.
            - if "all", then the modifier is applied to all stats.
        3. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        4. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then multiple collections are prepared.
        """

        modifier_list = get_modifier_collection(collection)

        for modifier in modifier_list:
            if char_obj != None:
                if char_obj.get_name() not in modifier.keys():
                    modifier[char_obj.get_name()] = {}
                modifier = modifier[char_obj.get_name()]

            if stat not in modifier.keys():
                modifier[stat] = {}

            modifier[stat][key] = None

    def get_modifier_lists(stat: str, char_obj: Char = None, collection: str | List[str] = 'default') -> Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]:
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

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None or len(modifier_list) == 0:
            return {}

        output = {}

        for modifier in modifier_list:
            if char_obj != None and char_obj.get_name() in modifier.keys():
                if stat in modifier[char_obj.get_name()].keys():
                    output = update_dict(output, modifier[char_obj.get_name()][stat])
                    # output.append(modifier[char_obj.get_name()][stat])
                if stat != 'all' and 'all' in modifier[char_obj.get_name()].keys():
                    output = update_dict(output, modifier[char_obj.get_name()]['all'])
                    # output.append(modifier[char_obj.get_name()]['all'])
            else:
                if stat in modifier.keys():
                    output = update_dict(output, modifier[stat])
                    # output.append(modifier[stat])
                if stat != 'all' and 'all' in modifier.keys():
                    output = update_dict(output, modifier['all'])
                    # output.append(modifier['all'])

        return output

    def get_total_modifier_change(mod_obj: Modifier_Obj, base_value: num, char_obj: Char = None, collection: str = 'default') -> float:
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

        value = 0
        value += mod_obj.calculate_change(base_value)

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
                value += get_total_modifier_change(modifier[key], base_value, None, collection)
        if modifier_char != None:
            for key in modifier_char.keys():
                value += get_total_modifier_change(modifier_char[key], base_value, char_obj, collection)

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

    def set_modifier(key: str, mod_obj: Modifier_Obj, *, stat: str = "all", char_obj: Char = None, collection: str | List[str] = 'default'):
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
        4. char_obj: Char
            - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
        5. collection: str | List[str] (default 'default')
            - The collection of modifiers. This is used to separate different collections of modifiers.
            - If a list of collections is given, then the modifier is added to multiple collections.
        """

        prepare_for_modifier(key, stat, char_obj, collection)

        modifier_list = get_modifier_collection(collection)

        for modifier in modifier_list:
            if char_obj != None:
                modifier[char_obj.get_name()][stat][key] = mod_obj
            else:
                modifier[stat][key] = mod_obj

    def remove_modifier(key: str, stat: str = "all", char_obj: Char = None, collection: str = 'default'):
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

        modifier_list = get_modifier_collection(collection)

        if modifier_list == None or len(modifier_list) == 0:
            return

        modifier = modifier_list[0]
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

    def get_modifier(key: str, stat: str = "all", char_obj: Char = None, collection: str = 'default') -> Modifier_Obj:
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

        if modifier_list == None or len(modifier_list) == 0:
            return None

        for modifier in modifier_list:
            if char_obj != None and char_obj.get_name() in modifier.keys():
                if stat in modifier[char_obj.get_name()].keys() and key in modifier[char_obj.get_name()][stat].keys():
                    return modifier[char_obj.get_name()][stat][key]
            else:
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

    $ value = apply_stat_modifier('money', value, None, collection)

    $ change_stat('money', value)

    return

label change_stat_with_modifier(stat, value, char_name, collection = 'default'):
    # """
    # Changes the stat with the modifier.

    # ### Parameters:
    # 1. stat: str
    #     - The stat that the modifier is changing.
    # 2. value: num
    #     - The value of the stat. This is the value that is being changed.
    # 3. char_obj: Char
    #     - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
    # 4. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # """

    $ char_obj = get_character_by_key(char_name)

    if is_in_replay or char_obj == None:
        return

    if isinstance(value, str):
        $ value = get_stat_levels(value)

    $ value = apply_stat_modifier(stat, value, char_obj, collection)

    $ char_obj.change_stat(stat, value)

    $ add_stat_notification(char_name, stat, value)

    return

label change_stats_with_modifier(char_name, collection = 'default', **kwargs):
    # """
    # Changes multiple stats with the modifier.

    # ### Parameters:
    # 1. char_obj: str
    #     - The character that the modifier is being applied to. If None, then the modifier is applied to the game data.
    # 2. collection: str (default 'default')
    #     - The collection of modifiers. This is used to separate different collections of modifiers.
    # 3. **kwargs:
    #     - The stats that are being changed. The key is the stat, and the value is the value of the stat.
    # """

    $ in_replay = get_kwargs('in_replay', False, **kwargs)

    if char_name == "" or in_replay:
        return

    $ keys = list(kwargs.keys())

    $ i = 0
    while i < len(keys):
        $ stat = keys[i]
        $ i += 1
        call change_stat_with_modifier(stat, kwargs[stat], char_name, collection) from _call_change_stat_with_modifier

    return

# endregion
#################################
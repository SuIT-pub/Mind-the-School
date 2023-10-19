init -6 python:
    
    class Modifier_Obj:
        def __init__(self, mod_type: str, value: num):
            self.mod_type = mod_type
            self.value = value

        def calculate_change(self, base_value: num) -> float:
            if self.mod_type == "+":
                return self.value
            elif self.mod_type == "*":
                return base_value * self.value - base_value
            elif self.mod_type == "%":
                return base_value / 100 * self.value
            else:
                return base_value

    def prepare_for_modifier(key: str, stat: str, char_obj: Char = None) -> None:

        if not contains_game_data('stat_modifier'):
            set_game_data('stat_modifier', {})

        modifier = get_game_data('stat_modifier')

        if char_obj != None:
            if char_obj.get_name() not in modifier.keys():
                modifier[char_obj.get_name()] = {}
            modifier = modifier[char_obj.get_name()]

        if stat not in modifier.keys():
            modifier[stat] = {}

        modifier[stat][key] = None

    def set_modifier(key: str, stat: str, mod_obj: Modifier_Obj, char_obj: Char = None) -> None:
        prepare_for_modifier(key, stat, char_obj)

        if char_obj != None:
            modifier[char_obj.get_name()][stat][key] = mod_obj
        else:
            modifier[stat][key] = mod_obj

    def remove_modifier(key: str, stat: str, char_obj: Char = None) -> None:
        modifier = get_game_data('stat_modifier')

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

    def get_modifier(key: str, stat: str, char_obj: Char = None) -> Modifier_Obj:
        modifier = get_game_data('stat_modifier')
        if modifier == None:
            return None

        if char_obj != None and char_obj.get_name() in modifier.keys():
            if stat in modifier[char_obj.get_name()].keys() and key in modifier[char_obj.get_name()][stat].keys():
                return modifier[char_obj.get_name()][stat][key]
        else:
            if stat in modifier.keys() and key in modifier[stat].keys():
                return modifier[stat][key]

        return None

    def get_modifier_lists(stat: str, char_obj: Char = None) -> Dict[str, Modifier_Obj | Dict[str, Modifier_Obj]]:
        modifier = get_game_data('stat_modifier')
        if modifier == None:
            return

        if char_obj != None:
            if char_obj.get_name() in modifier.keys() and stat in modifier[char_obj.get_name()].keys():
                return modifier[char_obj.get_name()][stat]
        else:
            if stat in modifier.keys():
                return modifier[stat]

        return None

    def get_total_modifier_change(key: str, stat: str, base_value: num, char_obj: Char = None) -> float:
        modifier = get_modifier(key, stat)
        modifier_char = None
        if char_obj != None:
            modifier_char = get_modifier(key, stat, char_obj)

        value = 0
        if modifier != None:
            value += modifier.calculate_change(base_value)
        if modifier_char != None:
            value += modifier_char.calculate_change(base_value)

        return value

    def get_total_stat_modifier_change(stat: str, base_value: num, char_obj: Char = None) -> float:
        modifier = get_modifier_lists(stat)
        modifier_char = None
        if char_obj != None:
            modifier_char = get_modifier_lists(stat, char_obj)

        value = 0
        if modifier != None:
            for key in modifier.keys():
                value += get_total_modifier_change(key, stat, base_value)
        if modifier_char != None:
            for key in modifier_char.keys():
                value += get_total_modifier_change(key, stat, base_value, char_obj)

        return value

    def apply_stat_modifier(stat: str, value: num, char_obj: Char = None) -> float:
        value = value + get_total_stat_modifier_change(stat, value, char_obj)
        
        return value

    def change_stat_with_modifier(stat: str, value: num, char_obj: Char) -> None:
        if isinstance(value, str):
            value = get_stat_levels(value)

        value = apply_stat_modifier(stat, value, char_obj)

        char_obj.change_stat(stat, value)

    def change_stats_with_modifier(char_obj: Char, **kwargs) -> None:
        for stat in kwargs.keys():
            # if stat in Stat_Data:
            change_stat_with_modifier(stat, kwargs[stat], char_obj)

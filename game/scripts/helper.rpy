init -99 python:
    from typing import TypeVar
    import re

    def in_kwargs(key: str, **kwargs) -> bool:
        """
        Checks if a key is in kwargs

        ### Parameters:
        1. key: str
            - The key to check for
        2. **kwargs
            - The kwargs to check in

        ### Returns:
        1. bool
            - True if the key is in kwargs, False otherwise
        """

        if key in kwargs.keys():
            return True
        return False

    def get_kwargs(key: str, alt = None, **kwargs) -> Any:
        """
        Gets a value from kwargs

        ### Parameters:
        1. key: str
            - The key to get
        2. alt: Any (default None)
            - The value to return if the key is not in kwargs
        3. **kwargs
            - The kwargs to get from
        """

        if key in kwargs.keys():
            return kwargs[key]
        return alt

    def max(*values: number) -> number:
        """
        Returns the largest value

        ### Parameters:
        1. *values: number
            - The values to compare

        ### Returns:
        1. number
            - The largest value
        """

        largest = None

        for value in values:
            if largest is None or value > largest:
                largest = value
        return largest

    def min(*values: number) -> number:
        """
        Returns the smallest value

        ### Parameters:
        1. *values: number
            - The values to compare

        ### Returns:
        1. number
            - The smallest value
        """

        smallest = None

        for value in values:
            if smallest is None or value < smallest:
                smallest = value
        return smallest

    def clamp_value(value: num, min: num, max: num) -> num:
        """
        Clamps a value between a min and max

        ### Parameters:
        1. value: num
            - The value to clamp
        2. min: num
            - The minimum value
        3. max: num
            - The maximum value

        ### Returns:
        1. num
            - The clamped value
        """

        if value < min:
            return min
        if value > max:
            return max
        return value

    def is_integer(text: str) -> bool:
        """
        Checks if a string can be converted to an integer

        ### Parameters:
        1. text: str
            - The string to check

        ### Returns:
        1. bool
            - True if the string can be converted to an integer, False otherwise
        """

        try:
            int(text)
            return True
        except ValueError:
            return False

    def is_float(text: str) -> bool:
        """
        Checks if a string can be converted to a float

        ### Parameters:
        1. text: str
            - The string to check

        ### Returns:
        1. bool
            - True if the string can be converted to a float, False otherwise
        """

        try:
            float(text)
            return True
        except ValueError:
            return False

    def set_smallest(*values: num) -> num:
        """
        Returns the smaller of the two values

        ### Parameters:
        1. *values: num
            - The values to compare

        ### Returns:
        1. num
            - The smallest value
        """

        smallest = None

        for value in values:
            if smallest is None or value < smallest:
                smallest = value
        return smallest

    def set_nearest(nearest: num, value: num) -> num:
        """
        Returns the value if it is closer to 0 than the nearest value

        ### Parameters:
        1. nearest: num
            - The nearest value
        2. value: num
            - The value to compare

        ### Returns:
        1. num
            - The nearest value
        """

        if nearest is None or abs(value) < abs(nearest):
            return value
        return nearest

    def check_in_value(value_range: [str, int], value: int) -> bool:
        """
        Checks if a value is in a value range
        The range can be defined in multiple ways:
            - as a single value
            - as a range (e.g. 1-5)
            - as a range with a minimum (e.g. 1+)
            - as a range with a maximum (e.g. 5-)
            - as a list of values (e.g. 1,3,5)

        ### Parameters:
        1. value_range: [str, int]
            - The value range to check
        2. value: int
            - The value to check

        ### Returns:
        1. bool
            - True if the value is in the value range, False otherwise
        """

        split = str(value_range).split(',')

        nearest = None

        for split_val in split:
            split_val = split_val.strip()
            val_str = re.findall('\d+', split_val)
            if val_str:
                vals = int(''.join(val_str))
                if '-' in split_val:
                    if split_val.endswith('-'):
                        if value <= vals:
                            return True
                    else:
                        val_list = split_val.split('-')
                        if value < int(val_list[0]) or value > int(val_list[1]):
                            continue
                        else:
                            return True
                elif split_val.endswith('+'):
                    if value >= vals:
                        return True
                elif vals == value:
                    return True

        return str(value_range) == str(value)

    def get_value_diff(value_range: [str, int], value: int) -> num:
        """
        Returns the difference between a value and a value range
        The range can be defined in multiple ways:
            - as a single value
            - as a range (e.g. 1-5)
            - as a range with a minimum (e.g. 1+)
            - as a range with a maximum (e.g. 5-)
            - as a list of values (e.g. 1,3,5)
        
        ### Parameters:
        1. value_range: [str, int]
            - The value range to check
        2. value: int
            - The value to check

        ### Returns:
        1. num
            - The difference between the value and the value range
            - If the value is inside the range the difference will be the positive difference from the next lowest value
            - If the value is outside the range the difference will be the negative difference from the nearest value
        """

        split = str(value_range).split(',')

        nearest = None

        for split_val in split:
            split_val = split_val.strip()
            val_str = re.findall('\d+', split_val)
            if val_str:
                vals = int(''.join(val_str))
                if '-' in split_val:
                    if split_val.endswith('-'):
                        nearest = set_nearest(nearest, vals - value)
                    else:
                        val_list = split_val.split('-')
                        if value < int(val_list[0]):
                            nearest = set_nearest(nearest, value - int(val_list[0]))
                        elif value > int(val_list[1]):
                            nearest = set_nearest(nearest, int(val_list[1]) - value)
                        else:
                            nearest = set_nearest(nearest, abs(int(val_list[0]) - value))
                elif split_val.endswith('+'):
                    nearest = set_nearest(nearest, value - vals)
                else:
                    nearest = set_nearest(nearest, -abs(vals - int(value)))

        return nearest
    
    def remove_all_from_list(list_obj: List[Any], value: Any | List[Any]) -> List[Any]:
        """
        Removes all instances of a value from a list

        ### Parameters:
        1. list_obj: List[Any]
            - The list to remove from
        2. value: Any | List[Any]
            - The value to remove

        ### Returns:
        1. List[Any]
            - The list with the value removed
        """

        if type(value) is list_obj:
            for val in value:
                list_obj.remove(val)
        else:
            while value in list_obj:
                list_obj.remove(value)
        return list_obj

    def random_say(*text: str | Tuple, **kwargs):
        """
        Prints a random string from a list of strings

        ### Parameters:
        1. *text: str | Tuple
            - The strings to print
            - If a tuple is passed it will be treated as a list of strings
            - If the tuple contains a bool it will be treated as a condition
            - If the tuple contains an int it will be treated as an image
            - If the tuple contains a ADVCharacter it will be treated as a character
            - If the tuple contains a tuple it will be treated as a character and a name
            - If the tuple is contained in another tuple starting with a float it will be treated as a weight
        2. **kwargs
            - The kwargs to get from
            - If the kwargs contain a "person" key it will be treated as a character
            - If the kwargs contain a "name" key it will be treated as a name
            - If the kwargs contain a "image" key it will be treated as an image
        """

        person = get_kwargs("person", character.subtitles, **kwargs)
        name = get_kwargs("name", person.name, **kwargs)
        image = get_kwargs("image", None, **kwargs)

        text_list = list(text)

        text_out = ""

        while len(text_list) > 0:
            text_obj = get_random_choice(*text_list)

            skip = False
            use_image = -1
            use_name = ""

            if isinstance(text_obj, str):
                text_out = text_obj
            else:
                for obj in text_obj:
                    if isinstance(obj, str):
                        text_out = obj
                    elif isinstance(obj, bool) and not obj:
                        text_list.remove(text_obj)
                        skip = True
                        break
                    elif isinstance(obj, int) and image != None:
                        use_image = obj
                    elif isinstance(obj, ADVCharacter):
                        person = obj
                        name = person.name
                    elif isinstance(obj, tuple):
                        person = obj[0]
                        use_name = obj[1]

                if skip:
                    continue
                if use_name != "":
                    name = use_name
                if use_image != -1 and image != None:
                    renpy.call("say_with_image", image, use_image, text_out, name, person)

            person (text_out, name = name)
            break

        return

    def begin_event(name: str = ""):
        """
        This method is called at the start of an event after choices and topics have been chosen in the event.
        It prevents rollback to before this method and thus prevents changing choices and topics.
        """

        global seenEvents

        if contains_game_data("seen_events"):
            seenEvents = get_game_data("seen_events")

        if name != "" and name in seenEvents.keys():
            seenEvents[name] = True
            set_game_data("seen_events", seenEvents)
            if all(seenEvents.values()):
                set_game_data("all_events_seen", True)

        renpy.block_rollback()

        renpy.call("show_sfw_text", name)


    def set_game_data(key: str, value: Any):
        """
        Sets a value in gameData

        ### Parameters:
        1. key: str
            - The key to set
        2. value: Any
            - The value to set
        """

        gameData[key] = value

    def start_progress(key: str):
        """
        Starts an event chain

        ### Parameters:
        1. key: str
            - The key for the event chain
        """

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = 1

    def advance_progress(key: str, delta: int = 1):
        """
        Advances an event chain

        ### Parameters:
        1. key: str
            - The key for the event chain
            - If the event chain does not exist it will be created
        2. delta: int (default 1)
            - The amount of advance for the event chain
        """

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        if key not in gameData["progress"].keys():
            gameData["progress"][key] = 0
        gameData["progress"][key] += delta

    def set_progress(key: str, value: int):
        """
        Sets the progress of an event chain

        ### Parameters:
        1. key: str
            - The key for the event chain
            - If the event chain does not exist it will be created
        2. value: int
            - The value of progress to set the event chain to
        """

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = value

    def get_progress(key: str) -> int:
        """
        Gets the progress of an event chain

        ### Parameters:
        1. key: str
            - The key for the event chain

        ### Returns:
        1. int
            - The progress of the event chain
            - if the event chain does not exist -1 is returned
        """

        if "progress" not in gameData.keys() or key not in gameData["progress"].keys():
            return -1
        return gameData["progress"][key]

    def get_game_data(key: str) -> Any:
        """
        Gets a value from gameData

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. Any
            - The value from gameData
            - If the key does not exist None is returned
        """

        if key in gameData.keys():
            return gameData[key]
        return None

    def contains_game_data(key: str) -> bool:
        """
        Checks if a key is in gameData

        ### Parameters:
        1. key: str
            - The key to check

        ### Returns:
        1. bool
            - True if the key is in gameData, False otherwise
        """

        return key in gameData.keys()

    def get_school() -> Char:
        """
        Gets a random school

        ### Returns:
        1. Char
            - The random school
        """
        
        if 'school' not in charList.keys():
            fix_schools()

        return charList['school']

    T = TypeVar('T')

    def fix_schools():
        old_character = get_character("school_mean_values", charList)
        if old_character != None:
            max_level = 0
            high_school = get_character("high_school", charList['schools'])
            middle_school = get_character("middle_school", charList['schools'])
            elementary_school = get_character("elementary_school", charList['schools'])
            if high_school != None:
                max_level = max(max_level, high_school.get_level())

            old_character.name = "school"
            old_character.title = "School"
            old_character.level = Stat("level", max_level)
            charList["school"] = old_character
            charList.pop("school_mean_values")
        if 'schools' in charList:
            charList['schools'].pop("high_school")
            charList['schools'].pop("middle_school")
            charList['schools'].pop("elementary_school")
            charList.pop('schools')

        load_character("school", "School", charList, {
            'stats_objects': {
                "corruption": Stat(CORRUPTION, 0),
                "inhibition": Stat(INHIBITION, 100),
                "happiness": Stat(HAPPINESS, 12),
                "education": Stat(EDUCATION, 9),
                "charm": Stat(CHARM, 8),
                "reputation": Stat(REPUTATION, 7),
            }
        })

    def get_random_choice(*choice: T | Tuple[float, T] | Tuple[float, T, bool | Condition], **kwargs) -> T:
        """
        Selects a random value from a set of values

        ### Parameters:
        1. *choice: T | Tuple[float, T] | Tuple[float, T, bool | Condition]
            - The set of values to choose from
            - If a value is a tuple, the float acts as a weight that influences the probability of that value being chosen
            - The float value is a percentage in the range from 0.0 to 1.0
            - If the tuple contains a bool, the value will only be chosen if the bool is True
            - If the tuple contains a Condition, the value will only be chosen if the Condition is fulfilled

        ### Returns:
        1. T
            - value chosen
            - if the input value was a tuple, only the value of that tuple is returned and not the float
        """
        choice = list(choice)
        if any((isinstance(item, tuple) and (isinstance(item[0], float) or isinstance(item[0], int))) for item in choice):
            end_choice = []
            tuples = [item for item in choice if isinstance(item, tuple)]
            no_tuples = [item for item in choice if not isinstance(item, tuple)]

            total_weight = 100

            for x in tuples:
                if len(x) == 3:
                    if isinstance(x[2], bool) and not x[2]:
                        continue
                    elif isinstance(x[2], Condition) and not x[2].is_fulfilled(**kwargs):
                        continue
                elif len(x) == 2:
                    if isinstance(x[1], bool):
                        if x[1]:
                            no_tuples.append(x[0])
                        continue
                    elif isinstance(x[1], Condition):
                        if x[1].is_fulfilled(**kwargs):
                            no_tuples.append(x[0])
                        continue

                weight = int(x[0] * 100)
                end_choice.extend([x[1]] * weight)
                total_weight -= weight

            weights = int(total_weight / len(no_tuples))

            for x in no_tuples:
                end_choice.extend([x] * weights)

            return end_choice[get_random_int(0, len(end_choice) - 1)]
        else:
            if any((isinstance(item, tuple) and isinstance(item[1], Condition) for item in choice)):
                choice = list(filter(lambda x: not isinstance(x, tuple) or not isinstance(x[1], Condition) or x[1].is_fulfilled(**kwargs), choice))

            if len(choice) == 0:
                return None

            result = choice[get_random_int(0, len(choice) - 1)]
            if isinstance(result, tuple):
                return result[0]
            return result

    def get_random_int(start: int, end: int) -> int:
        """
        Gets a random integer in a range

        ### Parameters:
        1. start: int
            - The start of the range (inclusive)
        2. end: int
            - The end of the range (inclusive)

        ### Returns:
        1. int
            - The random integer
        """

        return random.randint(start, end)

    def get_random_loli() -> int:
        """
        Gets a random value representing the choice of loli_content

        ### Returns:
        1. int
            - the random value
        """
        value = get_random_int(0, loli_content)
        return value

    def log_val(key: str, value: Any):
        """
        Prints a key and value

        ### Parameters:
        1. key: str
            - The key to print
        2. value: Any
            - The value to print
        """

        print(key + ": " + str(value) + "\n")

    def log(msg: str):
        """
        Prints a message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print(str(msg) + "\n")
        return

    def log_error(msg: str):
        """
        Prints an error message

        ### Parameters:
        1. msg: str
            - The message to print
        """

        print("|ERROR| " + str(msg) + "\n")
        # renpy.notify("|ERROR| " + str(msg))
        return

    def get_stat_from_char_kwargs(stat: str, **kwargs) -> float:
        """
        Gets a stat from a character stored in kwargs

        ### Parameters:
        1. stat: str
            - The stat to get
        2. **kwargs
            - The kwargs to get the character from

        ### Returns:
        1. float
            - The stat value
            - If the character is not in kwargs -1 is returned
        """

        char_obj = get_kwargs("char_obj", **kwargs)
        if char_obj == None:
            return -1
        return char_obj.get_stat_number(stat)

    def get_stat_from_char(char_obj: Character, stat: str) -> float:
        """
        Gets a stat from a character

        ### Parameters:
        1. char_obj: Character
            - The character to get the stat from
        2. stat: str
            - The stat to get

        ### Returns:
        1. float
            - The stat value
        """

        return char_obj.get_stat_number(stat)

    def get_members(tier: str = '') -> List[str]:
        """
        Gets a list of patreon members
        It retrieves the csv list from the members.csv and returns it as a list of strings after filtering it by tier

        ### Parameters:
        1. tier: str (default '')
            - The tier to filter by
            - If tier is '' no filtering is done

        ### Returns:
        1. List[str]
            - The list of members
        """

        if not renpy.loadable("members.csv"):
            return []
        file = renpy.open_file("members.csv")
        lines = split_to_non_empty_list(file.read().decode(), "\r\n")
        if tier == '':
            return lines
        else:
            return [line for line in lines if line.split(',')[1].strip() == tier]

    def split_to_non_empty_list(s, delimiter) -> List[str]:
        """
        Splits a string into a list of non-empty strings

        ### Parameters:
        1. s: str
            - The string to split
        2. delimiter: str
            - The delimiter to split by

        ### Returns:
        1. List[str]
            - The list of non-empty strings
        """

        return list(filter(str.strip, s.split(delimiter)))

    def has_keyboard() -> bool:
        """
        Checks if the current platform has a keyboard and the use of keyboard shortcuts is activated in the game settings

        ### Returns:
        1. bool
            - True if the platform has a keyboard and the use of keyboard shortcuts is activated in the game settings, False otherwise
        """

        return not renpy.android and not renpy.ios and persistent.shortcuts != 2

    def show_shortcut() -> bool:
        """
        Checks if the use of keyboard shortcuts is activated in the game settings

        ### Returns:
        1. bool
            - True if the use of keyboard shortcuts is activated in the game settings, False otherwise
        """

        return persistent.shortcuts == 0

    def reroll_selectors():
        """
        Rerolls all selectors
        """

        global rerollSelectors

        for selector in rerollSelectors:
            selector.roll_values()

        rerollSelectors.clear()

    def get_location_title(key: str) -> str:
        building = get_building(key)
        if building == None:
            return key
        return building.get_title()

    def get_event_from_register(name: str) -> Event:
        if name in event_register.keys():
            return event_register[name]
        return None
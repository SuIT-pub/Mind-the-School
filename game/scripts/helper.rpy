init -99 python:
    from typing import TypeVar, Any, List, Tuple
    import collections.abc
    import re
    import requests

    T = TypeVar('T')

    ###############################
    # region Kwargs Functions --- #
    ###############################

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

        if key in kwargs.keys() and kwargs[key] != None:
            return kwargs[key]
        return alt

    def set_kwargs_value(key: str, value: Any, **kwargs):
        if "values" not in kwargs.keys():
            kwargs["values"] = {}
        kwargs["values"][key] = value
        return kwargs

    def get_kwargs_value(key: str, alt = None, **kwargs) -> Any:
        if "values" in kwargs.keys():
            return get_kwargs(key, get_kwargs(key, alt, **kwargs), **kwargs["values"])
        return get_kwargs(key, alt, **kwargs)

    def load_kwargs_values(data, **kwargs):
        if "values" not in data.keys():
            data["values"] = {}
        for key, value in kwargs.items():
            data["values"][key] = value
        return data

    # endregion
    ###############################

    #####################################
    # region Mathematical Functions --- #
    #####################################

    def max(*values: num) -> num:
        """
        Returns the largest value

        ### Parameters:
        1. *values: int | float
            - The values to compare

        ### Returns:
        1. int | float
            - The largest value
        """

        largest = None

        for value in values:
            if largest is None or value > largest:
                largest = value
        return largest

    def min(*values: num) -> num:
        """
        Returns the smallest value

        ### Parameters:
        1. *values: int | float
            - The values to compare

        ### Returns:
        1. int | float
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

        value_range = re.sub(r'\s+', '', str(value_range))

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
                        smaller_value = int(val_list[0]) if int(val_list[0]) < int(val_list[1]) else int(val_list[1])
                        larger_value = int(val_list[0]) if int(val_list[0]) > int(val_list[1]) else int(val_list[1])
                        if value < int(smaller_value) or value > int(larger_value):
                            continue
                        else:
                            return True
                elif split_val.endswith('+'):
                    if value >= vals:
                        return True
                elif vals == value:
                    return True

        return str(value_range) == str(value)
    
    def get_highest_value(value_range: [str, int]) -> int:
        """
        Returns the highest value of the given range by comparing it to
        the maximum signed 64-bit value and subtracting the difference.
        Proper logic of interpreting the value range is done in get_value_diff

        ### Parameters:
        1. value_range: [str, int]
            - The value range to check

        ### Returns:
        1. int
            - Highest value in Range
            - Returns signed 64-bit max if range contains a (positive) infinite scale.
        """

        if str(value_range).count("+") > 0:
            return INT64_MAX

        diff = get_value_diff(value_range, INT64_MAX)
        
        return INT64_MAX - abs(diff)

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
    
    def compare_to(value1: num, value2: num) -> int:
        """
        Compares two values

        ### Parameters:
        1. value1: num
            - The first value
        2. value2: num
            - The second value

        ### Returns:
        1. int
            - 1 if value1 is greater than value2
            - -1 if value1 is less than value2
            - 0 if value1 is equal to value2
        """

        if value1 > value2:
            return 1
        elif value1 < value2:
            return -1
        else:
            return 0
    
    def get_element(value: num | str | Selector, **kwargs) -> Any:
        output = value
        while isinstance(output, Selector):
            output = output.roll(**kwargs)
        return output

    def get_element_num(value: num | str | Selector, **kwargs) -> num:
        output = value
        while isinstance(output, Selector):
            output = output.roll(**kwargs)
        if not is_float(output):
            return -1
        return float(output)

    # endregion
    #####################################

    #############################
    # region Dict Functions --- #
    #############################

    def update_dict(original_dict, new_dict):
        """
        Updates a dictionary with another dictionary

        ### Parameters:
        1. original_dict: dict
            - The dictionary to update
        2. new_dict: dict
            - The dictionary to update with

        ### Returns:
        1. dict
            - The updated dictionary
        """

        for key, value in new_dict.items():
            if isinstance(value, collections.Mapping):
                temp = update_dict(original_dict.get(key, { }), value)
                original_dict[key] = temp
            elif isinstance(value, list):
                original_dict[key] = (original_dict.get(key, []) + value)
            else:
                original_dict[key] = new_dict[key]
        return original_dict

    # endregion
    #############################

    #############################
    # region List Functions --- #
    #############################

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

    def is_in_list(elem: Any, list_obj: List[Any]) -> bool:
        """
        Checks if an element is in a list

        ### Parameters:
        1. elem: Any
            - The element to check for
        2. list_obj: List[Any]
            - The list to check in

        ### Returns:
        1. bool
            - True if the element is in the list, False otherwise
        """

        return elem in list_obj

    def get_next_in_list(list_obj: List[Any], value: Any) -> Any:
        """
        Returns the next element in a list
        """

        index = list_obj.index(value)

        if index + 1 == len(list_obj):
            return list_obj[0]
        else:
            return list_obj[index + 1]

    # endregion
    #############################

    ###############################
    # region String Functions --- #
    ###############################

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

    def get_translation(key: str) -> str:
        """
        Gets a translation from the translations.csv file

        ### Parameters:
        1. key: str
            - The key to get the translation for

        ### Returns:
        1. str
            - The translation
            - If the key is not in the translations.csv file the key is returned
        """

        if key in translation_texts.keys():
            return translation_texts[key]
        return key

    def set_text_color(text: str, color: str) -> str:
        """
        Sets the color of a text

        ### Parameters:
        1. text: str
            - The text to color
        2. color: str
            - The color to set

        ### Returns:
        1. str
            - The colored text
        """

        return "{" + "color=" + color + "}" + text + "{/color}"

    # endregion
    ###############################

    #################################
    # region Dialogue Functions --- #
    #################################

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

    # endregion
    #################################

    #############################
    # region Name Functions --- #
    #############################

    def set_name(key: str, first_name: str, last_name: str):
        """
        Sets a name in gameData

        ### Parameters:
        1. key: str
            - The key to set
        2. first_name: str
            - The first name to set
        3. last_name: str
            - The last name to set
        """

        if is_in_replay:
            return

        if "names" not in gameData.keys():
            gameData["names"] = {}
        gameData["names"][key] = (first_name, last_name)

        if key == "headmaster":
            headmaster_first_name = first_name
            headmaster_last_name = last_name

    def get_name(key: str) -> Tuple[str, str]:
        """
        Gets a name from gameData

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. Tuple[str, str]
            - The name
            - If the key is not in gameData (None, None) is returned
        """

        if "names" not in gameData.keys() or key not in gameData["names"].keys():
            if key in default_names.keys():
                return default_names[key]
            else:
                return (None, None)
        return gameData["names"][key]

    def get_name_str(key: str) -> str:
        """
        Gets a name from gameData as a string

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. str
            - The name
            - If the key is not in gameData "" is returned
        """

        if "names" not in gameData.keys() or key not in gameData["names"].keys():
            if key in default_names.keys():
                return ' '.join(list(default_names[key]))
            else:
                return "first_name last_name"
        return ' '.join(list(gameData["names"][key]))

    def get_name_first(key: str) -> str:
        """
        Gets a first name from gameData

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. str
            - The first name
            - If the key is not in gameData "" is returned
        """

        if "names" not in gameData.keys() or key not in gameData["names"].keys():
            if key in default_names.keys():
                return default_names[key][0]
            else:
                return "first_name"
        return gameData["names"][key][0]

    def get_name_last(key: str) -> str:
        """
        Gets a last name from gameData

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. str
            - The last name
            - If the key is not in gameData "" is returned
        """

        if "names" not in gameData.keys() or key not in gameData["names"].keys():
            if key in default_names.keys():
                return default_names[key][1]
            else:
                return "last_name"
        return gameData["names"][key][1]

    def split_name(name: str) -> Tuple[str, str]:
        """
        Splits a name into a first and last name

        ### Parameters:
        1. name: str
            - The name to split

        ### Returns:
        1. Tuple[str, str]
            - The first and last name
        """

        split = name.split(' ')
        if len(split) == 1:
            return (split[0], "")
        return (split[0], ' '.join(split[1:]))

    def split_name_first(name: str) -> str:
        return split_name(name)[0]

    def split_name_last(name: str) -> str:
        return split_name(name)[1]

    # endregion
    #############################

    #################################
    # region GameData Functions --- #
    #################################

    def set_game_data(key: str, value: Any):
        """
        Sets a value in gameData

        ### Parameters:
        1. key: str
            - The key to set
        2. value: Any
            - The value to set
        """

        if is_in_replay:
            return

        gameData[key] = value

    def get_game_data(key: str = None) -> Any:
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

        if key == None:
            return gameData

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

    def remove_game_data(key: str):
        """
        Removes a key from gameData

        ### Parameters:
        1. key: str
            - The key to remove
        """

        del gameData[key]

    def set_setting(key: str, value: Any):
        """
        Sets a setting in gameData

        ### Parameters:
        1. key: str
            - The key to set
        2. value: Any
            - The value to set
        """

        if is_in_replay:
            return

        if "settings" not in gameData.keys():
            gameData["settings"] = {}
        gameData["settings"][key] = value

    def get_setting(key: str) -> Any:
        """
        Gets a setting from gameData

        ### Parameters:
        1. key: str
            - The key to get

        ### Returns:
        1. Any
            - The value from gameData
            - If the key does not exist None is returned
        """

        if "settings" in gameData.keys() and key in gameData["settings"].keys():
            return gameData["settings"][key]
        return None

    def set_timer(key: str, new_time: str | Time = "", **kwargs):
        if is_in_replay:
            return

        if isinstance(new_time, str) and new_time != "":
            if new_time == "today":
                new_time = Time(time.day_to_string())
            else:
                new_time = Time(new_time)
        if new_time == "":
            new_time = Time()
            new_time.set_time(**kwargs)

        set_game_data("timer_" + key, new_time)

    

    # endregion
    #################################

    #################################
    # region Progress Functions --- #
    #################################

    def start_progress(key: str):
        """
        Starts an event chain
        (Sets the progress to 1)

        ### Parameters:
        1. key: str
            - The key for the event chain
        """

        if is_in_replay:
            return -1

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = 1
        return 1

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

        if is_in_replay:
            return -1

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        if key not in gameData["progress"].keys():
            gameData["progress"][key] = 0
        gameData["progress"][key] += delta


        return gameData["progress"][key]

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

        if is_in_replay:
            return value

        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = value

        return value

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

        if "progress" not in gameData.keys() or key not in gameData["progress"].keys() or is_in_replay:
            return -1
        return gameData["progress"][key]

    # endregion
    #################################

    ###################################
    # region Randomizer Functions --- #
    ###################################

    def get_random_choice(*choice: T | Tuple[float, T] | Tuple[T, bool | Condition] | Tuple[float, T, bool | Condition], **kwargs) -> T:
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

            if total_weight >= len(no_tuples):
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
            if isinstance(result, Selector):
                return result.get_value(**kwargs)
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
            - 0 is Class 3A
            - 1 is Class 2A
            - 2 is Class 1A
        """
        value = get_random_int(0, loli_content)
        return value

    # endregion
    ###################################

    ######################################
    # region External Data Functions --- #
    ######################################

    
    def download_message():
        global message

        if persistent.load_supporter == 1:
            log("Load message from web.")
            try:
                response = requests.get('https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/master/game/message.txt')
                message = response.text
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                message = "Wasn't able to load notifications. Please check your internet connection."
                log('Failed Message Download')
        else:
            message = "Can't load notifications. Please turn on internet connection in settings.\nGame will not upload any data, only download."

        message = refine_downloaded_message(message)

    def refine_downloaded_message(text):
        try:
            time_pattern = re.compile(r'\[TIME\|(.+?)\|(.+?)\]')

            def replace_time(match):
                time_str, timezone = match.groups()
                device_timezone = get_device_timezone()
                converted_time = convert_timezone(time_str + ":00", timezone, str(device_timezone))
                converted_time += f" {get_device_timezone()}"
                return converted_time

            text = time_pattern.sub(replace_time, text)
        except Exception as e:
            log(f"Error processing time pattern: {e}")

        try:
            link_pattern = re.compile(r'\[LINK\|(.+?)\|(.+?)\]')

            def replace_link(match):
                text, link = match.groups()
                return f"{{a={link}}}{text}{{/a}}"

            text = link_pattern.sub(replace_link, text)
        except Exception as e:
            log(f"Error processing link pattern: {e}")

        bracket_pattern_1 = re.compile(r'(\[TIME\||\])')
        text = bracket_pattern_1.sub("", text)

        return text

    def download_members():
        global members

        if persistent.load_supporter == 1:
            try:
                response = requests.get('https://raw.githubusercontent.com/SuIT-pub/Mind-the-School/master/game/members.csv')
                members = refine_downloaded_message(response.text)
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                members = ""
                log('Failed Member Download')
        else:
            members = ""

    def get_members(tier: str = '') -> Tuple[List[str],str]:
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

        time = ""
        file = members
        lines = []

        if members == "" or members == "404: Not Found":
            if not renpy.loadable("members.csv"):
                return [], "Supporter list could not be loaded."
            file = refine_downloaded_message(renpy.open_file("members.csv"))
            lines = split_to_non_empty_list(file.read().decode(), "\r\n")
        else:
            lines = split_to_non_empty_list(file, "\n")
        if len(lines) == 0:
            return [], "Supporter list could not be loaded."
        time = lines.pop(0)
        if tier == '':
            return lines, time
        else:
            return [line for line in lines if line.split(';')[1].strip() == tier], time

    def get_translations():
        """
        Gets the translations from the translations.csv file
        """

        global translation_texts

        translation_texts = {}

        paths = []

        for mod in get_active_mods():
            if 'translations' in mod.keys():
                if isinstance(mod['translations'], str):
                    paths.extend(mod['path'] + mod['translations'])
                else:
                    paths.extend([mod['path'] + translation for translation in mod['translations']])

        for path in paths:
            if not renpy.loadable(path):
                continue
            file = renpy.open_file(path)
            lines = split_to_non_empty_list(file.read().decode(), "\r\n")
            for line in lines:
                if line.count(';') != 1:
                    continue
                key, value = line.split(';')
                translation_texts[key] = value

    def get_loli_filter():
        """
        Gets the translations from the translations.csv file
        """

        global loli_filter

        if not renpy.loadable("loli_filter"):
            loli_filter = {0:[], 1:[], 2:[]}
        file = renpy.open_file("loli_filter")
        lines = split_to_non_empty_list(file.read().decode(), "\r\n")

        if 0 not in loli_filter:
            loli_filter[0] = []
        if 1 not in loli_filter:
            loli_filter[1] = []
        if 2 not in loli_filter:
            loli_filter[2] = []

        for line in lines:
            key, content_level = line.split(';', 1)
            if int(content_level) >= 1:
                loli_filter[0].append(key)
            if int(content_level) == 2:
                loli_filter[1].append(key)

    def get_file_max_value(key: str, file_path: str, start: int = 0, end: int = 10) -> int:
        """
        Searches for the highest available value for a key in the given image path.

        ### Parameters:
        1. key: str
            - The key to search for.
        2. file_path: str
            - The file path to search in.
        3. start: int (default 0)
            - The start value to search from.
        4. end: int (default 10)
            - The end value to search to.

        ### Returns:
        1. int
            - The highest available value for the key in the given image path.
        """

        old_file = file_path.replace(f"<{key}>", "~#~")
        old_file = re.sub("<.+>", "0", old_file)
        old_file = old_file.replace("~#~", f"<{key}>")

        for i in range(start, end):
            test_file = old_file.replace(f"<{key}>", str(i))
            if not renpy.loadable(test_file):
                return i - 1

        return end

    # endregion
    ######################################

    ######################
    # region Modding --- #
    ######################

    import os

    def register_mod(key: str, name: str, version: str, path: str, **kwargs):

        global persistent

        kwargs['key'] = key
        kwargs['name'] = name
        kwargs['version'] = version

        if path and not path.endswith('/'):
            path += '/'

        kwargs['path'] = path

        available_keys.append(key)

        mod = {}

        modList = persistent.modList

        if key in modList.keys():
            mod = modList[key]
            if mod['version'] != version:
                mod['active'] = False
            mod.update(kwargs)
            mod['path'] = f"mods/{path}"
            mod['translations'] = []
            mod['event_count'] = 0
            if 'translations' in kwargs.keys():
                mod['translations'] = kwargs['translations']
            modList[key] = mod
        else:
            mod = kwargs
            mod['active'] = False
            mod['path'] = f"mods/{path}"
            mod['translations'] = []
            mod['event_count'] = 0
            if 'translations' in kwargs.keys():
                mod['translations'] = kwargs['translations']
            modList[key] = mod

        persistent.modList = modList

        return modList

    def get_mod_list():
        import json
        
        # get list of folders in /mods
        metadata_list = [s for s in renpy.list_files() if s.startswith("mods/") and s.endswith("metadata")]

        repair_mod_list()
        available_keys = ['base']
        return persistent.modList

        for metadata in metadata_list:
            # json_string = renpy.open_file(metadata, "utf-8").read()
            json_string = ""
            
            path = os.path.normpath(os.path.join(config.basedir, "game", metadata))

            with open(path,"r") as metafile:
                json_string = metafile.read()
            mod_json_obj = json.loads(json_string) 

            available_keys.append(mod_json_obj['key'])

            mod = {}

            if mod_json_obj['key'] in persistent.modList.keys():
                mod = persistent.modList[mod_json_obj['key']]
                if mod['version'] != mod_json_obj['version']:
                    mod['active'] = False
                mod.update(mod_json_obj)
                mod['path'] = metadata.replace("metadata", "")
                mod['translations'] = []
                mod['event_count'] = 0
                if 'translations' in mod_json_obj.keys():
                    mod['translations'] = mod_json_obj['translations']
                persistent.modList[mod_json_obj['key']] = mod
            else:
                mod = mod_json_obj
                mod['active'] = False
                mod['path'] = metadata.replace("metadata", "")
                mod['translations'] = []
                mod['event_count'] = 0
                if 'translations' in mod_json_obj.keys():
                    mod['translations'] = mod_json_obj['translations']
                persistent.modList[mod_json_obj['key']] = mod

        return persistent.modList

    def repair_mod_list():

        if persistent.modList == None:
            persistent.modList = {}

        if len(persistent.modList.keys()) == 0:
            persistent.modList['base'] = {
                'key': 'base', 
                'version': '1', 
                'name': 'Base Mod', 
                'description': 'The base mod for the game.', 
                'author': 'SuIT-Ji', 
                'active': True, 
                'available': True,
                'path': '',
                'event_count': 0,
                'translations': ['translations.csv'],
            }

        if 'available' not in persistent.modList['base']:
            persistent.modList['base']['available'] = True

        if 'translations' not in persistent.modList['base']:
            persistent.modList['base']['translations'] = ['translations.csv']

        for key in persistent.modList.keys():
            persistent.modList[key]['event_count'] = 0


    def is_mod_active(key: str) -> bool:
        
        repair_mod_list()

        if key in persistent.modList.keys():
            return persistent.modList[key]['active']
        return False

    def mod_exists(key: str) -> bool:
        return key in persistent.modList.keys()

    def set_current_mod(key: str):
        global active_mod_key
        active_mod_key = key

    def get_mod_path(key: str) -> str:
        if key in persistent.modList.keys():
            return persistent.modList[key]['path']
        return ""

    def get_current_mod_path() -> str:
        return get_mod_path(active_mod_key)

    def activate_mod(key: str):
        if key in persistent.modList.keys():
            persistent.modList[key]['active'] = True

    def deactivate_mod(key: str):
        if key in persistent.modList.keys():
            persistent.modList[key]['active'] = False

    def get_active_mods() -> List[Dict[str, Any]]:
        return [mod for mod in persistent.modList.values() if mod['active']]

    def change_mod_event_count(key: str, delta: int):

        global mod_count

        if key not in mod_count.keys():
            mod_count[key] = 0
        mod_count[key] += delta

        if key in persistent.modList.keys():
            if not 'event_count' in persistent.modList[key]:
                persistent.modList[key]['event_count'] = 0
            persistent.modList[key]['event_count'] += delta

    def register_start_method(label: str):
        if is_mod_active(active_mod_key):
            start_methods.append(label)

    # endregion
    ######################

    ###############################
    # region Ren'Py Functions --- #
    ###############################

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

    def play_sound(sound: str, loop: bool = False, volume: float = 1.0, fadein: float = 1.0):
        if not renpy.music.get_playing(channel='sound') == sound or not renpy.music.is_playing(channel='sound'):
            renpy.sound.play(sound, loop = loop, relative_volume = volume, fadein = fadein)

    # endregion
    ###############################

    import datetime
    import pytz
    import time as python_time

    def convert_timezone(time_str, from_tz, to_tz, time_format="%Y-%m-%d %H:%M:%S"):
        """
        Convert time from one timezone to another.
        
        :param time_str: Time string in the given format (e.g., "2025-01-20 15:00:00")
        :param from_tz: Source timezone (e.g., "UTC")
        :param to_tz: Target timezone (e.g., "America/New_York")
        :param time_format: Format of the time string
        :return: Converted time string
        """
        # Parse the time string into a datetime object
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        time_obj = datetime.datetime.strptime(time_str, time_format)

        # Localize the datetime object to the source timezone
        localized_time = from_zone.localize(time_obj)

        # Convert to the target timezone
        converted_time = localized_time.astimezone(to_zone)

        # Return the converted time as a string
        return converted_time.strftime(time_format)

    def get_device_timezone():
        """
        Get the device's local timezone using pytz.
        """
        # Get the local timezone name from the system
        local_timezone_name = python_time.tzname[0]
        
        try:
            # Convert the timezone name to a pytz timezone object
            local_timezone = pytz.timezone(local_timezone_name)
        except Exception:
            # Fallback to UTC if timezone conversion fails
            local_timezone = pytz.utc

        return local_timezone

    def get_local_time():
        """
        Get the current local time as a string.
        """
        local_timezone = get_device_timezone()
        now = datetime.datetime.now(local_timezone)
        return now.strftime("%Y-%m-%d %H:%M:%S")

init -96 python:
    def finishing_mod_list():    
        for key in list(persistent.modList.keys()):
            persistent.modList[key]['event_count'] = 0
            if key not in available_keys:
                persistent.modList[key]['available'] = False
                persistent.modList[key]['active'] = False
            else:
                persistent.modList[key]['available'] = True
    finishing_mod_list()

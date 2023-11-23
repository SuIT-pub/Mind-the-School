init -99 python:
    from typing import TypeVar
    import random
    import re

    def get_element(name: str, map: Dict[str, Any] = None):
        if type(map) is dict and name in map.keys():
            return (True, map[name])
        if type(map) is list and name.isdigit() and int(name) >= 0 and int(name) < len(map):
            return (True, map[int(name)])

        if "." in name:
            nameSplit = name.split(".", 1)

            if (type(map) is list and 
                nameSplit[0].isdigit() and 
                int(nameSplit[0]) >= 0 and 
                int(nameSplit[0]) < len(map)
            ):
                return get_element(nameSplit[1], map[int(nameSplit[0])])
            if type(map) is dict and nameSplit[0] in map.keys():
                return get_element(nameSplit[1], map[nameSplit[0]])

            return (False)

        return (False)

    def set_element(key: str, value: Any, map: Dict[str, Any]):
        if "." in key:
            keySplit = key.split(".", 1)

            if type(map) is dict:
                if keySplit[0] not in map.keys():
                    createKey = keySplit[1]
                    if "." in createKey:
                        keySplit2 = createKey.split(".", 1)
                        createKey = keySplit2[0]

                    if createKey.isdigit():
                        map[keySplit[0]] = []
                    else:
                        map[keySplit[0]] = {}

                    return set_element(keySplit[1], value, map[keySplit[0]])
            elif type(map) is list:
                if not keySplit[0].isdigit():
                    return False 

                index = int(keySplit[0])

                if index < 0:
                    return False

                if index >= len(map):

                    while index >= len(map):
                        map.append(None)

                    createKey = keySplit[1]
                    if "." in createKey:
                        keySplit2 = createKey.split(".", 1)
                        createKey = keySplit2[0]

                    if createKey.isdigit():
                        map[index] = []
                    else:
                        map[index] = {}

                    return set_element(keySplit[1], value, map[index])
        else:
            if type(map) is dict:
                map[key] = value
                return True
            elif type(map) is list and key.isdigit():
                index = int(key)

                if index < 0:
                    return False

                while index >= len(map):
                    map.append(None)

                map[index] = value
                return True
    
        return False

    def in_kwargs(key: str, **kwargs):
        if key in kwargs.keys():
            return True
        return False

    def get_kwargs(key: str, alt = None, **kwargs):
        if key in kwargs.keys():
            return kwargs[key]
        return alt

    def is_integer(text: str):
        try:
            int(text)
            return True
        except ValueError:
            return False

    def is_float(text: str):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def set_smallest(smallest: num, value: num):
        if smallest is None or value < smallest:
            return value
        return smallest

    def set_nearest(nearest: num, value: num):
        if nearest is None or abs(value) < abs(nearest):
            return value
        return nearest

    def check_in_value(value1: [str, int], value2: int):
        split = str(value1).split(',')

        nearest = None

        for split_val in split:
            split_val = split_val.strip()
            val_str = re.findall('\d+', split_val)
            if val_str:
                vals = int(''.join(val_str))
                if '-' in split_val:
                    if split_val.endswith('-'):
                        if value2 <= vals:
                            return True
                    else:
                        val_list = split_val.split('-')
                        if value2 < int(val_list[0]) or value2 > int(val_list[1]):
                            continue
                        else:
                            return True
                elif split_val.endswith('+'):
                    if value2 >= vals:
                        return True
                elif vals == value2:
                    return True

        return str(value1) == str(value2)

    def get_value_diff(value1: [str, int], value2: int):
        split = str(value1).split(',')

        nearest = None

        for split_val in split:
            split_val = split_val.strip()
            val_str = re.findall('\d+', split_val)
            if val_str:
                vals = int(''.join(val_str))
                if '-' in split_val:
                    if split_val.endswith('-'):
                        nearest = set_nearest(nearest, vals - value2)
                    else:
                        val_list = split_val.split('-')
                        if value2 < int(val_list[0]):
                            nearest = set_nearest(nearest, value2 - int(val_list[0]))
                        elif value2 > int(val_list[1]):
                            nearest = set_nearest(nearest, int(val_list[1]) - value2)
                        else:
                            nearest = set_nearest(nearest, abs(int(val_list[0]) - value2))
                elif split_val.endswith('+'):
                    nearest = set_nearest(nearest, value2 - vals)
                else:
                    nearest = set_nearest(nearest, -abs(vals - int(value2)))

        return nearest
    
    def remove_all_from_list(list_obj: List[Any], value: Any | List[Any]):
        if type(value) is list_obj:
            for val in value:
                list_obj.remove(val)
        else:
            while value in list_obj:
                list_obj.remove(value)
        return list_obj

    def random_say(*text: str | Dict[str, Any] | Tuple[float, Dict[str, Any]], **kwargs):

        person = get_kwargs("person", character.subtitles, **kwargs)
        name = get_kwargs("name", person.name, **kwargs)
        image = get_kwargs("image", None, **kwargs)

        text_list = list(text)

        while len(text_list) > 0:
            text_obj = get_random_choice(*text_list)

            text_out = text_obj
            if isinstance(text_obj, dict):
                if "if" in text_obj.keys() and not text_obj["if"]:
                    text_list.remove(text_obj)
                    continue
                if "say" in text_obj.keys():
                    text_out = text_obj["say"]
                if "person" in text_obj.keys():
                    person = text_obj["person"]
                    name = person.name
                if "name" in text_obj.keys():
                    name = text_obj["name"]
                if "image" in text_obj.keys() and image != None:
                    renpy.call("say_with_image", image, text_obj["image"], text_out, name, person)

            person (text_out, name = name)
            break

        return

    def begin_event():
        renpy.block_rollback()

    
    def set_game_data(key: str, value: Any) -> None:
        gameData[key] = value

    def start_progress(key: str) -> None:
        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = 1

    def advance_progress(key: str, delta: int = 1) -> None:
        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        if key not in gameData["progress"].keys():
            gameData["progress"][key] = 0
        gameData["progress"][key] += delta

    def set_progress(key: str, value: int) -> None:
        if "progress" not in gameData.keys():
            gameData["progress"] = {}
        gameData["progress"][key] = value

    def get_progress(key: str)-> int:
        if "progress" not in gameData.keys() or key not in gameData["progress"].keys():
            return -1
        return gameData["progress"][key]

    def get_game_data(key: str) -> Any:
        if key in gameData.keys():
            return gameData[key]
        return None

    def contains_game_data(key: str) -> bool:
        return key in gameData.keys()

    def get_image_with_level(image_path: str, level: int) -> str:

        path = image_path.replace("<nude>", "0")

        for i in reversed(range(0, level + 1)):
            image = path.replace("<level>", str(i))
            if renpy.loadable(image):
                return image_path.replace("<level>", str(i))
        for i in range(0, 10):
            image = path.replace("<level>", str(i))
            if renpy.loadable(image):
                return image_path.replace("<level>", str(i))
        
        return image_path

    def get_random_school() -> Char:
        school = get_random_school_name()
        return charList['schools'][school]

    def get_random_school_name() -> str:
        if loli_content == 2:
            return get_random_choice("high_school", "middle_school", "elementary_school")
        elif loli_content == 1:
            return get_random_choice("high_school", "middle_school")
        else:
            return "high_school"

    def get_all_schools() -> List[Char]:
        if loli_content == 2:
            return [charList['schools']['high_school'], charList['schools']['middle_school'], charList['schools']['elementary_school']]
        elif loli_content == 1:
            return [charList['schools']['high_school'], charList['schools']['middle_school']]
        else:
            return [charList['schools']['high_school']]

    T = TypeVar('T')

    def get_random_choice(*choice: T | Tuple[float, T]) -> T:
        choice = list(choice)
        if any((isinstance(item, tuple) and (isinstance(item[0], float) or isinstance(item[0], int))) for item in choice):
            end_choice = []
            tuples = [item for item in choice if isinstance(item, tuple)]
            no_tuples = [item for item in choice if not isinstance(item, tuple)]

            total_weight = 100

            for x in tuples:
                weight = int(x[0] * 100)
                end_choice.extend([x[1]] * weight)
                total_weight -= weight

            weights = int(total_weight / len(no_tuples))

            for x in no_tuples:
                end_choice.extend([x] * weights)

            return end_choice[get_random_int(0, len(end_choice) - 1)]
        else:
            return choice[get_random_int(0, len(choice) - 1)]

    def get_random_int(start: int, end: int):
        return random.randint(start, end)

    def log_val(key: str, value: Any) -> None:
        print(key + ": " + str(value) + "\n")

    def log(msg: str) -> None:
        print(str(msg) + "\n")

    def get_stat_from_char_kwargs(stat: str, **kwargs) -> float:
        char_obj = get_kwargs("char_obj", **kwargs)
        if char_obj == None:
            return -1
        return char_obj.get_stat_number(stat)

    def get_stat_from_char(char_obj: Character, stat: str) -> float:
        return char_obj.get_stat_number(stat)


label say_with_image (image_series, step, text, person_name, person):
    $ image_series.show(step)
    $ person(text, name = person_name)
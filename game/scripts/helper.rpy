init python:
    import re

    def get_element(name, map = None):
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

    def set_element(key, value, map):
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

    def in_kwargs(key, **kwargs):
        if key in kwargs.keys():
            return True
        return False

    def get_kwargs(key, **kwargs):
        if key in kwargs.keys():
            return kwargs[key]
        return None

    def is_integer(text):
        try:
            int(text)
            return True
        except ValueError:
            return False

    def is_float(text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def set_smallest(smallest, value):
        if smallest is None or value < smallest:
            return value
        return smallest

    def set_nearest(nearest, value):
        if nearest is None or abs(value) < abs(nearest):
            return value
        return nearest

    def get_value_diff(value1: [str, int], value2: int):
        split = value1.split(',')

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

        print("value1: " + str(value1) + " value2: " + str(value2) + " nearest: " + str(nearest))

        return nearest
        

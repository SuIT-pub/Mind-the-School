init python:
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

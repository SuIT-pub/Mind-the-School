init -6 python:
    import math
    class Char:
        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.level = Stat("level", 0)
            self.stats_objects = {}

        def _update(self, data = None):
            if data != None:
                self.__dict__.update(data)

            if not hasattr(self, 'level'):
                self.level = Stat("level", 0)
            if not hasattr(self, 'stats_objects'):
                self.stats_objects = {}

        def get_name(self):
            return self.name

        def get_title(self):
            return self.title

        def get_stat_obj(self, stat):
            if not stat in self.stats_objects:
                return None
            return self.stats_objects[stat]

        def set_stat(self, stat, value):
            stat_obj = self.get_stat_obj(stat)
            stat_obj.set_value(value)

        def change_stat(self, stat, delta):
            stat_obj = self.get_stat_obj(stat)
            stat_obj.change_value(delta)

        def get_stat_number(self, stat):
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return -1
            return stat_obj.get_value()

        def get_stat_string(self, stat):
            return str(self.get_stat_number(stat))

        def reset_changed_stats(self):
            for stat_key in self.stats_objects.keys():
                stat_obj = self.get_stat_obj(stat_key)

                if stat_obj == None:
                    continue

                stat_obj.reset_change()

        def get_stats(self):
            return self.stats_objects

        def check_stat(self, stat_name, value):
            if value == "x":
                return True

            return get_value_diff(value, self.get_stat_number(stat_name)) >= 0

            # value = str(value)

            # split = value.split(',')

            # for split_val in split:
            #     split_val = split_val.strip()
            #     stat_str = re.findall('\d+', split_val)
            #     if stat_str:
            #         stat = int(''.join(stat_str))
                    
            #         if (stat == self.get_stat_number(stat_name) or
            #             (split_val.endswith('-') and self.get_stat_number(stat_name) <= stat) or
            #             (split_val.endswith('+') and self.get_stat_number(stat_name) >= stat)
            #         ):
            #             return True
            #         elif '-' in split_val:
            #             stat_split = split_val.split('-')
            #             if (len(stat_split) == 2 and 
            #                 stat_split[0].isdecimal() and 
            #                 stat_split[1].isdecimal() and
            #                 int(stat_split[0]) <= self.get_stat_number(stat_name) <= int(stat_split[1])
            #             ):
            #                 return True

            # return str(value) == self.get_stat_string(stat_name)

        def get_level(self):
            return self.level.get_value()

        def get_level_str(self):
            return str(self.get_level())

        def set_level(self, level):
            self.level.set_value(level)
            if self.level.get_value() < 0:
                self.level.set_value(0)
            elif self.level.get_value() > 10:
                self.level.set_value(10)

        def get_nearest_level_delta(self, level):
            for i in range(self.get_level(), 11):
                if self.check_level(level, i):
                    return self.get_level() - i

        def check_level(self, value, test_level = None):
            if value == "x":
                return self.get_level_str()

            if test_level == None:
                test_level = self.get_level()

            value = str(value)

            split = value.split(',')

            for split_val in split:
                split_val = split_val.strip()
                level_str = re.findall('\d+', split_val)
                if level_str:
                    level = int(''.join(level_str))
                    
                    if (level == self.get_level() or
                        (split_val.endswith('-') and test_level <= level) or
                        (split_val.endswith('+') and test_level >= level)
                    ):
                        return True
                    elif '-' in split_val:
                        level_split = split_val.split('-')
                        if (len(level_split) == 2 and 
                            level_split[0].isdecimal() and 
                            level_split[1].isdecimal() and
                            int(level_split[0]) <= test_level <= int(level_split[1])
                        ):
                            return True

            return str(value) == str(test_level)

        def display_stat(self, stat):
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.display_stat()

        def get_display_value(self, stat):
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_value()

        def get_display_change(self, stat):
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.get_display_change()
    
    def get_lowest_level(map):
        level = 100
        for school in map.values():
            if school.get_level() < level:
                level = school.get_level()

        return level

    def update_mean_stats():
        mean_school = get_character("school_mean_values", charList)
        for stat in mean_school.get_stats().keys():
            mean = 0
            count = 0

            for obj in charList["schools"].values():
                if obj.get_name() == "middle_school" and loli_content == 0:
                    continue
                if obj.get_name() == "elementary_school" and loli_content != 2:
                    continue
                
                mean += obj.get_stat_number(stat)
                count += 1

            if count == 0:
                mean_school.set_stat(stat, 0)
            else:
                mean_school.set_stat(stat, round(mean / count, 2))

        mean_level = 0
        count = 0
        for obj in charList["schools"].values():
            if obj.get_name() == "middle_school" and loli_content == 0:
                continue
            if obj.get_name() == "elementary_school" and loli_content != 2:
                continue

            mean_level += obj.get_level()
            count += 1

        mean_school.set_level(math.ceil(mean_level))
               
    def get_mean_stat(stat):
        if stat == "money":
            return money.get_value()
        elif stat == "level":
            return get_level_for_char(stat, "school_mean_values", map)
        else:
            return get_stat_for_char(stat, "school_mean_values", map)

    def display_mean_stat(stat):
        if stat == "money":
            return money.display_stat()
        else:
            return get_character("school_mean_values", charList).display_stat(stat)

    def get_character(name, map):
        if name not in map.keys():
            return None

        return map[name]

    def get_stat_for_char(stat, name = "", map = None):

        if stat == "money":
            return money.get_value()

        if name in map.keys():
            return map[name].get_stat_number(stat)
        return -1

    def get_level_for_char(name, map):
        if name in map.keys():
            return map[name].get_level()
        return -1

    def set_stat_for_all(stat, value, map):
        for character in map.keys():
            map[character].set_stat(stat, value)

    def set_stat_for_char(stat, value, name, map):
        if name not in map.keys():
            return
        map[name].set_stat(stat, value)
        
    def set_level_for_char(value, name, map):
        if name not in map.keys():
            return
        map[name].set_level(value)
        
    # changes the stat value
    def change_stat(stat, change, name = "", map = None):
        if stat == "money":
            money.change_value(change)
        else:
            change_stat_for_char(stat, change, name, map)

    def change_stat_for_all(stat, delta, map):
        for character in map.keys():
            map[character].change_stat(stat, delta)

    def change_stat_for_char(stat, value, name, map):
        if name not in map.keys():
            return
        map[name].change_stat(stat, value)

    def reset_stats(map, name = ""):
        money.reset_change()

        if name != "" and name in map.keys():
            map[name].reset_changed_stats()
        else:
            for keys in map.keys():
                map[keys].reset_changed_stats()

    def load_character(name, title, map, start_data, runtime_data = None):
        if name not in map.keys():
            map[name] = Char(name, title)
            map[name].__dict__.update(start_data)

        map[name]._update(runtime_data)

    def update_character(name, map, data):
        map[name]._update(runtime_data)

    def remove_character(name, map):
        if name in map.keys():
            del(map[name])

label load_schools:

    $ load_character("secretary", "Secretary", charList['staff'], {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        },
    })

    $ load_character("parents", "Parents", charList, {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        },
    })

    $ load_character("teacher", "Teacher", charList['staff'], {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        },
    })
    $ load_character("high_school", "High School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_character("middle_school", "Middle School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_character("elementary_school", "Elementary School", charList['schools'], {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_character("school_mean_values", "Mean School", charList, {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 100),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    return
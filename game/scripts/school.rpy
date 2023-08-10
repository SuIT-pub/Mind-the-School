init -6 python:
    import math
    class School:
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

        def get_stat_obj(self, stat):
            if not stat in self.stats_objects:
                return None
            return self.stats_objects[stat]

        def set_stat(self, stat, value):
            stat_obj = self.get_stat_obj(stat)
            stat_obj.set_value(value)

            update_mean_values()

        def change_stat(self, stat, delta):
            stat_obj = self.get_stat_obj(stat)
            stat_obj.change_value(delta)

            update_mean_values()

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
                return self.get_stat_string(stat_name)

            split = value.split(',')

            for split_val in split:
                split_val = split_val.strip()
                stat_str = re.findall('\d+', split_val)
                if stat_str:
                    stat = int(''.join(stat_str))
                    
                    if (stat == self.get_stat_number(stat_name) or
                        (split_val.endswith('-') and self.get_stat_number(stat_name) <= stat) or
                        (split_val.endswith('+') and self.get_stat_number(stat_name) >= stat)
                    ):
                        return True
                    elif '-' in split_val:
                        stat_split = split_val.split('-')
                        if (len(stat_split) == 2 and 
                            stat_split[0].isdecimal() and 
                            stat_split[1].isdecimal() and
                            int(stat_split[0]) <= self.get_stat_number(stat_name) <= int(stat_split[1])
                        ):
                            return True

            return str(value) == self.get_stat_string(stat_name)

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

        def check_level(self, value):
            if value == "x":
                return self.get_level_str()

            split = value.split(',')

            for split_val in split:
                split_val = split_val.strip()
                level_str = re.findall('\d+', split_val)
                if level_str:
                    level = int(''.join(level_str))
                    
                    if (level == self.get_level() or
                        (split_val.endswith('-') and self.get_level() <= level) or
                        (split_val.endswith('+') and self.get_level() >= level)
                    ):
                        return True
                    elif '-' in split_val:
                        level_split = split_val.split('-')
                        if (len(level_split) == 2 and 
                            level_split[0].isdecimal() and 
                            level_split[1].isdecimal() and
                            int(level_split[0]) <= self.get_level() <= int(level_split[1])
                        ):
                            return True

            return str(value) == self.get_level_str()

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
    
    def get_school(school):
        if school in schools.keys():
            return schools[school]
        return None

    def get_lowest_level():
        level = 100
        for school in schools.values():
            if school.get_level() < level:
                level = school.get_level()

        return level

    def update_mean_values():
        stats = {}

        mean_level = 0

        school_amount = 0
        for keys in schools.keys():
            if keys == 'school_mean':
                continue
            if keys == 'middle_school' and loli_content == 0:
                continue
            if keys == 'elementary_school' and loli_content != 2:
                continue

            mean_level += schools[keys].get_level()
            school_amount += 1
            for stat_keys in schools[keys].get_stats().keys():
                if stat_keys not in stats:
                    stats[stat_keys] = 0
                stats[stat_keys] += schools[keys].get_stat_obj(stat_keys).get_value()
        
        mean_level /= school_amount

        schools["school_mean"].set_level(int(mean_level))

        for stat_keys in stats.keys():
            minLimit = get_stat_data(stat_keys).get_min_limit()
            maxLimit = get_stat_data(stat_keys).get_max_limit()
            stats[stat_keys] = clamp_stat(math.ceil((stats[stat_keys] / school_amount) * 100) / 100, minLimit, maxLimit)

            stat_obj = schools["school_mean"].get_stat_obj(stat_keys)

            if stat_obj == None:
                continue

            stat_obj.set_changed_value(math.ceil((stats[stat_keys] - schools["school_mean"].get_stat_obj(stat_keys).get_value()) * 100) / 100)
            stat_obj.set_value(stats[stat_keys])
    
    def set_stat_for_all(stat, value):
        schools["high_school"].set_stat(stat, value)
        schools["middle_school"].set_stat(stat, value)
        schools["elementary_school"].set_stat(stat, value)

    def change_stat_for_all(stat, delta):
        schools["high_school"].change_stat(stat, delta)
        schools["middle_school"].change_stat(stat, delta)
        schools["elementary_school"].change_stat(stat, delta)

    def load_school(name, title, start_data, runtime_data = None):
        if name not in schools.keys():
            schools[name] = School(name, title)
            schools[name].__dict__.update(start_data)

        schools[name]._update(runtime_data)

    def update_school(name, data):
        schools[name]._update(data)

    def remove_school(name):
        if name in schools.keys():
            del(schools[name])

label load_schools:
    $ remove_school("staff")

    $ load_school("high_school", "High School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_school("middle_school", "Middle School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_school("elementary_school", "Elementary School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    $ load_school("school_mean", "School Mean", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    return
init python:
    import math
    class School:
        stats_objects = {}

        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.level = Stat("level", 0)

            print(self.stats_objects)

        def get_stat_obj(self, stat):
            if not stat in self.stats_objects:
                return None
            return self.stats_objects[stat]

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
            print (self.stats_objects)
            return self.stats_objects

        def get_level(self):
            return self.level.get_value()

        def set_level(self, level):
            self.level.set_value(level)

        def display_stat(self, stat):
            stat_obj = self.get_stat_obj(stat)

            if stat_obj == None:
                return "NaN"

            return stat_obj.display_stat()
    
    def get_school(school):
        if school in schools.keys():
            return schools[school]
        return None

    def update_mean_values():
        stats = {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        }

        school_amount = 0
        for keys in schools.keys():
            if keys == 'school_mean':
                continue
            school_amount += 1
            for stat_keys in schools[keys].get_stats().keys():
                stats[stat_keys] += schools[keys].get_stat_obj(stat_keys).get_value()
        
        for stat_keys in stats.keys():
            stats[stat_keys] = clamp_stat(math.ceil((stats[stat_keys] / school_amount) * 100) / 100)

            stat_obj = schools["school_mean"].get_stat_obj(stat_keys)

            if stat_obj == None:
                continue

            stat_obj.set_changed_value(math.ceil((stats[stat_keys] - schools["school_mean"].get_stat_obj(stat_keys).get_value()) * 100) / 100)
            stat_obj.set_value(stats[stat_keys])
    
    def load_school(name, title, start_data):
        if "high_school" not in schools.keys():
            schools[name] = School(name, title)
            schools[name].__dict__.update(start_data)
    
    def load_school(name, title, start_data, runtime_data):
        load_school(name, title, start_data)
        schools[name].__dict__.update(runtime_data)

    def update_school(name, data):
        schools[name].__dict__.update(data)

label load_schools:
    load_school("high_school", "High School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    load_school("middle_school", "Middle School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    load_school("elementary_school", "Elementary School", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    load_school("staff", "Staff", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })

    load_school("school_mean", "School Mean", {
        'stats_objects': {
            "corruption": Stat("corruption", 0),
            "inhibition": Stat("inhibition", 0),
            "happiness": Stat("happiness", 20),
            "education": Stat("education", 10),
            "charm": Stat("charm", 8),
            "reputation": Stat("reputation", 12),
        }
    })
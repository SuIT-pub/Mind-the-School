init python:
    import math
    class School:
        stats = {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
            "money"     : 0,
        }

        changed_stats = {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
            "money"     : 0,
        }

        level = 0

        def __init__(self, name, title):
            self.name = name
            self.title = title
            print(name)

        def change_stat(self, stat, change):
            change_val = math.ceil(change * 100) / 100
            self.stats[stat] = clamp_stat(math.ceil((self.stats[stat] + change_val) * 100) / 100)
            self.changed_stats[stat] = change_val
            print("changed " + stat + " for " + self.title)
            update_mean_values()

        def get_stat(self, stat):
            if not stat in self.stats.keys():
                return -1
            return self.stats[stat]

        def reset_changed_stats(self):
            self.changed_stats = {
                "corruption": 0,
                "inhibition": 0,
                "happiness" : 0,
                "education" : 0,
                "charm"     : 0,
                "reputation": 0,
                "money"     : 0,
            }

        def get_level(self):
            return self.level

        def set_level(self, level):
            self.level = level

        def display_stat(self, stat):
            stat_value = self.stats[stat]

            if stat == "inhibition":
                stat_value = 100 - stat_value

            text = str(stat_value)
            global change
            change = self.changed_stats[stat]

            if (stat != "inhibition"):
                if change < 0:
                    text += "{color=#ff0000}{size=15}([change]){/size}{/color}"
                elif change > 0:
                    text += "{color=#00ff00}{size=15}(+[change]){/size}{/color}"
            else:
                if change < 0:
                    change = -change
                    text += "{color=#ff0000}{size=15}(+[change]){/size}{/color}"
                elif change > 0:
                    text += "{color=#00ff00}{size=15}(-[change]){/size}{/color}"

            return text

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
            for stat_keys in schools[keys].stats.keys():
                stats[stat_keys] += schools[keys].stats[stat_keys]
        
        for stat_keys in stats.keys():
            stats[stat_keys] = clamp_stat(math.ceil((stats[stat_keys] / school_amount) * 100) / 100)
            schools["school_mean"].changed_stats[stat_keys] = math.ceil((stats[stat_keys] - schools["school_mean"].stats[stat_keys]) * 100) / 100
            schools["school_mean"].stats[stat_keys] = stats[stat_keys]
            
label load_schools:

    $ schools["high_school"] = School("high_school", "High School");
    $ schools["high_school"].__dict__.update({
        'stats': {
            "corruption":    0,
            "inhibition":    0,
            "happiness" :   20,
            "education" :   10,
            "charm"     :    8,
            "reputation":   12,
        },
        'changed_stats': {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        },
        'level': 0,
    })

    $ schools["middle_school"] = School("middle_school", "Middle School");
    $ schools["middle_school"].__dict__.update({
        'stats': {
            "corruption":    0,
            "inhibition":    0,
            "happiness" :   20,
            "education" :   10,
            "charm"     :    8,
            "reputation":   12,
        },
        'changed_stats': {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        },
        'level': 0,
    })

    $ schools["elementary_school"] = School("elementary_school", "Elementary School");
    $ schools["elementary_school"].__dict__.update({
        'stats': {
            "corruption":    0,
            "inhibition":    0,
            "happiness" :   20,
            "education" :   10,
            "charm"     :    8,
            "reputation":   12,
        },
        'changed_stats': {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        },
        'level': 0,
    })

    $ schools["staff"] = School("staff", "Staff");
    $ schools["staff"].__dict__.update({
        'stats': {
            "corruption":    0,
            "inhibition":    0,
            "happiness" :   20,
            "education" :   10,
            "charm"     :    8,
            "reputation":   12,
        },
        'changed_stats': {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        },
        'level': 0,
    })

    $ schools["school_mean"] = School("school_mean", "School Mean");
    $ schools["school_mean"].__dict__.update({
        'stats': {
            "corruption":    0,
            "inhibition":    0,
            "happiness" :   20,
            "education" :   10,
            "charm"     :    8,
            "reputation":   12,
        },
        'changed_stats': {
            "corruption": 0,
            "inhibition": 0,
            "happiness" : 0,
            "education" : 0,
            "charm"     : 0,
            "reputation": 0,
        },
        'level': 0,
    })
init python:
    import re
    class Rule:
        unlock_conditions = []

        unlocked = {
            "high_school": False,
            "middle_school": False,
            "elementary_school": False,
        }

        def __init__(self, name, title):
            self.name = name
            self.title = title
            self.description = ""
            self.image_path = "images/journal/empty_image.png"
        
        def unlock(self, school):
            if school in self.unlocked:
                self.unlocked[school] = True;

        def isUnlocked(self, school):
            if school in self.unlocked:
                return self.unlocked[school]
            else:
                return False

        def is_condition_fullfilled(self, school, condition):
            if condition["type"] == "stat":
                stat = condition["stat"]
                value = condition["value"]

                needed_stat = get_stat(value, stat, school)

                if needed_stat != get_school(school).get_stat_string(stat):
                    return False

            elif condition["type"] == "unlocked":
                value = condition["rule"]
                if not rules[value].isUnlocked(school):
                    return False
            elif condition["type"] == "level":
                stat = condition["school"]
                value = condition["value"]

                print("stat: " + stat + " school: " + school)

                if stat == school or stat == "x":
                    level = get_level(value, school)

                    if (level != level_to_string(school)):
                        return False
            elif condition["type"] == "school":
                value = condition["school"]
                if school != value:
                    return False

            return True

        def isVisible(self, school):
            for condition in self.unlock_conditions:
                print("rule: " + self.name + ", type: " + condition["type"] + ", blocking: " + str(condition["blocking"]))
                is_fullfilled = self.is_condition_fullfilled(school, condition)
                print("fullfilled:" + str(is_fullfilled))
                if (not is_fullfilled and 
                condition["blocking"]):
                    print ("FALSE")
                    return False
            print ("TRUE")
            return True

        def canBeUnlocked(self, school):
            if school not in schools.keys():
                return False

            for condition in self.unlock_conditions:
                if self.is_condition_fullfilled(school, condition):
                    continue
                return False

            return True


    def get_visible_rules_by_school(school):
        output = []

        print("\n\n\n\n#############################\n\n\n\n")

        for rule in rules.values():
            if (rule.isVisible(school) and 
            not rule.isUnlocked(school) and
            rule.name not in output):
                output.append(rule.name)
                continue

        return output

    def get_visible_rules():
        output = []

        print("\n\n\n\n#############################\n\n\n\n")

        for rule in rules.values():
            if (rule.isVisible("high_school") and 
            not rule.isUnlocked("high_school") and
            rule.name not in output):
                output.append(rule.name)
                continue
            
            if loli_content >= 1:
                if (rule.isVisible("middle_school") and 
                not rule.isUnlocked("middle_school") and
                rule.name not in output):
                    output.append(rule.name)
                    continue

            if loli_content == 2:
                if (rule.isVisible("elementary_school") and 
                not rule.isUnlocked("elementary_school") and
                rule.name not in output):   
                    output.append(rule.name)
                    continue

        return output

    def get_unlockable_rules():
        output = []

        for rule in rules.values():
            high_unlock = rule.canBeUnlocked("high_school")
            high_unlocked = rule.isUnlocked("high_school")

            if (high_unlock and 
            not high_unlocked and 
            rule.name not in output):
                output.append(rule.name)
                continue

            if loli_content >= 1:
                middle_unlock = rule.canBeUnlocked("middle_school")
                middle_unlocked = rule.isUnlocked("middle_school")

                if (middle_unlock and 
                not middle_unlocked and 
                rule.name not in output):
                    output.append(rule.name)
                    continue

            if loli_content == 2:
                elementary_unlock = rule.canBeUnlocked("elementary_school")
                elementary_unlocked = rule.isUnlocked("elementary_school")

                if (elementary_unlock and 
                not elementary_unlocked and 
                rule.name not in output):
                    output.append(rule.name)
                    continue

        return output

    def get_unlockable_rules_by_school(school):
        output = []

        for rule in rules.values():
            unlock = rule.canBeUnlocked(school)
            unlocked = rule.isUnlocked(school)

            if (unlock and not unlocked and rule.name not in output):
                output.append(rule.name)
                continue

        return output

    def get_rule(rule_name):
        if rule_name not in rules.keys():
            return None
        return rules[rule_name]

    def load_rule(name, title):
        if name not in rules.keys():
            rules[name] = Rule(name, title)

    def load_rule(name, title, data):
        load_rule(name, title)
        rules[name].__dict__.update(data)

label load_rules:
    $ load_rule(
        "theoretical_sex_ed", 
        "Theoretical Sex Education",{
            'description': ("Students get a new sub+++ject in which they deal with the"
                " topic of the human body and human reproduction."
                " All on a theoretical basis, of course."),
            'unlock_conditions': [
                {
                    "type": "level",
                    "school": "x",
                    "value": "2+",
                    "blocking": False,
                },
                {
                    "type": "stat",
                    "stat": "corruption",
                    "value": "0+",
                    "blocking": False,
                }
            ],
            'image_path': 'images/journal/rules/theoretical_sex_ed.png',
        }
    )
    load_rule(
        "theoretical_digital_material", 
        "Use Digital Material for study in Theoretical Sex Ed",{
            'unlock_conditions': [
                {
                    "type": "level",
                    "school": "x",
                    "value": "3+",
                    "blocking": False,
                },
                {
                    "type": "unlocked",
                    "rule": "theoretical_sex_ed",
                    "blocking": False,
                }
            ],
            'image_path': 'images/journal/rules/theoretical_digital_sex_ed.png',
        }
    )
    load_rule(
        "theoretical_teacher_material", 
        "Use Teacher for study in Theoretical Sex Ed", {
            'unlock_conditions': [
                {
                    "type": "unlocked",
                    "rule": "theoretical_digital_material",
                    "blocking": False,
                }
            ],
            'image_path': 'images/journal/rules/theoretical_teacher_sex_ed.png',
        }
    )
    load_rule(
        "theoretical_student_material", 
        "Use Students for study in Theoretical Sex Ed", {
            'unlock_conditions': [
                {
                    "type": "unlocked",
                    "rule": "theoretical_teacher_material",
                    "blocking": False,
                }
            ]
        }
    )

    load_rule(
        "practical_sex_ed", 
        "Practical Sex Education", {
            'unlock_conditions': [
                {
                    "type": "level",
                    "school": "x",
                    "value": "4+",
                    "blocking": False,
                },
                {
                    "type": "unlocked",
                    "rule": "theoretical_sex_ed",
                    "blocking": False,
                }
            ]
        }
    )

    load_rule(
        "practical_teacher_material", 
        "Use Teacher for study in Practical Sex Ed", {
            'unlock_conditions': [
                {
                    "type": "level",
                    "school": "x",
                    "value": "3+",
                    "blocking": False,
                },
                {
                    "type": "unlocked",
                    "rule": "practical_sex_ed",
                    "blocking": False,
                }
            ]
        }
    )

    load_rule(
        "practical_student_material", 
        "Use Students for study in Practical Sex Ed", {
            'unlock_conditions': [
                {
                    "type": "unlocked",
                    "rule": "practical_teacher_material",
                    "blocking": False,
                }
            ]
        }
    )

    load_rule(
        "student_student_relation", 
        "Allowed Relationships between Students", {
            'description': ("Allows for students to have a relationship between"
                " each other and to openly show it.")
        }
    )

    load_rule(
        "student_teacher_relation", 
        "Allowed Relationships between Students and Teacher", {
            'description': ("Allows for teacher to engage in a relationship with"
                " students.")
        }
    )

    return